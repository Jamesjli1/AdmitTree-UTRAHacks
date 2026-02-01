"""
University Scoring Engine - Matches students to programs based on multiple criteria.
"""

from services.database import fetch_university_data


def get_university_db():
    """
    Get university database from MongoDB.
    New schema returns one "mega document" that contains metadata keys
    like _id/apply_deadline plus universities as top-level keys.
    This function normalizes it to:
        { "University Name": {ec_quality, "co-op", programs, ...}, ... }
    """
    raw = fetch_university_data()

    if not raw:
        raise RuntimeError("University database is empty or not found in MongoDB.")

    if not isinstance(raw, dict):
        raise TypeError(f"University database must be a dict, got {type(raw)}")

    # Remove metadata keys that are not universities
    meta_keys = {"_id", "apply_deadline"}
    UNIVERSITY_DB = {k: v for k, v in raw.items() if k not in meta_keys}

    # Normalize fields a bit (helps avoid bugs)
    for uni_name, uni_data in UNIVERSITY_DB.items():
        if not isinstance(uni_data, dict):
            continue

        # Normalize coop field to list of lowercase strings
        coop = uni_data.get("co-op") or uni_data.get("co_op") or []
        if isinstance(coop, str):
            coop = [coop]
        if not isinstance(coop, list):
            coop = [str(coop)]
        uni_data["co-op"] = [str(x).strip().lower() for x in coop]

        # Ensure programs is a dict
        programs = uni_data.get("programs", {})
        if programs is None:
            programs = {}
        uni_data["programs"] = programs

    return UNIVERSITY_DB


