import json
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# 1. FINAL DATA: Includes Steps + Deadlines + CAREER OUTCOMES
data = {
  "apply_deadline": "January 15",
  "University of Toronto": {
    "ec_quality": 5,
    "co-op": ["yes"],
    "steps": [
        "<b>1. Apply on OUAC:</b> Submit by <b>January 15</b> (Recommended Early: Dec 1).",
        "<b>2. Join Engineering Applicant Portal:</b> Access via email link sent after OUAC submission.",
        "<b>3. Online Student Profile (OSP):</b> MANDATORY. Deadline <b>January 15</b>. Includes extracurriculars.",
        "<b>4. Personal Profile:</b> Answer 3 random questions (1 written, 2 video) to test resilience.",
        "<b>5. Submit Documents:</b> Upload transcripts by <b>January 15</b>."
    ],
    "programs": {
      "Mechanical Engineering": { 
          "recommended_average": [88, 93], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U", "One U/M"], 
          "interests": ["mechanics", "thermodynamics", "design", "manufacturing"],
          "outcomes": ["Automotive Engineer", "Manufacturing Manager", "HVAC Systems Designer"]
      },
      "Computer Engineering": { 
          "recommended_average": [90, 95], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U", "One U/M"], 
          "interests": ["programming", "electronics", "computer networking"],
          "outcomes": ["Software Developer", "Embedded Systems Architect", "Network Engineer"]
      },
      "Electrical Engineering": { 
          "recommended_average": [90, 95], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U", "One U/M"], 
          "interests": ["circuits", "signal processing", "communications"],
          "outcomes": ["Power Systems Engineer", "Control Systems Designer", "Telecommunications Specialist"]
      },
      "Civil Engineering": { 
          "recommended_average": [88, 93], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U", "One U/M"], 
          "interests": ["building", "planning", "transportation"],
          "outcomes": ["Structural Engineer", "Construction Project Manager", "Urban Planner"]
      },
      "Chemical Engineering": { 
          "recommended_average": [88, 93], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U", "One U/M"], 
          "interests": ["chemistry", "materials", "biology"],
          "outcomes": ["Process Engineer", "Environmental Consultant", "Quality Control Manager"]
      },
      "Engineering Science": { 
          "recommended_average": [93, 98], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U", "One U/M"], 
          "interests": ["advanced mathematics", "theoretical concepts", "research"],
          "outcomes": ["Research Scientist", "Biomedical R&D Engineer", "Academic Professor"]
      },
      "Track One": { 
          "recommended_average": [92, 97], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U", "One U/M"], 
          "interests": ["interdisciplinary studies", "flexible curriculum"],
          "outcomes": ["Specialized Engineer (matches chosen major)", "Technical Consultant", "Project Manager"]
      },
      "Undeclrared": { 
          "recommended_average": [90, 95], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U", "One U/M"], 
          "interests": ["varied engineering fields", "exploratory studies"],
          "outcomes": ["Flexible Career Path", "Engineering Consultant", "Operations Analyst"]
      },
      "Industrial Engineering": { 
          "recommended_average": [88, 93], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U", "One U/M"], 
          "interests": ["systems optimization", "operations research", "human factors"],
          "outcomes": ["Supply Chain Analyst", "Process Improvement Engineer", "Data Scientist"]
      },
      "Materials Engineering": { 
          "recommended_average": [88, 93], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U", "One U/M"], 
          "interests": ["nanotechnology", "metallurgy", "polymers"],
          "outcomes": ["Metallurgist", "Product Development Engineer", "Failure Analyst"]
      },
      "Mineral Engineering": { 
          "recommended_average": [88, 93], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U", "One U/M"], 
          "interests": ["mining processes", "geology", "environmental impact"],
          "outcomes": ["Mine Planning Engineer", "Geotechnical Engineer", "Mineral Exploration Consultant"]
      }
    }
  },
  "University of Waterloo": {
    "ec_quality": 5, "co-op": ["yes"],
    "steps": [
        "<b>1. Apply on OUAC:</b> Deadline <b>January 15</b>.",
        "<b>2. Admission Information Form (AIF):</b> MANDATORY. Deadline <b>January 30</b>. Focuses on extracurriculars.",
        "<b>3. Online Video Interview:</b> Strongly recommended. Completed via Kira Talent by <b>mid-February</b>.",
        "<b>4. Submit Documents:</b> Upload transcripts to Quest portal by <b>January 30</b>."
    ],
    "programs": {
      "Architectural Engineering": { 
          "recommended_average": [85, 90], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U", "One U/M"], 
          "outcomes": ["Building Systems Engineer", "Structural Designer", "Energy Efficiency Consultant"]
      },
      "Biomedical Engineering": { 
          "recommended_average": [88, 93], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U", "One U/M"], 
          "outcomes": ["Medical Device Designer", "Clinical Engineer", "Biomechanics Researcher"]
      },
      "Chemical Engineering": { 
          "recommended_average": [85, 89], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U", "One U/M"], 
          "outcomes": ["Process Engineer", "Petrochemical Analyst", "Environmental Safety Officer"]
      },
      "Civil Engineering": { 
          "recommended_average": [84, 88], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U", "One U/M"], 
          "outcomes": ["Structural Engineer", "Transportation Planner", "Site Superintendent"]
      },
      "Computer Engineering": { 
          "recommended_average": [90, 95], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U", "One U/M"], 
          "outcomes": ["Software Architect", "Hardware Design Engineer", "Cybersecurity Specialist"]
      },
      "Electrical Engineering": { 
          "recommended_average": [89, 94], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U", "One U/M"], 
          "outcomes": ["Power Grid Engineer", "Control Systems Specialist", "Electronics Designer"]
      },
      "Environmental Engineering": { 
          "recommended_average": [85, 90], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U", "One U/M"], 
          "outcomes": ["Water Resource Engineer", "Sustainability Consultant", "Waste Management Specialist"]
      },
      "Geological Engineering": { 
          "recommended_average": [84, 89], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U", "One U/M"], 
          "outcomes": ["Geotechnical Engineer", "Groundwater Hydrologist", "Mineral Exploration Geologist"]
      },
      "Mechanical Engineering": { 
          "recommended_average": [88, 93], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U", "One U/M"], 
          "outcomes": ["Mechanical Design Engineer", "Automotive Systems Engineer", "Manufacturing Supervisor"]
      },
      "Mechatronics Engineering": { 
          "recommended_average": [90, 95], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U", "One U/M"], 
          "outcomes": ["Robotics Engineer", "Automation Specialist", "Control Systems Designer"]
      },
      "Nanotechnology Engineering": { 
          "recommended_average": [89, 94], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U", "One U/M"], 
          "outcomes": ["Nanomaterials Scientist", "Microchip Process Engineer", "Biotech Researcher"]
      },
      "Software Engineering": { 
          "recommended_average": [91, 96], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U", "One U/M"], 
          "outcomes": ["Full Stack Developer", "AI/Machine Learning Engineer", "DevOps Engineer"]
      },
      "Systems Design Engineering": { 
          "recommended_average": [90, 95], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U", "One U/M"], 
          "outcomes": ["User Experience (UX) Designer", "Product Manager", "Systems Analyst"]
      }
    }
  },
  "McMaster University": {
    "ec_quality": 4, "co-op": ["yes", "no"],
    "steps": [
        "<b>1. Apply on OUAC:</b> Deadline <b>January 15</b>.",
        "<b>2. Activate MacID:</b> Wait for email instructions.",
        "<b>3. Supplementary Application:</b> MANDATORY. Deadline <b>January 29</b>. Completed on Kira Talent.",
        "<b>4. Scholarship App:</b> Submit via AwardSpring if eligible."
    ],
    "programs": {
      "Integrated Biomedical Engineering & Health Sciences (iBioMed)": { 
          "recommended_average": [90, 95], 
          "required_courses": ["ENG4U", "MCV4U", "SBI4U", "SCH4U", "SPH4U", "One 4U/M"],
          "outcomes": ["Biomedical Engineer", "Medical Technology Innovator", "Health Systems Analyst"]
      },
      "Chemical Engineering ": { 
          "recommended_average": [87, 90], 
          "required_courses": ["ENG4U", "MCV4U", "SCH4U", "SPH4U"],
          "outcomes": ["Process Safety Engineer", "Biochemical Engineer", "Energy Analyst"]
      },
      "Civil Engineering ": { 
          "recommended_average": [87, 90], 
          "required_courses": ["ENG4U", "MCV4U", "SCH4U", "SPH4U"],
          "outcomes": ["Structural Engineer", "Municipal Engineer", "Project Coordinator"]
      },
      "Computer Engineering ": { 
          "recommended_average": [87, 90], 
          "required_courses": ["ENG4U", "MCV4U", "SCH4U", "SPH4U"],
          "outcomes": ["Embedded Software Engineer", "Hardware Developer", "Network Administrator"]
      },
      "Electrical Engineering": { 
          "recommended_average": [87, 90], 
          "required_courses": ["ENG4U", "MCV4U", "SCH4U", "SPH4U"],
          "outcomes": ["Power Distribution Engineer", "Control Systems Specialist", "Telecommunications Engineer"]
      },
      "Engineering Physics": { 
          "recommended_average": [87, 90], 
          "required_courses": ["ENG4U", "MCV4U", "SCH4U", "SPH4U"],
          "outcomes": ["Nuclear Engineer", "Photonics Researcher", "Quantum Computing Scientist"]
      },
      "Materials Engineering": { 
          "recommended_average": [87, 90], 
          "required_courses": ["ENG4U", "MCV4U", "SCH4U", "SPH4U"],
          "outcomes": ["Materials Scientist", "Corrosion Engineer", "Manufacturing Process Engineer"]
      },
      "Mechanical Engineering": { 
          "recommended_average": [87, 90], 
          "required_courses": ["ENG4U", "MCV4U", "SCH4U", "SPH4U"],
          "outcomes": ["Mechanical Design Engineer", "HVAC Engineer", "Automotive Specialist"]
      },
      "Mechatronics Engineering": { 
          "recommended_average": [87, 90], 
          "required_courses": ["ENG4U", "MCV4U", "SCH4U", "SPH4U"],
          "outcomes": ["Robotics Engineer", "Automation Engineer", "Control Systems Architect"]
      },
      "Software Engineering": { 
          "recommended_average": [87, 90], 
          "required_courses": ["ENG4U", "MCV4U", "SCH4U", "SPH4U"],
          "outcomes": ["Software Engineer", "Game Developer", "Cybersecurity Analyst"]
      },
      "Computer Science (B.A.Sc.)": { 
          "recommended_average": [92, 96], 
          "required_courses": ["ENG4U", "MCV4U", "Two of: SBI4U, SCH4U, SPH4U, SES4U, ICS4U or TEJ4M"],
          "outcomes": ["Data Scientist", "Software Developer", "Artificial Intelligence Researcher"]
      }
    }
  },
  "Western University": {
    "ec_quality": 3, "co-op": ["yes"],
    "steps": [
        "<b>1. Apply on OUAC:</b> Deadline <b>January 15</b>.",
        "<b>2. Activate Student Center:</b> Use your Western Student ID.",
        "<b>3. CONNECT Profile (Optional):</b> Highly recommended. Due <b>mid-February</b>.",
        "<b>4. English Proficiency:</b> Submit scores if required."
    ],
    "programs": {
      "Chemical Engineering": { 
          "recommended_average": [88, 93], 
          "required_courses": ["ENG4U", "MCV4U", "MHF4U", "SPH4U", "SCH4U", "One 4U/M"],
          "outcomes": ["Process Engineer", "Environmental Compliance Officer", "Biochemical Engineer"]
      },
      "Civil Engineering": { 
          "recommended_average": [88, 93], 
          "required_courses": ["ENG4U", "MCV4U", "MHF4U", "SPH4U", "SCH4U", "One 4U/M"],
          "outcomes": ["Structural Engineer", "Transportation Engineer", "Construction Manager"]
      },
      "Computer Engineering": { 
          "recommended_average": [88, 93], 
          "required_courses": ["ENG4U", "MCV4U", "MHF4U", "SPH4U", "SCH4U", "One 4U/M"],
          "outcomes": ["Software Engineer", "Embedded Systems Developer", "Network Architect"]
      },
      "Electrical Engineering": { 
          "recommended_average": [88, 93], 
          "required_courses": ["ENG4U", "MCV4U", "MHF4U", "SPH4U", "SCH4U", "One 4U/M"],
          "outcomes": ["Power Systems Engineer", "Control Systems Designer", "Electronics Engineer"]
      },
      "Integrated Engineering": { 
          "recommended_average": [88, 93], 
          "required_courses": ["ENG4U", "MCV4U", "MHF4U", "SPH4U", "SCH4U", "One 4U/M"],
          "outcomes": ["Engineering Project Manager", "Technical Consultant", "Business Analyst"]
      },
      "Mechanical Engineering": { 
          "recommended_average": [88, 93], 
          "required_courses": ["ENG4U", "MCV4U", "MHF4U", "SPH4U", "SCH4U", "One 4U/M"],
          "outcomes": ["Automotive Engineer", "Manufacturing Engineer", "Mechanical Designer"]
      },
      "Mechatronic Systems Engineering": { 
          "recommended_average": [88, 93], 
          "required_courses": ["ENG4U", "MCV4U", "MHF4U", "SPH4U", "SCH4U", "One 4U/M"],
          "outcomes": ["Robotics Engineer", "Automation Systems Integrator", "Control Systems Engineer"]
      },
      "Software Engineering": { 
          "recommended_average": [88, 93], 
          "required_courses": ["ENG4U", "MCV4U", "MHF4U", "SPH4U", "SCH4U", "One 4U/M"],
          "outcomes": ["Software Developer", "Cloud Solutions Architect", "App Developer"]
      },
      "Biomedical Engineering (Concurrent Degree)": { 
          "recommended_average": [88, 93], 
          "required_courses": ["ENG4U", "MCV4U", "MHF4U", "SPH4U", "SCH4U", "One 4U/M"],
          "outcomes": ["Biomedical Engineer", "Prosthetics Designer", "Medical Imaging Specialist"]
      },
      "Artificial Intelligence Systems Engineering (Concurrent Degree)": { 
          "recommended_average": [88, 93], 
          "required_courses": ["ENG4U", "MCV4U", "MHF4U", "SPH4U", "SCH4U", "One 4U/M"],
          "outcomes": ["AI Engineer", "Machine Learning Specialist", "Data Engineer"]
      }
    }
  },
  "University of Ottawa": {
    "ec_quality": 3, "co-op": ["yes", "no"],
    "steps": [
        "<b>1. Apply on OUAC:</b> Deadline <b>January 15</b>.",
        "<b>2. uoZone:</b> Log in to upload documents.",
        "<b>3. Declaration of Personal Experience (Optional):</b> Submit only if average is borderline."
    ],
    "programs": {
      "Biomedical Mechanical Engineering (BASc)": { 
          "recommended_average": [80, 85], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U", "SBI4U"],
          "outcomes": ["Biomedical Engineer", "Medical Device Manufacturer", "Biomechanical Researcher"]
      },
      "Chemical Engineering": { 
          "recommended_average": [80, 85], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U"],
          "outcomes": ["Process Engineer", "Environmental Engineer", "Materials Scientist"]
      },
      "Civil Engineering": { 
          "recommended_average": [80, 85], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U"],
          "outcomes": ["Civil Engineer", "Structural Designer", "Transportation Analyst"]
      },
      "Computer Engineering": { 
          "recommended_average": [80, 85], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U"],
          "outcomes": ["Computer Hardware Engineer", "Network Specialist", "Embedded Systems Designer"]
      },
      "Electrical Engineering": { 
          "recommended_average": [80, 85], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U"],
          "outcomes": ["Electrical Design Engineer", "Power Systems Analyst", "Telecommunications Engineer"]
      },
      "Mechanical Engineering": { 
          "recommended_average": [80, 85], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U"],
          "outcomes": ["Mechanical Engineer", "HVAC Specialist", "Automotive Designer"]
      },
      "Software Engineering": { 
          "recommended_average": [80, 85], 
          "required_courses": ["ENG4U", "MHF4U", "MCV4U", "One Science"],
          "outcomes": ["Software Engineer", "Web Developer", "System Architect"]
      }
    }
  },
  "Queens University": {
    "ec_quality": 3, "co-op": ["yes", "no"],
    "steps": [
        "<b>1. Apply on OUAC:</b> Deadline <b>January 15</b>.",
        "<b>2. SOLUS Student Center:</b> Activate NetID.",
        "<b>3. Major Admission Awards (Optional):</b> Deadline <b>December 8</b>. Requires essays.",
        "<b>4. Engineering Admission:</b> Grades-based. No supplementary essay for General Eng."
    ],
    "programs": {
      "Chemical Engineering": { "recommended_average": [87, 93], "required_courses": ["ENG4U", "MCV4U", "MHF4U", "SPH4U", "SCH4U"], "outcomes": ["Chemical Process Engineer", "Pharmaceutical Engineer", "Energy Consultant"] },
      "Civil Engineering": { "recommended_average": [87, 93], "required_courses": ["ENG4U", "MCV4U", "MHF4U", "SPH4U", "SCH4U"], "outcomes": ["Structural Engineer", "Geotechnical Engineer", "Construction Manager"] },
      "Computer Engineering": { "recommended_average": [87, 93], "required_courses": ["ENG4U", "MCV4U", "MHF4U", "SPH4U", "SCH4U"], "outcomes": ["Computer Hardware Engineer", "Software Developer", "Network Engineer"] },
      "Electrical Engineering": { "recommended_average": [87, 93], "required_courses": ["ENG4U", "MCV4U", "MHF4U", "SPH4U", "SCH4U"], "outcomes": ["Electrical Engineer", "Power Systems Controller", "Electronics Designer"] },
      "Engineering Chemistry": { "recommended_average": [87, 93], "required_courses": ["ENG4U", "MCV4U", "MHF4U", "SPH4U", "SCH4U"], "outcomes": ["Chemical Researcher", "Materials Scientist", "Process Control Engineer"] },
      "Engineering Physics": { "recommended_average": [87, 93], "required_courses": ["ENG4U", "MCV4U", "MHF4U", "SPH4U", "SCH4U"], "outcomes": ["Physicist", "Nuclear Engineer", "Optical Engineer"] },
      "Geological Engineering": { "recommended_average": [87, 93], "required_courses": ["ENG4U", "MCV4U", "MHF4U", "SPH4U", "SCH4U"], "outcomes": ["Geological Engineer", "Hydrogeologist", "Mining Consultant"] },
      "Mathematics and Engineering": { "recommended_average": [87, 93], "required_courses": ["ENG4U", "MCV4U", "MHF4U", "SPH4U", "SCH4U"], "outcomes": ["Control Systems Engineer", "Data Analyst", "Robotics Mathematician"] },
      "Mechanical Engineering": { "recommended_average": [87, 93], "required_courses": ["ENG4U", "MCV4U", "MHF4U", "SPH4U", "SCH4U"], "outcomes": ["Mechanical Engineer", "Aerospace Systems Designer", "Manufacturing Engineer"] },
      "Mechatronics and Robotics Engineering (Direct Entry)": { "recommended_average": [90, 95], "required_courses": ["ENG4U", "MCV4U", "MHF4U", "SPH4U", "SCH4U"], "outcomes": ["Robotics Engineer", "Automation Specialist", "Artificial Intelligence Engineer"] },
      "Mining Engineering": { "recommended_average": [87, 93], "required_courses": ["ENG4U", "MCV4U", "MHF4U", "SPH4U", "SCH4U"], "outcomes": ["Mining Engineer", "Mine Safety Officer", "Mineral Exploration Manager"] }
    }
  },
  "Carleton University": {
    "ec_quality": 2, "co-op": ["yes", "no"],
    "steps": [
        "<b>1. Apply on OUAC:</b> Deadline <b>January 15</b>.",
        "<b>2. Carleton 360:</b> Monitor application status.",
        "<b>3. Grades Based:</b> No mandatory supplementary app."
    ],
    "programs": {
      "Aerospace Engineering": { "recommended_average": [84, 88], "required_courses": ["ENG4U", "MHF4U", "SCH4U", "SPH4U", "MCV4U"], "outcomes": ["Aerospace Engineer", "Avionics Specialist", "Flight Systems Tester"] },
      "Civil Engineering": { "recommended_average": [78, 84], "required_courses": ["ENG4U", "MHF4U", "SCH4U", "SPH4U", "MCV4U"], "outcomes": ["Civil Engineer", "Urban Infrastructure Planner", "Structural Analyst"] },
      "Computer Systems Engineering": { "recommended_average": [80, 86], "required_courses": ["ENG4U", "MHF4U", "SCH4U", "SPH4U", "MCV4U"], "outcomes": ["Systems Engineer", "Real-time Systems Developer", "Robotics Integrator"] },
      "Mechanical Engineering": { "recommended_average": [80, 86], "required_courses": ["ENG4U", "MHF4U", "SCH4U", "SPH4U", "MCV4U"], "outcomes": ["Mechanical Engineer", "Product Designer", "Manufacturing Engineer"] },
      "Software Engineering": { "recommended_average": [82, 88], "required_courses": ["ENG4U", "MHF4U", "SCH4U", "SPH4U", "MCV4U"], "outcomes": ["Software Engineer", "Application Developer", "Cybersecurity Analyst"] }
    }
  },
  "University of Windsor": {
    "ec_quality": 2, "application_deadline": "Not specified", "co-op": ["yes"],
    "steps": [
        "<b>1. Apply on OUAC:</b> Deadline <b>January 15</b>.",
        "<b>2. UWindsor Student Portal:</b> Monitor for document requests.",
        "<b>3. Grades Based:</b> Admission based on Grade 12 top 6 average."
    ],
    "programs": {
      "Civil Engineering": { "recommended_average": [86, 89], "required_courses": ["ENG4U", "MHF4U", "SCH4U", "SPH4U"], "outcomes": ["Civil Engineer", "Construction Manager", "Traffic Engineer"] },
      "Electrical Engineering": { "recommended_average": [87, 90], "required_courses": ["ENG4U", "MHF4U", "SCH4U", "SPH4U"], "outcomes": ["Electrical Engineer", "Power Systems Engineer", "Control Systems Analyst"] },
      "Mechanical Engineering": { "recommended_average": [84, 87], "required_courses": ["ENG4U", "MHF4U", "SCH4U", "SPH4U"], "outcomes": ["Mechanical Engineer", "Automotive Systems Engineer", "Manufacturing Supervisor"] }
    }
  },
  "Ontario Tech University": {
    "ec_quality": 2, "application_deadline": "Not specified", "co-op": ["yes", "no"],
    "steps": [
        "<b>1. Apply on OUAC:</b> Deadline <b>January 15</b>.",
        "<b>2. Applicant Portal:</b> Check status.",
        "<b>3. Grades Based:</b> No mandatory supplementary application."
    ],
    "programs": {
      "Automotive Engineering": { "recommended_average": [70], "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SCH4U", "SPH4U"], "outcomes": ["Automotive Engineer", "Vehicle Dynamics Specialist", "Manufacturing Engineer"] },
      "Electrical Engineering": { "recommended_average": [70], "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SCH4U", "SPH4U"], "outcomes": ["Electrical Engineer", "Power Distribution Specialist", "Electronics Designer"] },
      "Mechanical Engineering": { "recommended_average": [70], "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SCH4U", "SPH4U"], "outcomes": ["Mechanical Engineer", "Product Design Engineer", "HVAC Specialist"] },
      "Software Engineering": { "recommended_average": [70], "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SCH4U", "SPH4U"], "outcomes": ["Software Developer", "Software Tester", "Systems Architect"] },
      "Nuclear Engineering": { "recommended_average": [70], "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SCH4U", "SPH4U"], "outcomes": ["Nuclear Engineer", "Radiation Safety Officer", "Energy Systems Analyst"] }
    }
  },
  "Toronto Metropolitan University": {
    "ec_quality": 2, "application_deadline": "Not specified", "co-op": ["yes"],
    "steps": [
        "<b>1. Apply on OUAC:</b> Deadline <b>January 15</b>.",
        "<b>2. ChooseTMU Portal:</b> Track documents.",
        "<b>3. Supplementary Form (Optional):</b> Recommended for special circumstances."
    ],
    "programs": {
      "Aerospace Engineering": { "recommended_average": [80], "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U"], "outcomes": ["Aerospace Engineer", "Aircraft Maintenance Engineer", "Avionics Technician"] },
      "Biomedical Engineering": { "recommended_average": [80], "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U"], "outcomes": ["Biomedical Engineer", "Clinical Technologist", "Medical Researcher"] },
      "Chemical Engineering": { "recommended_average": [80], "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U"], "outcomes": ["Chemical Engineer", "Process Safety Specialist", "Environmental Analyst"] },
      "Civil Engineering": { "recommended_average": [80], "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U"], "outcomes": ["Civil Engineer", "Structural Engineer", "Project Manager"] },
      "Computer Engineering": { "recommended_average": [80], "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U"], "outcomes": ["Computer Engineer", "Hardware Designer", "Network Administrator"] },
      "Electrical Engineering": { "recommended_average": [80], "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U"], "outcomes": ["Electrical Engineer", "Power Systems Engineer", "Telecommunications Specialist"] },
      "Mechanical Engineering": { "recommended_average": [80], "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SPH4U", "SCH4U"], "outcomes": ["Mechanical Engineer", "Manufacturing Engineer", "Thermal Systems Designer"] }
    }
  },
  "York University": {
    "ec_quality": 3, "application_deadline": "Not specified", "co-op": ["yes"],
    "steps": [
        "<b>1. Apply on OUAC:</b> Deadline <b>January 15</b>.",
        "<b>2. MyFile Portal:</b> Track application status.",
        "<b>3. Lassonde Boost (Optional):</b> Supplementary video interview. Deadline <b>April 2</b>."
    ],
    "programs": {
      "Civil Engineering": { "recommended_average": [88], "required_courses": ["ENG4U", "SCH4U", "SPH4U", "MHF4U", "MCV4U", "One 4U/M"], "outcomes": ["Civil Engineer", "Structural Designer", "Transportation Planner"] },
      "Computer Engineering": { "recommended_average": [83], "required_courses": ["ENG4U", "SCH4U", "SPH4U", "MHF4U", "MCV4U", "One 4U/M"], "outcomes": ["Computer Engineer", "Hardware Developer", "Systems Analyst"] },
      "Electrical Engineering": { "recommended_average": [83], "required_courses": ["ENG4U", "SCH4U", "SPH4U", "MHF4U", "MCV4U", "One 4U/M"], "outcomes": ["Electrical Engineer", "Power Grid Specialist", "Electronics Engineer"] },
      "Mechanical Engineering": { "recommended_average": [83], "required_courses": ["ENG4U", "SCH4U", "SPH4U", "MHF4U", "MCV4U", "One 4U/M"], "outcomes": ["Mechanical Engineer", "Automotive Designer", "Manufacturing Specialist"] },
      "Software Engineering": { "recommended_average": [82], "required_courses": ["ENG4U", "SCH4U", "SPH4U", "MHF4U", "MCV4U", "One 4U/M"], "outcomes": ["Software Developer", "Web Application Architect", "Quality Assurance Engineer"] },
      "Space Engineering": { "recommended_average": [82], "required_courses": ["ENG4U", "SCH4U", "SPH4U", "MHF4U", "MCV4U", "One 4U/M"], "outcomes": ["Space Systems Engineer", "Satellite Communications Specialist", "Mission Control Analyst"] }
    }
  },
  "University of Guelph": {
    "ec_quality": 3, "application_deadline": "Not specified", "co-op": ["yes", "no"],
    "steps": [
        "<b>1. Apply on OUAC:</b> Deadline <b>January 15</b>.",
        "<b>2. Student Profile Form (SPF) (Optional):</b> Recommended if average is borderline. Deadline <b>April 1</b>."
    ],
    "programs": {
      "Biological Engineering": { "co-op": ["yes"], "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SCH4U", "SPH4U", "One 4U/M"], "outcomes": ["Biomedical Engineer", "Food Process Engineer", "Biotech Researcher"] },
      "Biomedical Engineering": { "co-op": ["yes"], "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SCH4U", "SPH4U", "One 4U/M"], "outcomes": ["Medical Device Engineer", "Clinical Engineer", "Rehabilitation Engineer"] },
      "Civil Engineering": { "co-op": ["no"], "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SCH4U", "SPH4U", "One 4U/M"], "outcomes": ["Civil Engineer", "Structural Analyst", "Water Resources Engineer"] },
      "Computer Engineering": { "co-op": ["yes"], "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SCH4U", "SPH4U", "One 4U/M"], "outcomes": ["Computer Hardware Engineer", "Software Developer", "Network Engineer"] },
      "Environmental Engineering": { "co-op": ["yes"], "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SCH4U", "SPH4U", "One 4U/M"], "outcomes": ["Environmental Engineer", "Pollution Control Specialist", "Sustainability Consultant"] },
      "Mechanical Engineering": { "co-op": ["yes"], "required_courses": ["ENG4U", "MHF4U", "MCV4U", "SCH4U", "SPH4U", "One 4U/M"], "outcomes": ["Mechanical Engineer", "Manufacturing Supervisor", "Energy Systems Engineer"] }
    }
  }
}

