# src/bps_data.py
# Curated Boston Public Schools source data for the 6.C395 chatbot
# Last updated: 2026-03-13
#
# Design notes:
# - Keep only facts you can support from official BPS pages.
# - Every record includes source URLs.
# - Prefer concise, retrieval-friendly fields over long prose.
# - When details may change year to year (deadlines, sessions, contact info),
#   keep the source URL and optionally a "last_verified" field.

DISTRICT_SOURCES = {
    "registration": "https://www.bostonpublicschools.org/enrollment/welcome-services/registration",
    "welcome_centers": "https://www.bostonpublicschools.org/enrollment/welcome-services/welcome-centers-locations",
    "faq": "https://www.bostonpublicschools.org/enrollment/welcome-services/faq",
    "kindergarten": "https://www.bostonpublicschools.org/enrollment/welcome-services/grade-levels-overview/kindergarten",
    "great_starts": "https://www.bostonpublicschools.org/enrollment/greatstarts-container/greatstarts",
    "school_listings": "https://www.bostonpublicschools.org/schools-container/schools-listings",
    "school_types": "https://www.bostonpublicschools.org/schools-container/school-types",
    "high_schools": "https://www.bostonpublicschools.org/enrollment/welcome-services/grade-levels-overview/high-schools",
    "school_info_sessions": "https://www.bostonpublicschools.org/enrollment/welcome-services/school-information-sessions",
    "sei_language_specific": "https://www.bostonpublicschools.org/bps-departments/multilingual-and-multicultural-education/instructional-programs/sheltered-english-immersion-sei/sei-language-specific-program",
    "child_find": "https://www.bostonpublicschools.org/academics/specialized-services/programs-services/child-find",
    "early_childhood": "https://www.bostonpublicschools.org/students-families/early-childhood",
    "boston_prek_apply": "https://www.bostonpublicschools.org/students-families/universal-pre-k-boston/apply",
}

DISTRICT_FACTS = [
    {
        "id": "home_based_assignment",
        "topic": "assignment",
        "fact": (
            "BPS uses a home-based assignment plan to determine the schools available "
            "to a family based on the student's home address."
        ),
        "notes": (
            "If a school does not appear on the family's list, the student is not eligible "
            "to apply to that school."
        ),
        "last_verified": "2026-03-13",
        "sources": [
            DISTRICT_SOURCES["registration"],
        ],
    },
    {
        "id": "high_schools_citywide",
        "topic": "assignment",
        "fact": "All BPS high schools are citywide options for students living in Boston.",
        "notes": "Some schools may still have special admission requirements.",
        "last_verified": "2026-03-13",
        "sources": [
            DISTRICT_SOURCES["registration"],
            DISTRICT_SOURCES["high_schools"],
        ],
    },
    {
        "id": "registration_methods",
        "topic": "registration",
        "fact": "Families can register online or at a BPS Welcome Center.",
        "notes": None,
        "last_verified": "2026-03-13",
        "sources": [
            DISTRICT_SOURCES["registration"],
            DISTRICT_SOURCES["welcome_centers"],
        ],
    },
    {
        "id": "priority_registration_2026_2027",
        "topic": "registration_timing",
        "fact": (
            "For the 2026-2027 school year, registration for students entering K0, K1, K2, "
            "Grade 6, Grade 7, and Grade 9 runs from January 5, 2026 through February 6, 2026. "
            "Registration for all other grades opens February 9, 2026."
        ),
        "notes": "This is time-sensitive and should be treated as a year-specific fact.",
        "last_verified": "2026-03-13",
        "sources": [
            DISTRICT_SOURCES["welcome_centers"],
        ],
    },
    {
        "id": "great_starts_platform",
        "topic": "school_search",
        "fact": (
            "Great Starts is a citywide enrollment platform that helps families explore "
            "childcare, preschool, and Boston Public Schools options."
        ),
        "notes": "Useful as an official next step when the chatbot cannot fully resolve eligibility.",
        "last_verified": "2026-03-13",
        "sources": [
            DISTRICT_SOURCES["great_starts"],
        ],
    },
]