class UniversityMatcher:
    def __init__(self, user_profile):
        self.user = user_profile

        # ✅ Normalize JSON shapes (tuples don't exist in JSON)
        self.user["courses_taken"] = self._normalize_courses(self.user.get("courses_taken", []))
        self.user["extra_curriculars"] = self._normalize_ecs(self.user.get("extra_curriculars", []))
        self.user["major_interests"] = self._normalize_interests(self.user.get("major_interests", []))

        self.grade = user_profile["grade_level"]
        self.weights = self._get_dynamic_weights()

    # -----------------------------
    # Normalizers (fix common 500s)
    # -----------------------------
    def _normalize_courses(self, courses):
        """
        Accepts:
          - [["ENG4U", 90], ["MHF4U", 92]]
          - [("ENG4U", 90), ...]
          - [{"course_code":"ENG4U","grade":90}, {"code":"MHF4U","grade":92}]
        Returns: list[tuple(code, grade)]
        """
        out = []
        for c in courses:
            if isinstance(c, (list, tuple)) and len(c) >= 2:
                out.append((c[0], c[1]))
            elif isinstance(c, dict):
                code = c.get("course_code") or c.get("code") or c.get("name")
                grade = c.get("grade")
                if code is not None and grade is not None:
                    out.append((code, grade))
        return out

    def _normalize_ecs(self, ecs):
        """
        Accepts:
          - [["DECA", 3], ["Robotics", 2]]
          - [{"name":"DECA","level":3}]
        Returns: list[tuple(name, level)]
        """
        out = []
        for ec in ecs:
            if isinstance(ec, (list, tuple)) and len(ec) >= 2:
                out.append((ec[0], ec[1]))
            elif isinstance(ec, dict):
                name = ec.get("name")
                level = ec.get("level")
                if name is not None and level is not None:
                    out.append((name, level))
        return out

    def _normalize_interests(self, interests):
        """
        Ensures interests is a list of lowercase strings.
        """
        if interests is None:
            return []
        if isinstance(interests, str):
            return [interests.strip().lower()]
        if isinstance(interests, list):
            return [str(x).strip().lower() for x in interests if str(x).strip()]
        return [str(interests).strip().lower()]

    # -----------------------------
    # Weighting
    # -----------------------------
    def _get_dynamic_weights(self):
        """
        Adjusts priorities based on how close the student is to graduating.
        """
        if self.grade <= 10:
            return {"interest": 0.60, "academic": 0.30, "ec": 0.03}
        else:
            return {"interest": 0.1, "academic": 0.8, "ec": 0.1}

    # -----------------------------
    # Scoring Components
    # -----------------------------
    def _calculate_academic_score(self, min_avg, max_avg, required_courses):
        """
        Checks if user meets grade cutoffs and has taken required courses.
        Rewards competitive programs (higher averages) when requirements are met.
        """
        user_avg = self.user["average"]

        # A. Grade Range Interpolation
        if user_avg >= max_avg:
            grade_score = 1.0
        elif user_avg < (min_avg - 5):
            grade_score = 0.0
        else:
            grade_score = (user_avg - (min_avg - 5)) / (max_avg - (min_avg - 5))

        # B. Required Course Check (Grade 11/12 Only)
        course_penalty = 1.0
        if self.grade >= 11:
            user_courses = [str(c[0]).strip().lower() for c in self.user["courses_taken"]]
            missing = []

            for req in required_courses:
                req_str = str(req).strip()
                req_lower = req_str.lower()

                # skip generic requirements
                if any(phrase in req_lower for phrase in ["one more", "additional", "any u", "any m", "another"]):
                    continue

                # alternatives like "ENG4U / EAE4U"
                alternatives = [alt.strip().lower() for alt in req_str.split("/")]
                found_match = False
                for alt in alternatives:
                    for user_course in user_courses:
                        if alt in user_course or user_course in alt:
                            found_match = True
                            break
                    if found_match:
                        break

                if not found_match:
                    missing.append(req_str)

            if self.grade == 12 and missing:
                course_penalty = max(0, 1.0 - (len(missing) * 0.15))
            elif self.grade == 11 and missing:
                course_penalty = 1.0  # keep as warning

        # C. Competitiveness Bonus
        competitiveness_bonus = 0.0
        if user_avg >= max_avg:
            if max_avg >= 95:
                competitiveness_bonus = 0.20 + (0.10 * ((max_avg - 95) / 5))
            elif max_avg >= 90:
                competitiveness_bonus = 0.10 + (0.10 * ((max_avg - 90) / 5))
            elif max_avg >= 85:
                competitiveness_bonus = 0.05 + (0.05 * ((max_avg - 85) / 5))
            elif max_avg >= 80:
                competitiveness_bonus = 0.02 + (0.03 * ((max_avg - 80) / 5))
        elif user_avg >= (max_avg - 2):
            proximity = (user_avg - (max_avg - 2)) / 2
            if max_avg >= 95:
                competitiveness_bonus = (0.20 + (0.10 * ((max_avg - 95) / 5))) * proximity * 0.5
            elif max_avg >= 90:
                competitiveness_bonus = (0.10 + (0.10 * ((max_avg - 90) / 5))) * proximity * 0.5
            elif max_avg >= 85:
                competitiveness_bonus = (0.05 + (0.05 * ((max_avg - 85) / 5))) * proximity * 0.5
            elif max_avg >= 80:
                competitiveness_bonus = (0.02 + (0.03 * ((max_avg - 80) / 5))) * proximity * 0.5

        final_score = min(1.30, (grade_score * course_penalty) + competitiveness_bonus)
        return final_score

    def _calculate_interest_score(self, program_interests):
        """
        Coverage score: matches / total program keywords (case-insensitive)
        """
        user_interests = set(self.user["major_interests"])
        prog_interests = set(str(i).strip().lower() for i in program_interests)

        if not prog_interests:
            return 0.0

        matches = user_interests.intersection(prog_interests)
        return len(matches) / len(prog_interests)

    def _calculate_ec_score(self, required_level):
        """
        Matches user's highest EC leadership level against program expectation.
        """
        if not self.user["extra_curriculars"]:
            user_best = 0
        else:
            user_best = max([ec[1] for ec in self.user["extra_curriculars"]])

        if user_best >= required_level:
            return 1.0 + (0.05 * (user_best - required_level))
        else:
            return max(0, 1.0 - (0.2 * (required_level - user_best)))

    def _calculate_coop_fit(self, program_coop_options):
        """
        program_coop_options example: ["yes", "no"] or ["yes"]
        """
        user_wants_coop = self.user["wants_coop"]

        if isinstance(program_coop_options, str):
            opts = [program_coop_options]
        elif isinstance(program_coop_options, list):
            opts = program_coop_options
        else:
            opts = [str(program_coop_options)]

        opts = [str(x).strip().lower() for x in opts]

        if user_wants_coop:
            return 1.0 if "yes" in opts else 0.85
        else:
            return 1.0 if "no" in opts else 0.92

    # -----------------------------
    # Main Ranker
    # -----------------------------
    def get_ranked_programs(self):
        results = []

        UNIVERSITY_DB = get_university_db()

        for uni_name, uni_data in UNIVERSITY_DB.items():
            if "ec_quality" not in uni_data:
                raise ValueError(f"University '{uni_name}' missing 'ec_quality'. Keys: {list(uni_data.keys())}")

            if "co-op" not in uni_data:
                raise ValueError(f"University '{uni_name}' missing 'co-op'. Keys: {list(uni_data.keys())}")

            if "programs" not in uni_data:
                raise ValueError(f"University '{uni_name}' missing 'programs'. Keys: {list(uni_data.keys())}")

            uni_ec_quality = uni_data["ec_quality"]
            uni_coop_options = uni_data["co-op"]
            programs = uni_data["programs"]

            if not isinstance(programs, dict):
                raise ValueError(f"University '{uni_name}': 'programs' must be dict, got {type(programs)}")

            for prog_name, details in programs.items():
                if not isinstance(details, dict):
                    continue

                if "recommended_average" not in details:
                    continue  # skip broken entries instead of hard failing

                recommended_avg = details["recommended_average"]
                if not isinstance(recommended_avg, list):
                    continue

                if len(recommended_avg) == 1:
                    recommended_avg = [recommended_avg[0] - 2, recommended_avg[0] + 2]
                if len(recommended_avg) < 2:
                    continue

                required_courses = details.get("required_courses", [])
                interests = details.get("interests", [])

                # component scores
                s_acad = self._calculate_academic_score(
                    recommended_avg[0], recommended_avg[1], required_courses
                )
                s_int = self._calculate_interest_score(interests)
                s_ec = self._calculate_ec_score(uni_ec_quality)

                base_score = (
                    (s_acad * self.weights["academic"]) +
                    (s_int * self.weights["interest"]) +
                    (s_ec * self.weights["ec"])
                )

                coop_mult = self._calculate_coop_fit(uni_coop_options)
                final_score = base_score * coop_mult * 100

                results.append({
                    "university": uni_name,
                    "program": prog_name,
                    "score": round(final_score, 1),
                    "breakdown": {
                        "academic": round(s_acad, 2),
                        "interest": round(s_int, 2),
                        "ec": round(s_ec, 2),
                        "coop_fit": round(coop_mult, 2)
                    }
                })

        sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

        # Normalize scores if top > 100
        if sorted_results:
            max_score = sorted_results[0]["score"]
            if max_score > 100:
                factor = 100 / max_score
                for r in sorted_results:
                    r["score"] = round(r["score"] * factor, 1)

        return sorted_results
