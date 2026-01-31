"""
University Scoring Engine - Matches students to programs based on multiple criteria.
"""

from services.database import fetch_university_data

def get_university_db():
    """
    Get university database from MongoDB.
    Raises an exception if MongoDB is unavailable or not configured.
    """
    return fetch_university_data()


class UniversityMatcher:
    def __init__(self, user_profile):
        self.user = user_profile
        self.grade = user_profile['grade_level']
        self.weights = self._get_dynamic_weights()

    def _get_dynamic_weights(self):
        """
        Adjusts priorities based on how close the student is to graduating.
        """
        # Grade 9/10: Exploration Mode (Interests > Grades)
        if self.grade <= 10:
            return {"interest": 0.60, "academic": 0.30, "ec": 0.03}
        
        # Grade 11/12: Execution Mode (Grades/Reqs > Interests)
        else:
            return {"interest": 0.1, "academic": 0.8, "ec": 0.1}

    def _calculate_academic_score(self, min_avg, max_avg, required_courses):
        """
        Checks if user meets grade cutoffs and has taken required courses.
        Rewards competitive programs (higher averages) when requirements are met.
        """
        user_avg = self.user['average']
        
        # --- A. Grade Range Interpolation ---
        if user_avg >= max_avg:
            grade_score = 1.0
        elif user_avg < (min_avg - 5):  # 5% buffer zone before scoring 0
            grade_score = 0.0
        else:
            # Linear scaling between (min-5) and max
            grade_score = (user_avg - (min_avg - 5)) / (max_avg - (min_avg - 5))

        # --- B. Required Course Check (Grade 11/12 Only) ---
        course_penalty = 1.0
        if self.grade >= 11:
            user_courses = [c[0] for c in self.user['courses_taken']]  # Extract subject names
            missing = []
            
            for req in required_courses:
                # Skip generic requirements like "One more U or M course"
                req_lower = req.lower()
                if any(phrase in req_lower for phrase in ["one more", "additional", "any u", "any m", "another"]):
                    continue  # Don't penalize for generic requirements
                
                # Handle alternatives (e.g., "ENG4U / EAE4U")
                # Split by "/" and check if any alternative is contained in user's courses
                alternatives = [alt.strip() for alt in req.split('/')]
                found_match = False
                for alt in alternatives:
                    # Check if this alternative is contained in any user course
                    # or if any user course is contained in this alternative
                    for user_course in user_courses:
                        if alt in user_course or user_course in alt:
                            found_match = True
                            break
                    if found_match:
                        break
                
                if not found_match:
                    # Course is truly missing
                    missing.append(req)
            
            # If missing courses in Gr 12, heavy penalty
            if self.grade == 12 and missing:
                course_penalty = max(0, 1.0 - (len(missing) * 0.15)) 
            # If Gr 11, slight warning penalty (they have time to take them)
            elif self.grade == 11 and missing:
                course_penalty = 1.0  # No penalty yet, just warning (optional: 0.95)

        # --- C. Competitiveness Bonus ---
        # Reward meeting/exceeding requirements of competitive programs (higher averages)
        competitiveness_bonus = 0.0
        if user_avg >= max_avg:
            # User meets/exceeds requirements - give bonus based on program competitiveness
            # More competitive programs (higher max_avg) get bigger bonuses
            # Scale: max_avg of 70-80 = no bonus, 80-90 = small bonus, 90-95 = larger bonus, 95+ = highest bonus
            if max_avg >= 95:
                # Extremely competitive: bonus of 0.20-0.30 based on how high the requirement is
                competitiveness_bonus = 0.20 + (0.10 * ((max_avg - 95) / 5))  # 0.20 at 95, up to 0.30 at 100
            elif max_avg >= 90:
                # Highly competitive: bonus of 0.10-0.20 based on how high the requirement is
                competitiveness_bonus = 0.10 + (0.10 * ((max_avg - 90) / 5))  # 0.10 at 90, up to 0.20 at 95
            elif max_avg >= 85:
                # Moderately competitive: bonus of 0.05-0.10
                competitiveness_bonus = 0.05 + (0.05 * ((max_avg - 85) / 5))  # 0.05 at 85, up to 0.10 at 90
            elif max_avg >= 80:
                # Somewhat competitive: small bonus
                competitiveness_bonus = 0.02 + (0.03 * ((max_avg - 80) / 5))  # 0.02 at 80, up to 0.05 at 85
            # max_avg < 80: no bonus (less competitive programs)
        elif user_avg >= (max_avg - 2):
            # User is very close to meeting requirements - give partial bonus
            proximity = (user_avg - (max_avg - 2)) / 2  # 0 to 1 based on how close
            if max_avg >= 95:
                competitiveness_bonus = (0.20 + (0.10 * ((max_avg - 95) / 5))) * proximity * 0.5
            elif max_avg >= 90:
                competitiveness_bonus = (0.10 + (0.10 * ((max_avg - 90) / 5))) * proximity * 0.5
            elif max_avg >= 85:
                competitiveness_bonus = (0.05 + (0.05 * ((max_avg - 85) / 5))) * proximity * 0.5
            elif max_avg >= 80:
                competitiveness_bonus = (0.02 + (0.03 * ((max_avg - 80) / 5))) * proximity * 0.5

        # Cap the final score at 1.30 to allow for higher bonuses for extremely competitive programs
        final_score = min(1.30, (grade_score * course_penalty) + competitiveness_bonus)
        return final_score

    def _calculate_interest_score(self, program_interests):
        """
        Jaccard Similarity: How many of the program's tags match the user's tags?
        """
        user_interests = set(self.user['major_interests'])
        prog_interests = set(program_interests)
        
        if not prog_interests:
            return 0.0
        
        matches = user_interests.intersection(prog_interests)
        # Score = matches / total program keywords (Coverage)
        return len(matches) / len(prog_interests)

    def _calculate_ec_score(self, required_level):
        """
        Matches user's highest EC leadership level against program expectation.
        """
        if not self.user['extra_curriculars']:
            user_best = 0
        else:
            user_best = max([ec[1] for ec in self.user['extra_curriculars']])

        # Bonus if they exceed requirements, penalty if they fail
        if user_best >= required_level:
            return 1.0 + (0.05 * (user_best - required_level))
        else:
            return max(0, 1.0 - (0.2 * (required_level - user_best)))

    def _calculate_coop_fit(self, program_coop_options):
        """
        Determines fit based on user preference vs. available options list.
        program_coop_options example: ["yes", "no"] or ["yes"]
        """
        user_wants_coop = self.user['wants_coop']  # boolean
        
        # CASE 1: User WANTS Co-op
        if user_wants_coop:
            if "yes" in program_coop_options:
                return 1.0  # Program offers what user wants. Perfect.
            else:
                return 0.85  # Penalty: Program ONLY has regular stream.

        # CASE 2: User DOES NOT WANT Co-op
        else:
            if "no" in program_coop_options:
                return 1.0  # Program offers regular stream. Perfect.
            else:
                return 0.92  # Friction Penalty: Program forces Co-op (mandatory).

    def get_ranked_programs(self):
        results = []
        
        # Fetch university data from MongoDB
        UNIVERSITY_DB = get_university_db()
        
        for uni_name, uni_data in UNIVERSITY_DB.items():
            # Validate university-level fields
            if 'ec_quality' not in uni_data:
                raise ValueError(f"University '{uni_name}' missing required field 'ec_quality'. Available fields: {list(uni_data.keys())}")
            
            if 'co-op' not in uni_data:
                raise ValueError(f"University '{uni_name}' missing required field 'co-op'. Available fields: {list(uni_data.keys())}")
            
            if 'programs' not in uni_data:
                raise ValueError(f"University '{uni_name}' missing required field 'programs'. Available fields: {list(uni_data.keys())}")
            
            # Get university-level metadata
            uni_ec_quality = uni_data['ec_quality']
            uni_coop_options = uni_data['co-op']  # University-level co-op options
            programs = uni_data['programs']
            
            if not isinstance(programs, dict):
                raise ValueError(f"University '{uni_name}': 'programs' must be a dictionary, got {type(programs)}")
            
            for prog_name, details in programs.items():
                try:
                    # Validate required program fields
                    if 'recommended_average' not in details:
                        raise KeyError(f"Program '{prog_name}' at university '{uni_name}' missing 'recommended_average'")
                    
                    recommended_avg = details['recommended_average']
                    if not isinstance(recommended_avg, list):
                        raise ValueError(
                            f"Program '{prog_name}' at university '{uni_name}': "
                            f"'recommended_average' must be a list, got {type(recommended_avg)}"
                        )
                    
                    if len(recommended_avg) == 1:
                        recommended_avg = [recommended_avg[0] - 2, recommended_avg[0] + 2]

                    if len(recommended_avg) < 2:
                        raise ValueError(
                            f"Program '{prog_name}' at university '{uni_name}': "
                            f"'recommended_average' must have at least 2 elements (min and max), "
                            f"got {len(recommended_avg)} elements: {recommended_avg}"
                        )
                    
                    # Validate other fields with defaults
                    required_courses = details.get('required_courses', [])
                    if not isinstance(required_courses, list):
                        raise ValueError(
                            f"Program '{prog_name}' at university '{uni_name}': "
                            f"'required_courses' must be a list, got {type(required_courses)}"
                        )
                    
                    interests = details.get('interests', [])
                    if not isinstance(interests, list):
                        raise ValueError(
                            f"Program '{prog_name}' at university '{uni_name}': "
                            f"'interests' must be a list, got {type(interests)}"
                        )
                    
                    # 1. Component Scores
                    s_acad = self._calculate_academic_score(
                        recommended_avg[0],
                        recommended_avg[1],
                        required_courses
                    )
                    
                    s_int = self._calculate_interest_score(interests)
                    
                    # Use university-level ec_quality
                    s_ec = self._calculate_ec_score(uni_ec_quality)
                    
                    # 2. Weighted Base Calculation
                    base_score = (
                        (s_acad * self.weights['academic']) +
                        (s_int * self.weights['interest']) +
                        (s_ec * self.weights['ec'])
                    )
                    
                    # 3. Apply Multipliers (Co-op) - use university-level co-op options
                    coop_mult = self._calculate_coop_fit(uni_coop_options)
                    
                    final_score = base_score * coop_mult * 100  # Convert to percentage

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
                except (KeyError, ValueError, IndexError, TypeError) as e:
                    # Provide detailed error information
                    raise ValueError(
                        f"Error processing program '{prog_name}' at university '{uni_name}': {e}. "
                        f"Available fields: {list(details.keys())}. "
                        f"recommended_average value: {details.get('recommended_average', 'MISSING')}. "
                        f"recommended_average type: {type(details.get('recommended_average', None))}"
                    ) from e
        
        # Return sorted by highest score
        sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
        
        # Normalize scores to cap at 100% while preserving relative rankings
        if sorted_results:
            max_score = sorted_results[0]['score']
            if max_score > 100:
                # Scale all scores proportionally so the highest becomes 100%
                normalization_factor = 100 / max_score
                for result in sorted_results:
                    result['score'] = round(result['score'] * normalization_factor, 1)
        
        return sorted_results

