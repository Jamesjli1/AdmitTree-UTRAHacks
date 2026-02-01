"""
Mock university database for testing the scoring engine.
Structure: University -> Metadata (ec_quality) -> Programs -> Details
"""

UNIVERSITY_DB = {
    "University of Waterloo": {
        "ec_quality": 3,  # High EC expectations across all programs
        "co-op": ["yes"],  # University-level: Only Co-op available
        "programs": {
            "Computer Engineering": {
                "recommended_average": [92, 98],
                "interest_fields": ["circuits", "hardware", "physics", "robotics"],
                "required_courses": ["MHF4U", "MCV4U", "SPH4U", "SCH4U"]
            },
            "Software Engineering": {
                "recommended_average": [95, 99],
                "interest_fields": ["software", "programming", "algorithms", "systems"],
                "required_courses": ["MHF4U", "MCV4U", "SPH4U"]
            },
            "Arts and Business": {
                "recommended_average": [82, 88],
                "interest_fields": ["business", "culture", "writing", "management"],
                "required_courses": []
            }
        }
    },
    "University of Toronto": {
        "ec_quality": 3,  # High EC expectations across all programs
        "co-op": ["yes", "no"],  # University-level: ASIP (Co-op) and Regular available
        "programs": {
            "Computer Science": {
                "recommended_average": [94, 99],
                "interest_fields": ["software", "theory", "math", "ai", "data"],
                "required_courses": ["MHF4U"]
            },
            "Mechanical Engineering": {
                "recommended_average": [88, 95],
                "interest_fields": ["machines", "structures", "physics", "cars"],
                "required_courses": ["MHF4U", "MCV4U", "SPH4U", "SCH4U"]
            },
            "Electrical Engineering": {
                "recommended_average": [90, 96],
                "interest_fields": ["circuits", "electronics", "power", "signals"],
                "required_courses": ["MHF4U", "MCV4U", "SPH4U", "SCH4U"]
            }
        }
    },
    "McMaster University": {
        "ec_quality": 2,  # Moderate EC expectations
        "co-op": ["yes", "no"],  # University-level: Both streams available
        "programs": {
            "Computer Science": {
                "recommended_average": [85, 92],
                "interest_fields": ["software", "programming", "algorithms"],
                "required_courses": ["MHF4U"]
            },
            "Software Engineering": {
                "recommended_average": [87, 94],
                "interest_fields": ["software", "engineering", "systems"],
                "required_courses": ["MHF4U", "MCV4U", "SPH4U"]
            },
            "Health Sciences": {
                "recommended_average": [90, 96],
                "interest_fields": ["health", "medicine", "biology", "research"],
                "required_courses": ["MHF4U", "SCH4U", "SPH4U"]
            }
        }
    },
    "Queen's University": {
        "ec_quality": 2,  # Moderate EC expectations
        "co-op": ["yes", "no"],  # University-level: Both streams available
        "programs": {
            "Computer Science": {
                "recommended_average": [83, 90],
                "interest_fields": ["software", "programming", "theory"],
                "required_courses": ["MHF4U"]
            },
            "Engineering": {
                "recommended_average": [85, 93],
                "interest_fields": ["engineering", "design", "problem-solving"],
                "required_courses": ["MHF4U", "MCV4U", "SPH4U", "SCH4U"]
            }
        }
    },
    "University of British Columbia": {
        "ec_quality": 3,  # High EC expectations across all programs
        "co-op": ["yes", "no"],  # University-level: Both streams available
        "programs": {
            "Computer Science": {
                "recommended_average": [92, 97],
                "interest_fields": ["software", "ai", "data", "systems"],
                "required_courses": ["MHF4U"]
            },
            "Engineering": {
                "recommended_average": [88, 95],
                "interest_fields": ["engineering", "design", "physics"],
                "required_courses": ["MHF4U", "MCV4U", "SPH4U", "SCH4U"]
            }
        }
    }
}