GRADE_RULES = [
    {
        "id": "k0_age_2026_2027",
        "grade": "K0",
        "rule_type": "age_cutoff",
        "fact": "Children must be 3 years old on or before September 1, 2026 to register for K0.",
        "last_verified": "2026-03-13",
        "sources": [DISTRICT_SOURCES["registration"]],
    },
    {
        "id": "k1_age_2026_2027",
        "grade": "K1",
        "rule_type": "age_cutoff",
        "fact": "Children must be 4 years old on or before September 1, 2026 to register for K1.",
        "last_verified": "2026-03-13",
        "sources": [DISTRICT_SOURCES["registration"]],
    },
    {
        "id": "k2_age_2026_2027",
        "grade": "K2",
        "rule_type": "age_cutoff",
        "fact": "Children must be 5 years old on or before September 1, 2026 to register for K2.",
        "last_verified": "2026-03-13",
        "sources": [DISTRICT_SOURCES["registration"]],
    },
    {
        "id": "k2_full_day",
        "grade": "K2",
        "rule_type": "program_structure",
        "fact": "K2 is a six-hour full-day program for 5-year-olds.",
        "notes": "BPS says K2 is provided in all BPS elementary schools and early learning centers.",
        "last_verified": "2026-03-13",
        "sources": [DISTRICT_SOURCES["kindergarten"]],
    },
    {
        "id": "k2_assignment_guarantee",
        "grade": "K2",
        "rule_type": "assignment",
        "fact": "A K2 assignment is guaranteed for children who apply for K2.",
        "notes": "A specific school assignment is not guaranteed.",
        "last_verified": "2026-03-13",
        "sources": [DISTRICT_SOURCES["kindergarten"]],
    },
    {
        "id": "k0_k1_not_guaranteed",
        "grade": "K0_K1",
        "rule_type": "assignment",
        "fact": "BPS does not guarantee a pre-K assignment for every child who applies to K0 or K1.",
        "notes": (
            "The FAQ states K0 classrooms are much more limited, and most K0 seats are reserved "
            "for students with disabilities."
        ),
        "last_verified": "2026-03-13",
        "sources": [
            DISTRICT_SOURCES["faq"],
        ],
    },
    {
        "id": "school_info_sessions_k0_marker",
        "grade": "K0",
        "rule_type": "notation",
        "fact": (
            "In BPS school information session materials, K0* means K0 is available only "
            "for students with disabilities at that school."
        ),
        "last_verified": "2026-03-13",
        "sources": [
            DISTRICT_SOURCES["school_info_sessions"],
        ],
    },
]

PROGRAM_RULES = [
    {
        "id": "dual_language_entry_points",
        "program_type": "dual_language",
        "fact": (
            "For dual language / two-way immersion programs, program entry grade levels are "
            "K1 to 2 and 9 to 11."
        ),
        "notes": (
            "Students entering grades 3 through 8 must be assessed by the school in the partner "
            "language to enter the program."
        ),
        "last_verified": "2026-03-13",
        "sources": [
            DISTRICT_SOURCES["school_types"],
        ],
    },
    {
        "id": "child_find_ages",
        "program_type": "special_education",
        "fact": (
            "BPS conducts Child Find for students ages 3 through 21 who live in Boston or attend "
            "school in Boston, including students in private school or home-school settings."
        ),
        "last_verified": "2026-03-13",
        "sources": [
            DISTRICT_SOURCES["child_find"],
        ],
    },
    {
        "id": "boston_prek_eligibility",
        "program_type": "early_childhood",
        "fact": (
            "A child is eligible for Boston Pre-K if they are 3 or 4 years old by September 1 "
            "of the school year they are applying to and are a resident of the City of Boston."
        ),
        "last_verified": "2026-03-13",
        "sources": [
            DISTRICT_SOURCES["boston_prek_apply"],
        ],
    },
]

