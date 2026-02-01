"""
University Scoring Engine - Matches students to programs based on multiple criteria.
"""

from services.database import fetch_university_data
import numpy as np


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

def get_program_interests():
    """
    Get a dictionary mapping program names to their interests arrays.
    Returns: dict of {program_name: [interests]}
    """
    from services.database import get_universities_collection
    
    collection = get_universities_collection()
    
    # Define the aggregation pipeline
    pipeline = [
        # Step 1: Convert the entire document into an array of key-value pairs
        {"$project": {"data": {"$objectToArray": "$$ROOT"}}},
        
        # Step 2: Unwind to process each key (University names, _id, etc.)
        {"$unwind": "$data"},
        
        # Step 3: Filter for keys that are universities (they contain a 'programs' field)
        {"$match": {"data.v.programs": {"$exists": True}}},
        
        # Step 4: Convert the 'programs' object within each university to an array
        {"$project": {
            "program_entries": {"$objectToArray": "$data.v.programs"}
        }},
        
        # Step 5: Unwind the programs to get individual program documents
        {"$unwind": "$program_entries"},
        
        # Step 6: Project the final Program_name and interests array
        {"$project": {
            "_id": 0,
            "program_name": "$program_entries.k",
            "interests": "$program_entries.v.interests"
        }}
    ]
    
    # Execute query and format as a dictionary { Program_name: interests[] }
    results = collection.aggregate(pipeline)
    program_interests_map = {res['program_name']: res['interests'] for res in results}
    
    return program_interests_map


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
    import numpy as np
from services.database import fetch_university_data

class UniversityMatcher:
    def __init__(self, user_profile):
        self.user = user_profile
        self.user_avg = float(user_profile.get('average', 0))
        self.grade = int(user_profile.get('grade_level', 12))

    def _calculate_academic_score(self, min_avg, max_avg, required_courses):
        """Uses sigmoid logic with competitive bias for the raw academic base."""
        # Sigmoid midpoint centered at the min_avg
        z = 0.8 * (self.user_avg - min_avg)
        base_grade_score = 1 / (1 + np.exp(-z))

        # Competitive Bias
        bias = 1.0 + ((max_avg - 85) / 100) if self.user_avg >= 92 and max_avg >= 90 else 1.0
        
        # Course Match
        user_courses = [c[0].upper().strip() for c in self.user.get('courses_taken', [])]
        req_courses = [str(c).split(' ')[0].upper().strip() for c in required_courses]
        penalty = 1.0
        if self.grade == 12 and req_courses:
            missing = [r for r in req_courses if r not in user_courses]
            penalty = max(0.1, 1.0 - (len(missing) * 0.15))

        return (base_grade_score * penalty) * bias

    def get_ranked_programs(self):
        db = fetch_university_data()
        raw_results = []

        # Step 1: Calculate Raw Scores
        for uni_name, uni_data in db.items():
            if uni_name in ["_id", "apply_deadline"]: continue
            programs = uni_data.get('programs', {})
            for prog_name, details in programs.items():
                # Interest Match
                user_ints = set(i.lower() for i in self.user.get('major_interests', []))
                prog_ints = set(i.lower() for i in details.get('interests', []))
                s_int = len(user_ints.intersection(prog_ints)) / len(user_ints) if user_ints else 0
                
                # Academic Score
                avg_range = details.get('recommended_average', [80, 85])
                s_acad = self._calculate_academic_score(avg_range[0], avg_range[1], details.get('required_courses', []))
                
                # Raw weighted total
                raw_score = (s_int * 0.5) + (s_acad * 0.5)
                
                raw_results.append({
                    "university": uni_name,
                    "program": prog_name,
                    "raw_score": raw_score
                })

        # Step 2: Z-Score Standardization
        scores = [r['raw_score'] for r in raw_results]
        if len(scores) > 1:
            mean_val = np.mean(scores)
            std_dev = np.std(scores)
            
            for res in raw_results:
                # Calculate Z = (x - mean) / std_dev
                z_score = (res['raw_score'] - mean_val) / std_dev if std_dev > 0 else 0
                
                # Map Z-Score to 0-100 range. 
                # A Z-score of 2 (2 standard deviations above mean) becomes ~98%
                final_mapped_score = 1 / (1 + np.exp(-z_score)) * 100
                res['score'] = round(final_mapped_score, 1)
        else:
            for res in raw_results: res['score'] = 100.0

        return sorted(raw_results, key=lambda x: x['score'], reverse=True)