# 2. Setup PDF
pdf_filename = "University_Engineering_Programs.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=LETTER)
styles = getSampleStyleSheet()
story = []

# Custom Styles
title_style = ParagraphStyle(
    'Title', parent=styles['Heading1'], alignment=1, fontSize=18, spaceAfter=20
)
uni_header_style = ParagraphStyle(
    'UniHeader', parent=styles['Heading2'], fontSize=16, spaceBefore=15, spaceAfter=10, textColor=colors.darkblue
)
prog_header_style = ParagraphStyle(
    'ProgHeader', parent=styles['Heading3'], fontSize=14, spaceBefore=10, spaceAfter=5, textColor=colors.black
)
normal_style = styles['Normal']
bullet_style = ParagraphStyle(
    'Bullet', parent=normal_style, leftIndent=20, bulletIndent=10, spaceAfter=2
)
step_header_style = ParagraphStyle(
    'StepHeader', parent=styles['Heading4'], fontSize=12, spaceBefore=5, spaceAfter=5, textColor=colors.darkgreen
)

# 3. Build Content
story.append(Paragraph("Ontario University Engineering Programs Data", title_style))
story.append(Paragraph("This document contains key processes, averages, requirements, and career outcomes.", normal_style))
story.append(Spacer(1, 20))

for uni_name, uni_data in data.items():
    if uni_name == "_id" or uni_name == "apply_deadline":
        continue
        
    # University Header
    story.append(Paragraph(uni_name, uni_header_style))
    
    # Global Uni Info (Co-op, Rating)
    global_info = []
    if "apply_deadline" in data:
        global_info.append(f"<b>Application Deadline:</b> {data['apply_deadline']}")
        
    if "co-op" in uni_data:
        coop_status = ", ".join(uni_data['co-op'])
        global_info.append(f"<b>Co-op Available:</b> {coop_status}")
    
    if "ec_quality" in uni_data:
         global_info.append(f"<b>Extracurricular Quality Rating:</b> {uni_data['ec_quality']}/5")

    for info in global_info:
        story.append(Paragraph(info, normal_style))
    
    # --- Steps to Apply ---
    if "steps" in uni_data:
        story.append(Spacer(1, 5))
        story.append(Paragraph("Steps to Apply:", step_header_style))
        for step in uni_data["steps"]:
             story.append(Paragraph(step, bullet_style))
    # ----------------------

    story.append(Spacer(1, 10))
    
    # Programs
    programs = uni_data.get("programs", {})
    for prog_name, prog_details in programs.items():
        story.append(Paragraph(prog_name, prog_header_style))
        
        # Averages
        avg = prog_details.get("recommended_average", "N/A")
        if isinstance(avg, list):
            avg_str = f"{avg[0]}% - {avg[1]}%" if len(avg) > 1 else f"{avg[0]}%"
        else:
            avg_str = str(avg)
        story.append(Paragraph(f"<b>Recommended Average:</b> {avg_str}", normal_style))
        
        # Required Courses
        reqs = prog_details.get("required_courses", [])
        if reqs:
            story.append(Paragraph("<b>Required Courses:</b>", normal_style))
            for req in reqs:
                story.append(Paragraph(f"• {req}", bullet_style))
        
        # Key Interests
        interests = prog_details.get("interests", [])
        if interests:
            story.append(Paragraph("<b>Key Areas of Study:</b>", normal_style))
            for interest in interests:
                story.append(Paragraph(f"• {interest}", bullet_style))

        # --- NEW: CAREER OUTCOMES ---
        outcomes = prog_details.get("outcomes", [])
        if outcomes:
            story.append(Paragraph("<b>Top 3 Career Outcomes:</b>", normal_style))
            for outcome in outcomes:
                story.append(Paragraph(f"• {outcome}", bullet_style))
        # ----------------------------
        
        # Notes
        notes = prog_details.get("notes")
        if notes:
             story.append(Paragraph(f"<b>Notes:</b> {notes}", normal_style))
             
        story.append(Spacer(1, 10))
        
    story.append(PageBreak())

# 4. Generate
doc.build(story)
print(f"PDF generated: {pdf_filename}")