# These school records are intentionally a SMALL, high-confidence starter set.
# Add more schools only when you can verify them on official BPS profile pages.
SCHOOL_RECORDS = [
    {
        "name": "East Boston Early Education Center",
        "school_type": ["early_education"],
        "neighborhood": "East Boston",
        "grades_served_text": None,
        "program_tags": ["early_childhood"],
        "language_programs": [],
        "special_features": [
            "Early education setting",
        ],
        "notes": (
            "School profile emphasizes a nurturing environment and strong partnership among "
            "teachers, staff, and families."
        ),
        "last_verified": "2026-03-13",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/east-boston-early-education-center",
        ],
    },
    {
        "name": "Henderson, Dr. William W. Inclusion School",
        "school_type": ["inclusion"],
        "neighborhood": None,
        "grades_served_text": "early childhood through Grade 12 and Transition",
        "program_tags": ["inclusion", "special_education"],
        "language_programs": [],
        "special_features": [
            "Inclusion school",
            "Serves students through transition",
        ],
        "notes": (
            "The school profile says the Henderson Inclusion School serves children from early "
            "childhood through Grade 12 and Transition."
        ),
        "last_verified": "2026-03-13",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/henderson-dr-william-w-inclusion-school",
        ],
    },
    {
        "name": "Josiah Quincy Upper School",
        "school_type": ["upper_school", "IB"],
        "neighborhood": "Chinatown / Downtown Boston",
        "grades_served_text": None,
        "program_tags": ["IB", "bilingual"],
        "language_programs": ["one-way Chinese bilingual"],
        "special_features": [
            "International Baccalaureate",
            "Guaranteed K-12 pathway referenced on school profile",
        ],
        "notes": (
            "The school profile states that both the elementary and upper school are accredited "
            "IB schools and that the school offers a one-way Chinese bilingual program for "
            "families who speak Chinese at home."
        ),
        "last_verified": "2026-03-13",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/quincy-upper-school",
        ],
    },
    {
        "name": "Muñiz, Margarita Academy",
        "school_type": ["dual_language", "high_school"],
        "neighborhood": None,
        "grades_served_text": "Grades 7-12",
        "program_tags": ["dual_language", "early_college"],
        "language_programs": ["dual language"],
        "special_features": [
            "Early College starting in Grade 10",
        ],
        "notes": (
            "The school profile describes Muñiz as a dual language high school serving grades 7-12."
        ),
        "last_verified": "2026-03-13",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/muniz-margarita-academy",
        ],
    },
    {
        "name": "West Zone Early Learning Center",
        "school_type": ["early_education", "inclusion"],
        "neighborhood": None,
        "grades_served_text": None,
        "program_tags": ["early_childhood", "special_education", "ESL"],
        "language_programs": [],
        "special_features": [
            "Integrated early childhood classrooms for students with disabilities",
            "ESL services",
        ],
        "notes": (
            "The school profile says the school offers integrated early childhood classrooms "
            "for students with disabilities and provides ESL services."
        ),
        "last_verified": "2026-03-13",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/west-zone-early-learning-center",
        ],
    },
]

# Optional: language-specific SEI examples from an official BPS page.
# This is useful if you want the chatbot to answer questions like:
# "Are there schools with Haitian Creole SEI?"
SEI_LANGUAGE_SPECIFIC_EXAMPLES = [
    {
        "language": "Chinese",
        "schools": ["Harvard/Kent Elementary", "Quincy Elementary", "Charlestown High School"],
        "last_verified": "2026-03-13",
        "sources": [DISTRICT_SOURCES["sei_language_specific"]],
    },
    {
        "language": "Cape Verdean Creole",
        "schools": ["Burke High School", "Dearborn 6-12 STEM Academy", "Orchard Gardens K-8 School"],
        "last_verified": "2026-03-13",
        "sources": [DISTRICT_SOURCES["sei_language_specific"]],
    },
    {
        "language": "Haitian Creole",
        "schools": [
            "Community Academy of Science and Health",
            "Mattapan EES",
            "Taylor Elementary",
            "TechBoston Academy 6-12",
        ],
        "last_verified": "2026-03-13",
        "sources": [DISTRICT_SOURCES["sei_language_specific"]],
    },
]