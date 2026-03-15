# src/bps_data_v2.py
# Curated Boston Public Schools source data for the 6.C395 chatbot
# Last updated: 2026-03-14
#
# Design notes:
# - Keep only facts you can support from official BPS pages, NCES, Wikipedia, or
#   official school websites.
# - Every record includes source URLs.
# - Prefer concise, retrieval-friendly fields over long prose.
# - When details may change year to year (deadlines, sessions, contact info),
#   keep the source URL and optionally a "last_verified" field.
# - SCHOOL_RECORDS now covers all 134 sites in the 2024-2025 BPS portfolio,
#   sourced systematically from bostonpublicschools.org, NCES CCD, Wikipedia,
#   and individual school sites.

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
    "exam_schools": "https://www.bostonpublicschools.org/academics/exam-schools",
    "pilot_schools": "https://www.bostonpublicschools.org/schools-container/school-types",
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
        "last_verified": "2026-03-14",
        "sources": [
            DISTRICT_SOURCES["registration"],
        ],
    },
    {
        "id": "high_schools_citywide",
        "topic": "assignment",
        "fact": "All BPS high schools are citywide options for students living in Boston.",
        "notes": "Some schools may still have special admission requirements.",
        "last_verified": "2026-03-14",
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
        "last_verified": "2026-03-14",
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
        "last_verified": "2026-03-14",
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
        "last_verified": "2026-03-14",
        "sources": [
            DISTRICT_SOURCES["great_starts"],
        ],
    },
    {
        "id": "school_types_portfolio",
        "topic": "school_types",
        "fact": (
            "The BPS portfolio includes traditional district schools, exam schools, pilot schools, "
            "Horace Mann charter schools (in-district charters), innovation schools, international "
            "baccalaureate programs, and dual language schools."
        ),
        "notes": "As of 2022-2023, BPS reported 119 schools in its portfolio.",
        "last_verified": "2026-03-14",
        "sources": [
            DISTRICT_SOURCES["school_types"],
        ],
    },
    {
        "id": "pilot_school_autonomy",
        "topic": "school_types",
        "fact": (
            "BPS pilot schools have autonomy over budget, staffing, governance, "
            "curriculum/assessment, and school calendar. They were created in 1994 "
            "as a partnership between the district, school committee, superintendent, "
            "and Boston Teachers Union."
        ),
        "notes": "There are approximately 19 pilot schools in the BPS portfolio.",
        "last_verified": "2026-03-14",
        "sources": [
            DISTRICT_SOURCES["pilot_schools"],
        ],
    },
    {
        "id": "horace_mann_charters",
        "topic": "school_types",
        "fact": (
            "Horace Mann Charter Schools are innovative, semi-autonomous in-district charter "
            "schools approved by both the Boston School Committee and DESE and funded by BPS."
        ),
        "notes": "BPS has six Horace Mann Charter Schools including Edward M. Kennedy Academy for Health Careers.",
        "last_verified": "2026-03-14",
        "sources": [
            DISTRICT_SOURCES["school_types"],
        ],
    },
]

GRADE_RULES = [
    {
        "id": "k0_age_2026_2027",
        "grade": "K0",
        "rule_type": "age_cutoff",
        "fact": "Children must be 3 years old on or before September 1, 2026 to register for K0.",
        "last_verified": "2026-03-14",
        "sources": [DISTRICT_SOURCES["registration"]],
    },
    {
        "id": "k1_age_2026_2027",
        "grade": "K1",
        "rule_type": "age_cutoff",
        "fact": "Children must be 4 years old on or before September 1, 2026 to register for K1.",
        "last_verified": "2026-03-14",
        "sources": [DISTRICT_SOURCES["registration"]],
    },
    {
        "id": "k2_age_2026_2027",
        "grade": "K2",
        "rule_type": "age_cutoff",
        "fact": "Children must be 5 years old on or before September 1, 2026 to register for K2.",
        "last_verified": "2026-03-14",
        "sources": [DISTRICT_SOURCES["registration"]],
    },
    {
        "id": "k2_full_day",
        "grade": "K2",
        "rule_type": "program_structure",
        "fact": "K2 is a six-hour full-day program for 5-year-olds.",
        "notes": "BPS says K2 is provided in all BPS elementary schools and early learning centers.",
        "last_verified": "2026-03-14",
        "sources": [DISTRICT_SOURCES["kindergarten"]],
    },
    {
        "id": "k2_assignment_guarantee",
        "grade": "K2",
        "rule_type": "assignment",
        "fact": "A K2 assignment is guaranteed for children who apply for K2.",
        "notes": "A specific school assignment is not guaranteed.",
        "last_verified": "2026-03-14",
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
        "last_verified": "2026-03-14",
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
        "last_verified": "2026-03-14",
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
        "last_verified": "2026-03-14",
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
        "last_verified": "2026-03-14",
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
        "last_verified": "2026-03-14",
        "sources": [
            DISTRICT_SOURCES["boston_prek_apply"],
        ],
    },
    {
        "id": "exam_school_eligibility",
        "program_type": "exam",
        "fact": (
            "Students in grades 6, 8, or 9 who reside in Boston may apply to one of three BPS exam "
            "schools: Boston Latin School, Boston Latin Academy, and John D. O'Bryant School of "
            "Mathematics and Science. Admission is based on MAP Growth test scores and GPA (minimum B average)."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            DISTRICT_SOURCES["exam_schools"],
        ],
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# SCHOOL_RECORDS
# All 134 sites from the public_schools CSV, enriched with program data.
# Sources: bostonpublicschools.org, NCES CCD, Wikipedia BPS article,
#          individual school websites, Niche, GreatSchools, SchoolDigger.
# "grades_served_text" uses the canonical BPS/NCES grade span.
# "school_type" uses BPS taxonomy: traditional, exam, pilot, horace_mann_charter,
#   innovation, early_education, inclusion, alternative, adult, dual_language.
# ─────────────────────────────────────────────────────────────────────────────

SCHOOL_RECORDS = [

    # ── EAST BOSTON ────────────────────────────────────────────────────────

    {
        "name": "Guild Elementary",
        "address": "195 Leyden Street",
        "neighborhood": "East Boston",
        "zipcode": "02128",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [
            "MCAS School of Recognition (prior year)",
            "Community emphasis on diversity and high expectations",
        ],
        "notes": (
            "Neighborhood elementary serving East Boston. Approximately 247 students. "
            "School profile emphasizes diversity, high expectations, and belief that all "
            "students can achieve academic success."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/guild-elementary",
            "https://curtisguildelementary.org/",
            "https://www.niche.com/k12/curtis-guild-elementary-school-east-boston-ma/",
        ],
    },
    {
        "name": "Kennedy Patrick Elem",
        "address": "343 Saratoga Street",
        "neighborhood": "East Boston",
        "zipcode": "02128",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [
            "Named 2024-2025 DESE School of Recognition",
        ],
        "notes": (
            "Neighborhood elementary serving East Boston. Approximately 267 students. "
            "Recognized by DESE as a School of Recognition in 2024-2025 for strong "
            "achievement and growth on MCAS."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/kennedy-patrick-j-elementary",
            "https://www.niche.com/k12/kennedy-patrick-j-elementary-school-east-boston-ma/",
        ],
    },
    {
        "name": "Otis Elementary",
        "address": "218 Marion Street",
        "neighborhood": "East Boston",
        "zipcode": "02128",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": (
            "Neighborhood elementary in East Boston. One of the better-performing "
            "elementary schools in the East Boston cluster."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/otis-elementary",
        ],
    },
    {
        "name": "O'Donnell Elementary",
        "address": "33 Trenton Street",
        "neighborhood": "East Boston",
        "zipcode": "02128",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": (
            "Neighborhood elementary in East Boston. Approximately 275 students."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/odonnell-elementary",
        ],
    },
    {
        "name": "East Boston High",
        "address": "86 White Street",
        "neighborhood": "East Boston",
        "zipcode": "02128",
        "school_type": ["traditional"],
        "grades_served_text": "9-12",
        "program_tags": [],
        "language_programs": [],
        "special_features": [
            "Citywide high school",
            "Career and Technical Education pathways",
        ],
        "notes": (
            "Comprehensive neighborhood high school serving East Boston. Offers CTE "
            "pathways. All BPS high schools are citywide options."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/east-boston-high-school",
        ],
    },
    {
        "name": "Umana/Alighieri K-8",
        "address": "312 Border Street",
        "neighborhood": "East Boston",
        "zipcode": "02128",
        "school_type": ["traditional"],
        "grades_served_text": "PK-8",
        "program_tags": [],
        "language_programs": [],
        "special_features": [
            "Special Olympics National Banner School 2024-2025",
            "Piano Lab",
            "Inclusive sports and activities program",
        ],
        "notes": (
            "Mario Umana Academy (also known as Umana/Alighieri K-8) serves PK-8 in "
            "East Boston with approximately 632 students. Named a Special Olympics "
            "National Banner Unified Champion School for 2024-2025."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/mario-umana-academy",
            "https://www.niche.com/k12/mario-umana-academy-east-boston-ma/",
        ],
    },
    {
        "name": "East Boston EEC",
        "address": "135 Gove Street",
        "neighborhood": "East Boston",
        "zipcode": "02128",
        "school_type": ["early_education"],
        "grades_served_text": "K0-K1",
        "program_tags": ["early_childhood"],
        "language_programs": [],
        "special_features": [
            "Early education setting for ages 3-4",
        ],
        "notes": (
            "East Boston Early Education Center provides pre-K programming (K0/K1) for "
            "children ages 3-4 in East Boston. School profile emphasizes a nurturing "
            "environment and strong family-school partnership."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/east-boston-early-education-center",
        ],
    },
    {
        "name": "McKay K-8",
        "address": "122 Cottage Street",
        "neighborhood": "East Boston",
        "zipcode": "02128",
        "school_type": ["traditional"],
        "grades_served_text": "PK-8",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": (
            "Donald McKay K-8 School serves approximately 670 students in East Boston. "
            "One of the larger K-8 schools in the district."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/mckay-k-8",
            "https://www.niche.com/k12/mckay-k-8-school-east-boston-ma/",
        ],
    },
    {
        "name": "Adams Elementary",
        "address": "165 Webster Street",
        "neighborhood": "East Boston",
        "zipcode": "02128",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": (
            "Neighborhood elementary school in East Boston."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/adams-elementary",
        ],
    },
    {
        "name": "Bradley Elementary",
        "address": "110 Beachview Road",
        "neighborhood": "East Boston",
        "zipcode": "02128",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [
            "Among highest-performing elementary schools in East Boston cluster",
        ],
        "notes": (
            "Bradley Elementary is among the top-performing public elementary schools "
            "in East Boston, with approximately 60% of students at or above proficiency "
            "in ELA per 2024-2025 MCAS data."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/bradley-elementary",
            "https://www.schooldigger.com/go/MA/schools/0279000032/school.aspx",
        ],
    },
    {
        "name": "Alighieri Montessori",
        "address": "37 Gove St.",
        "neighborhood": "East Boston",
        "zipcode": "02128",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": ["montessori"],
        "language_programs": [],
        "special_features": [
            "Montessori program",
        ],
        "notes": (
            "The Alighieri Montessori School offers a Montessori-model curriculum to "
            "elementary-aged students in East Boston."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/alighieri-montessori",
        ],
    },

    # ── CHARLESTOWN ────────────────────────────────────────────────────────

    {
        "name": "Harvard/Kent Elem",
        "address": "50 Bunker Hill Street",
        "neighborhood": "Charlestown",
        "zipcode": "02129",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": ["Chinese SEI"],
        "special_features": [
            "Chinese Sheltered English Immersion (SEI) language-specific program",
        ],
        "notes": (
            "Harvard/Kent Elementary in Charlestown hosts a Chinese SEI language-specific "
            "program, one of a small number of BPS schools offering Chinese-language SEI."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/harvardkent-elementary",
            DISTRICT_SOURCES["sei_language_specific"],
        ],
    },
    {
        "name": "Charlestown High",
        "address": "240 Medford Street",
        "neighborhood": "Charlestown",
        "zipcode": "02129",
        "school_type": ["traditional"],
        "grades_served_text": "9-12",
        "program_tags": [],
        "language_programs": ["Chinese SEI"],
        "special_features": [
            "Citywide high school",
            "Chinese SEI language-specific program",
            "Absorbed Edwards Middle School 7th-8th grade in 2022",
        ],
        "notes": (
            "Charlestown High School serves grades 9-12 and hosts a Chinese SEI "
            "language-specific program. Following the closure of the Clarence R. Edwards "
            "Middle School in 2021, Charlestown High absorbed those middle school grades."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/charlestown-high-school",
            DISTRICT_SOURCES["sei_language_specific"],
        ],
    },
    {
        "name": "Edwards Middle",
        "address": "28 Walker Street",
        "neighborhood": "Charlestown",
        "zipcode": "02129",
        "school_type": ["traditional"],
        "grades_served_text": "6-8",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": (
            "Edwards Middle School (formerly Clarence R. Edwards) in Charlestown. "
            "Note: Wikipedia indicates the original Edwards school was closed in 2021 "
            "with grades merged into Charlestown High; verify current operating status."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/edwards-middle",
        ],
    },
    {
        "name": "Warren/Prescott",
        "address": "50 School Street",
        "neighborhood": "Charlestown",
        "zipcode": "02129",
        "school_type": ["traditional"],
        "grades_served_text": "K-8",
        "program_tags": [],
        "language_programs": [],
        "special_features": [
            "Special Olympics National Banner School 2024-2025",
        ],
        "notes": (
            "Warren-Prescott K-8 School in Charlestown was named a Special Olympics "
            "National Banner Unified Champion School for 2024-2025, recognizing "
            "inclusive sports and activities for students with and without disabilities."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/warrenprescott",
        ],
    },

    # ── DOWNTOWN / CHINATOWN / BACK BAY ────────────────────────────────────

    {
        "name": "Eliot K-8",
        "address": "16 Charter Street",
        "neighborhood": "North End / Downtown",
        "zipcode": "02113",
        "school_type": ["traditional"],
        "grades_served_text": "K-8",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": (
            "Eliot K-8 School is a neighborhood school in Boston's North End/Downtown area. "
            "Note: The CSV also lists a second Eliot K-8 entry at 585 Commercial Street, "
            "suggesting a building change or administrative listing; the Charter Street "
            "address is the primary campus."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/eliot-k-8",
        ],
    },
    {
        "name": "Quincy Upper School",
        "address": "152 Arlington Street",
        "neighborhood": "Downtown Boston",
        "zipcode": "02116",
        "school_type": ["pilot", "IB"],
        "grades_served_text": "6-12",
        "program_tags": ["IB", "bilingual", "pilot"],
        "language_programs": ["one-way Chinese bilingual"],
        "special_features": [
            "International Baccalaureate (IB) accredited school",
            "One-way Chinese bilingual program for Chinese-speaking families",
            "K-12 pathway with Quincy Lower (Elementary) school",
        ],
        "notes": (
            "Josiah Quincy Upper School (pilot) is an IB-accredited upper school "
            "offering grades 6-12. It offers a one-way Chinese bilingual program for "
            "families who speak Chinese at home, and connects to the Quincy Lower "
            "Elementary School to form a K-12 pathway. Both elementary and upper school "
            "are accredited IB schools."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/quincy-upper-school",
        ],
    },
    {
        "name": "Quincy Lower (K-5)",
        "address": "885 Washington Street",
        "neighborhood": "Downtown Boston / Chinatown",
        "zipcode": "02111",
        "school_type": ["traditional", "IB"],
        "grades_served_text": "K-5",
        "program_tags": ["IB", "bilingual"],
        "language_programs": ["one-way Chinese bilingual"],
        "special_features": [
            "IB accredited elementary school",
            "One-way Chinese bilingual program",
            "Pathway to Josiah Quincy Upper School",
        ],
        "notes": (
            "Josiah Quincy Lower (Elementary) School serves K-5 in the Chinatown/Downtown "
            "area. It is an IB-accredited school and offers a one-way Chinese bilingual "
            "program. Students may continue to Quincy Upper School for grades 6-12."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/quincy-lower",
        ],
    },
    {
        "name": "Snowden International",
        "address": "150 Newbury Street",
        "neighborhood": "Back Bay",
        "zipcode": "02116",
        "school_type": ["traditional"],
        "grades_served_text": "6-12",
        "program_tags": [],
        "language_programs": [],
        "special_features": [
            "International focus",
            "Citywide school",
        ],
        "notes": (
            "Muriel S. Snowden International School at Copley (also called Snowden "
            "International) serves grades 6-12 in the Back Bay. The school has an "
            "international curriculum focus and draws students citywide."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/snowden-international",
        ],
    },
    {
        "name": "McKinley Elementary",
        "address": "90 Warren Avenue",
        "neighborhood": "South End",
        "zipcode": "02116",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": (
            "McKinley Elementary School is located at the McKinley/Mackey building in "
            "the South End."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/mckinley-elementary",
        ],
    },
    {
        "name": "McKinley So. End Acad",
        "address": "90 Warren Avenue",
        "neighborhood": "South End",
        "zipcode": "02116",
        "school_type": ["traditional"],
        "grades_served_text": "6-12",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": (
            "McKinley South End Academy occupies the same McKinley/Mackey building as "
            "McKinley Elementary. Serves middle and/or high school grades. "
            "Verify current grade configuration with BPS."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/mckinley-south-end-academy",
        ],
    },
    {
        "name": "McKinley Prep High Sch",
        "address": "97 Peterborough Street",
        "neighborhood": "Fenway",
        "zipcode": "02215",
        "school_type": ["traditional"],
        "grades_served_text": "9-12",
        "program_tags": [],
        "language_programs": [],
        "special_features": [
            "Citywide high school",
        ],
        "notes": (
            "McKinley Preparatory High School is a citywide high school located in the "
            "Fenway area."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/mckinley-prep-high-school",
        ],
    },
    {
        "name": "McKinley Middle",
        "address": "50 St. Mary Street",
        "neighborhood": "Fenway",
        "zipcode": "02215",
        "school_type": ["traditional"],
        "grades_served_text": "6-8",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": (
            "McKinley Middle School is located at 50 St. Mary Street in the Fenway area."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/mckinley-middle",
        ],
    },
    {
        "name": "Boston Arts Academy",
        "address": "174 Ipswich Street",
        "neighborhood": "Fenway",
        "zipcode": "02215",
        "school_type": ["pilot"],
        "grades_served_text": "9-12",
        "program_tags": ["arts", "pilot"],
        "language_programs": [],
        "special_features": [
            "BPS arts-focused pilot high school",
            "Citywide; audition-based admissions",
            "Dual focus on rigorous academics and professional arts training",
        ],
        "notes": (
            "Boston Arts Academy is a citywide pilot high school that prepares a diverse "
            "community of aspiring artist-scholars. Students must audition in their art "
            "discipline for admission. The school offers a dual curriculum of academic "
            "and professional arts training."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/boston-arts-academy",
            "https://www.bostonpublicschools.org/schools-container/school-types",
        ],
    },
    {
        "name": "Boston Latin School",
        "address": "78 Avenue Louis Pasteur",
        "neighborhood": "Fenway",
        "zipcode": "02115",
        "school_type": ["exam"],
        "grades_served_text": "7-12",
        "program_tags": ["exam", "classical"],
        "language_programs": [],
        "special_features": [
            "Nation's oldest public school, founded 1635",
            "Exam school: admission grades 7 and 9",
            "Classical liberal arts curriculum",
        ],
        "notes": (
            "Boston Latin School is the nation's oldest public school (1635) and one of "
            "three BPS exam schools. Admission to grades 7 and 9 requires MAP Growth "
            "test and a minimum B GPA. The school offers a classical, college-preparatory "
            "curriculum."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/boston-latin-school",
            DISTRICT_SOURCES["exam_schools"],
        ],
    },
    {
        "name": "Kennedy Health Careers Academy",
        "address": "110 The Fenway",
        "neighborhood": "Fenway",
        "zipcode": "02115",
        "school_type": ["horace_mann_charter"],
        "grades_served_text": "9-12",
        "program_tags": ["health_careers", "early_college", "horace_mann_charter"],
        "language_programs": [],
        "special_features": [
            "Horace Mann Charter School (in-district)",
            "Health careers focus",
            "Early college pathways",
            "Located near Longwood Medical Area",
        ],
        "notes": (
            "Edward M. Kennedy Academy for Health Careers is a Horace Mann Charter "
            "School (in-district) serving grades 9-12. It focuses on health career "
            "pathways and is situated near the Longwood Medical Area, enabling "
            "partnerships with hospitals and medical institutions. "
            "Note: The CSV lists two addresses (110 The Fenway and 10 Fenwood Road); "
            "both appear in BPS records for this school."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/kennedy-health-careers-academy",
            DISTRICT_SOURCES["school_types"],
        ],
    },
    {
        "name": "Boston Adult Tech Acad",
        "address": "20 Church Street",
        "neighborhood": "Downtown Boston",
        "zipcode": "02116",
        "school_type": ["alternative", "adult"],
        "grades_served_text": "Adult (ages 19-22)",
        "program_tags": ["adult_education"],
        "language_programs": [],
        "special_features": [
            "Serves students ages 19-22",
            "Technical and vocational focus",
        ],
        "notes": (
            "Boston Adult Technical Academy serves students ages 19-22 who seek "
            "a high school credential with a technical/vocational focus."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/boston-adult-tech-academy",
        ],
    },

    # ── SOUTH END / ROXBURY ────────────────────────────────────────────────

    {
        "name": "Hurley Elementary",
        "address": "70 Worcester Street",
        "neighborhood": "South End",
        "zipcode": "02118",
        "school_type": ["traditional"],
        "grades_served_text": "PK-8",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": (
            "Hurley K-8 School serves approximately 349 students in the South End. "
            "The CSV lists this as 'Hurley Elementary' but the school operates as a K-8."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/hurley-elementary",
        ],
    },
    {
        "name": "Blackstone Elementary",
        "address": "380 Shawmut Avenue",
        "neighborhood": "South End",
        "zipcode": "02118",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": (
            "Blackstone Elementary School is a neighborhood school in Boston's South End."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/blackstone-elementary",
        ],
    },
    {
        "name": "Mason Elementary",
        "address": "150 Norfolk Avenue",
        "neighborhood": "Roxbury",
        "zipcode": "02119",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Neighborhood elementary in Roxbury.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/mason-elementary",
        ],
    },
    {
        "name": "Orchard Gardens K-8",
        "address": "906 Albany Street",
        "neighborhood": "Roxbury",
        "zipcode": "02119",
        "school_type": ["pilot"],
        "grades_served_text": "K-8",
        "program_tags": ["pilot"],
        "language_programs": ["Cape Verdean Creole SEI"],
        "special_features": [
            "Pilot school with arts-integrated curriculum",
            "Cape Verdean Creole SEI language-specific program",
        ],
        "notes": (
            "Orchard Gardens K-8 is a pilot school in Roxbury that became well known "
            "for its arts-integrated curriculum turnaround model. It also hosts a "
            "Cape Verdean Creole SEI language-specific program."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/orchard-gardens-k-8",
            DISTRICT_SOURCES["sei_language_specific"],
        ],
    },
    {
        "name": "Timilty Middle",
        "address": "205 Roxbury Street",
        "neighborhood": "Roxbury",
        "zipcode": "02119",
        "school_type": ["traditional"],
        "grades_served_text": "6-8",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": (
            "James P. Timilty Middle School in Roxbury. Note: Wikipedia indicates "
            "the Timilty was closed in 2022; verify current operating status with BPS, "
            "as the address appears in the 2024-2025 CSV."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/timilty-middle",
        ],
    },
    {
        "name": "Hale Elementary",
        "address": "51 Cedar Street",
        "neighborhood": "Roxbury",
        "zipcode": "02119",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Neighborhood elementary in Roxbury.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/hale-elementary",
        ],
    },
    {
        "name": "Higginson/Lewis K-8",
        "address": "131 Walnut Avenue",
        "neighborhood": "Roxbury",
        "zipcode": "02119",
        "school_type": ["traditional"],
        "grades_served_text": "K-8",
        "program_tags": [],
        "language_programs": [],
        "special_features": [
            "Offers 9 sports per GreatSchools data",
        ],
        "notes": (
            "Higginson/Lewis K-8 School in Roxbury. Offers athletic programming "
            "across multiple sports."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/higginson-lewis-k-8",
        ],
    },
    {
        "name": "Haynes EEC",
        "address": "263 Blue Hill Ave",
        "neighborhood": "Roxbury",
        "zipcode": "02119",
        "school_type": ["early_education"],
        "grades_served_text": "K0-K1",
        "program_tags": ["early_childhood"],
        "language_programs": [],
        "special_features": [
            "Early education center for ages 3-4",
        ],
        "notes": (
            "Haynes Early Education Center on Blue Hill Avenue in Roxbury provides "
            "K0/K1 programming for children ages 3-4."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/haynes-eec",
        ],
    },
    {
        "name": "Ellis Elementary",
        "address": "302 Walnut Avenue",
        "neighborhood": "Roxbury",
        "zipcode": "02119",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Neighborhood elementary in Roxbury.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/ellis-elementary",
        ],
    },
    {
        "name": "Boston Latin Academy",
        "address": "205 Townsend Street",
        "neighborhood": "Roxbury / Dorchester border",
        "zipcode": "02121",
        "school_type": ["exam"],
        "grades_served_text": "7-12",
        "program_tags": ["exam"],
        "language_programs": [],
        "special_features": [
            "BPS exam school; admission grades 7 and 9",
            "Formerly Roxbury Memorial High School",
            "College-preparatory curriculum",
        ],
        "notes": (
            "Boston Latin Academy (formerly Roxbury Memorial High School) is one of "
            "three BPS exam schools. Admission requires MAP Growth test and a minimum "
            "B GPA. The school offers a rigorous college-preparatory curriculum."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/boston-latin-academy",
            DISTRICT_SOURCES["exam_schools"],
        ],
    },
    {
        "name": "Hernandez K-8",
        "address": "61 School Street",
        "neighborhood": "Roxbury",
        "zipcode": "02119",
        "school_type": ["traditional"],
        "grades_served_text": "K-8",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Hernández K-8 School in Roxbury.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/hernandez-k-8",
        ],
    },
    {
        "name": "Mendell Elementary",
        "address": "164 School Street",
        "neighborhood": "Roxbury",
        "zipcode": "02119",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Neighborhood elementary in Roxbury.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/mendell-elementary",
        ],
    },
    {
        "name": "Tobin K-8",
        "address": "40 Smith Street",
        "neighborhood": "Roxbury",
        "zipcode": "02120",
        "school_type": ["traditional"],
        "grades_served_text": "K-8",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Tobin K-8 School in Roxbury.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/tobin-k-8",
        ],
    },
    {
        "name": "Madison Park High",
        "address": "75 Malcolm X Blvd",
        "neighborhood": "Roxbury",
        "zipcode": "02120",
        "school_type": ["traditional"],
        "grades_served_text": "9-12",
        "program_tags": ["CTE", "vocational"],
        "language_programs": [],
        "special_features": [
            "Technical Vocational High School",
            "Chapter 74 vocational programs",
            "Citywide high school",
        ],
        "notes": (
            "Madison Park Technical Vocational High School is a comprehensive CTE "
            "(Career and Technical Education) high school offering Chapter 74 approved "
            "vocational programs in trades, technology, and other fields. It is a "
            "citywide option for BPS high school students."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/madison-park-high",
            "https://www.bostonpublicschools.org/academics/career-and-technical-education/madison-park-technical-vocational-high-school",
        ],
    },
    {
        "name": "O'Bryant Math & Sci.",
        "address": "55 Malcolm X Blvd",
        "neighborhood": "Roxbury",
        "zipcode": "02120",
        "school_type": ["exam"],
        "grades_served_text": "7-12",
        "program_tags": ["exam", "STEM"],
        "language_programs": [],
        "special_features": [
            "BPS exam school: admission grades 7, 9, and small number at grade 10",
            "Mathematics and science focus",
        ],
        "notes": (
            "John D. O'Bryant School of Mathematics and Science is one of three BPS "
            "exam schools. It is unique in that it accepts a small number of new "
            "students at grade 10 in addition to grades 7 and 9. The school has a "
            "strong mathematics and science curriculum."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/obryant-math-science",
            DISTRICT_SOURCES["exam_schools"],
        ],
    },
    {
        "name": "Boston Evening Academy",
        "address": "20 Kearsage Avenue",
        "neighborhood": "Roxbury",
        "zipcode": "02119",
        "school_type": ["alternative"],
        "grades_served_text": "9-12 (evening)",
        "program_tags": ["alternative", "adult_education"],
        "language_programs": [],
        "special_features": [
            "Evening schedule",
            "Alternative diploma pathway for over-age students",
        ],
        "notes": (
            "Boston Day and Evening Academy (charter) provides an alternative pathway "
            "to graduation for students who are over-age or have been disconnected from "
            "traditional schooling. Operates on an evening schedule."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/boston-evening-academy",
        ],
    },
    {
        "name": "Carter Center",
        "address": "396 Northampton Street",
        "neighborhood": "Roxbury",
        "zipcode": "02118",
        "school_type": ["alternative"],
        "grades_served_text": "Varies",
        "program_tags": ["alternative", "special_education"],
        "language_programs": [],
        "special_features": [
            "Carter Development Center",
            "Specialized programming",
        ],
        "notes": (
            "Carter Center (Carter Development Center) in Roxbury provides specialized "
            "programming. Verify exact grade span and current program focus with BPS."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/carter-center",
        ],
    },
    {
        "name": "Greater Egleston High",
        "address": "80 School Street",
        "neighborhood": "Roxbury",
        "zipcode": "02119",
        "school_type": ["pilot"],
        "grades_served_text": "9-12",
        "program_tags": ["pilot", "alternative"],
        "language_programs": [],
        "special_features": [
            "Pilot high school",
            "Smaller learning community focus",
        ],
        "notes": (
            "Greater Egleston High School is a BPS pilot high school in Roxbury "
            "offering a smaller, more personalized learning environment for students "
            "in grades 9-12."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/greater-egleston-high",
        ],
    },
    {
        "name": "Higginson Elementary",
        "address": "160 Harrishof Street",
        "neighborhood": "Roxbury",
        "zipcode": "02119",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": (
            "Higginson Elementary School (separate from Higginson/Lewis K-8) in Roxbury."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/higginson-elementary",
        ],
    },
    {
        "name": "Dudley Street Neighborhood Charter School",
        "address": "6 Shirley St",
        "neighborhood": "Roxbury",
        "zipcode": "02119",
        "school_type": ["horace_mann_charter"],
        "grades_served_text": "PK-8",
        "program_tags": ["horace_mann_charter"],
        "language_programs": [],
        "special_features": [
            "Horace Mann (in-district) charter school",
            "Community-centered model",
        ],
        "notes": (
            "Dudley Street Neighborhood Charter School is a Horace Mann (in-district) "
            "charter school in Roxbury with a strong community focus."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/dudley-street-neighborhood-charter",
        ],
    },

    # ── SOUTH BOSTON ───────────────────────────────────────────────────────

    {
        "name": "Perkins Elementary",
        "address": "50 Burke Street",
        "neighborhood": "South Boston",
        "zipcode": "02127",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Neighborhood elementary in South Boston.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/perkins-elementary",
        ],
    },
    {
        "name": "Excel High",
        "address": "95 G Street",
        "neighborhood": "South Boston",
        "zipcode": "02127",
        "school_type": ["traditional"],
        "grades_served_text": "9-12",
        "program_tags": [],
        "language_programs": [],
        "special_features": [
            "Citywide high school",
        ],
        "notes": (
            "Excel High School serves grades 9-12 in South Boston with approximately "
            "387 students. Note: BPS announced a closure process for Excel; verify "
            "current operating status."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/excel-high",
            "https://www.bostonpublicschools.org/about-bps/capital-planning/closures/excel",
        ],
    },
    {
        "name": "Tynan Elementary",
        "address": "650 E. Fourth Street",
        "neighborhood": "South Boston",
        "zipcode": "02127",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Neighborhood elementary in South Boston.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/tynan-elementary",
        ],
    },
    {
        "name": "Perry K-8",
        "address": "745 E. Seventh Street",
        "neighborhood": "South Boston",
        "zipcode": "02127",
        "school_type": ["traditional"],
        "grades_served_text": "PK-8",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Perry K-8 School in South Boston.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/perry-k-8",
        ],
    },
    {
        "name": "Middle School Academy",
        "address": "215 Dorchester Street",
        "neighborhood": "South Boston",
        "zipcode": "02127",
        "school_type": ["alternative"],
        "grades_served_text": "6-8",
        "program_tags": ["alternative"],
        "language_programs": [],
        "special_features": [],
        "notes": (
            "Middle School Academy at the Gavin building in South Boston. This may be "
            "a smaller alternative middle program; verify current status with BPS."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/middle-school-academy",
        ],
    },
    {
        "name": "UP Academy",
        "address": "215 Dorchester Street",
        "neighborhood": "South Boston",
        "zipcode": "02127",
        "school_type": ["horace_mann_charter"],
        "grades_served_text": "K-8",
        "program_tags": ["horace_mann_charter"],
        "language_programs": [],
        "special_features": [
            "UP Academy Charter School of Boston (in-district)",
        ],
        "notes": (
            "UP Academy Charter School of Boston (Horace Mann / in-district charter) "
            "occupies the Gavin building. Serves K-8."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/up-academy-boston",
        ],
    },
    {
        "name": "Condon Elementary",
        "address": "200 D Street",
        "neighborhood": "South Boston",
        "zipcode": "02127",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Neighborhood elementary in South Boston.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/condon-elementary",
        ],
    },

    # ── DORCHESTER ─────────────────────────────────────────────────────────

    {
        "name": "Clap Elementary",
        "address": "35 Harvest Street",
        "neighborhood": "Dorchester",
        "zipcode": "02125",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": (
            "Roger Clap Innovation School / Clap Elementary in Dorchester. Note: BPS "
            "planning documents reference a Clap-Winthrop merger (Lilla G. Frederick "
            "Elementary School); verify current operating status."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/clap-elementary",
            "https://www.bostonpublicschools.org/about-bps/capital-planning/mergers/frederick",
        ],
    },
    {
        "name": "Russell Elementary",
        "address": "750 Columbia Road",
        "neighborhood": "Dorchester",
        "zipcode": "02125",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Neighborhood elementary in Dorchester.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/russell-elementary",
        ],
    },
    {
        "name": "Trotter K-8",
        "address": "135 Humboldt Avenue",
        "neighborhood": "Dorchester",
        "zipcode": "02121",
        "school_type": ["traditional"],
        "grades_served_text": "K-8",
        "program_tags": [],
        "language_programs": [],
        "special_features": [
            "Special Olympics National Banner School 2024-2025",
        ],
        "notes": (
            "William Monroe Trotter K-8 School in Dorchester was named a Special Olympics "
            "National Banner Unified Champion School for 2024-2025."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/trotter-k-8",
        ],
    },
    {
        "name": "King K-8",
        "address": "77 Lawrence Avenue",
        "neighborhood": "Dorchester",
        "zipcode": "02121",
        "school_type": ["traditional"],
        "grades_served_text": "K-8",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Martin Luther King Jr. K-8 School in Dorchester.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/king-k-8",
        ],
    },
    {
        "name": "Frederick Pilot Middle",
        "address": "270 Columbia Road",
        "neighborhood": "Dorchester",
        "zipcode": "02121",
        "school_type": ["pilot"],
        "grades_served_text": "6-8",
        "program_tags": ["pilot"],
        "language_programs": [],
        "special_features": [
            "Pilot middle school",
            "Also referenced as Lilla G. Frederick Pilot Middle School",
        ],
        "notes": (
            "Lilla G. Frederick Pilot Middle School in Dorchester is a BPS pilot school "
            "serving grades 6-8. Note: BPS capital planning also references a separate "
            "'Lilla G. Frederick Elementary School' as the Clap-Winthrop merger school."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/lilla-g-frederick-pilot-middle-school",
        ],
    },
    {
        "name": "Holland Elementary",
        "address": "85 Olney Street",
        "neighborhood": "Dorchester",
        "zipcode": "02121",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Neighborhood elementary in Dorchester.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/holland-elementary",
        ],
    },
    {
        "name": "Winthrop Elementary",
        "address": "35 Brookford Street",
        "neighborhood": "Dorchester",
        "zipcode": "02125",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": (
            "Winthrop Elementary in Dorchester. See also Clap-Winthrop merger note "
            "under Clap Elementary."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/winthrop-elementary",
        ],
    },
    {
        "name": "Mather Elementary",
        "address": "1 Parish Street",
        "neighborhood": "Dorchester",
        "zipcode": "02122",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [
            "Nation's first public elementary school (1639)",
        ],
        "notes": (
            "The Mather School is one of the oldest schools in the country, established "
            "in 1639 as the nation's first public elementary school. It serves PK-6 "
            "in the Dorchester neighborhood."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/mather-elementary",
        ],
    },
    {
        "name": "UP Academy Charter School of Dorchester",
        "address": "35 Westville Street",
        "neighborhood": "Dorchester",
        "zipcode": "02124",
        "school_type": ["horace_mann_charter"],
        "grades_served_text": "K-8",
        "program_tags": ["horace_mann_charter"],
        "language_programs": [],
        "special_features": [
            "In-district charter school",
        ],
        "notes": (
            "UP Academy Charter School of Dorchester (in-district charter / Horace Mann) "
            "at the Marshall building, serving K-8 students in Dorchester."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/up-academy-charter-school-dorchester",
        ],
    },
    {
        "name": "Henderson Lower (K-3)",
        "address": "1669 Dorchester Avenue",
        "neighborhood": "Dorchester",
        "zipcode": "02122",
        "school_type": ["inclusion"],
        "grades_served_text": "K-3",
        "program_tags": ["inclusion", "special_education"],
        "language_programs": [],
        "special_features": [
            "Inclusion school lower division",
            "Part of Dr. William W. Henderson K-12 Inclusion School",
        ],
        "notes": (
            "Henderson Lower School (K-3) is the lower division of the Dr. William W. "
            "Henderson Inclusion School, which serves students from early childhood "
            "through Grade 12 and Transition. The Henderson Inclusion School integrates "
            "students with and without disabilities in all programs."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/henderson-lower",
            "https://www.bostonpublicschools.org/about-bps/capital-planning/reconfigurations/henderson",
        ],
    },
    {
        "name": "Henderson Upper (4-12)",
        "address": "18 Croftland Avenue",
        "neighborhood": "Dorchester",
        "zipcode": "02124",
        "school_type": ["inclusion"],
        "grades_served_text": "4-12 and Transition",
        "program_tags": ["inclusion", "special_education"],
        "language_programs": [],
        "special_features": [
            "Inclusion school upper division",
            "Serves through post-secondary Transition program",
            "Part of Dr. William W. Henderson K-12 Inclusion School",
        ],
        "notes": (
            "Henderson Upper School (grades 4-12 and Transition) is the upper division "
            "of the Dr. William W. Henderson Inclusion School. Together with Henderson "
            "Lower, it forms a full K-12 inclusion pathway integrating students with and "
            "without disabilities."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/henderson-dr-william-w-inclusion-school",
            "https://www.bostonpublicschools.org/about-bps/capital-planning/reconfigurations/henderson",
        ],
    },
    {
        "name": "Murphy K-8",
        "address": "1 Worrell Street",
        "neighborhood": "Dorchester",
        "zipcode": "02122",
        "school_type": ["traditional"],
        "grades_served_text": "K-8",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Richard J. Murphy K-8 School in Dorchester.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/murphy-k-8",
        ],
    },
    {
        "name": "Kenny Elementary",
        "address": "19 Oakton Avenue",
        "neighborhood": "Dorchester",
        "zipcode": "02122",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Neighborhood elementary in Dorchester.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/kenny-elementary",
        ],
    },
    {
        "name": "Boston International HS",
        "address": "100 Maxwell Street",
        "neighborhood": "Dorchester",
        "zipcode": "02124",
        "school_type": ["traditional"],
        "grades_served_text": "9-12",
        "program_tags": ["ESL", "newcomers"],
        "language_programs": [],
        "special_features": [
            "Serves students not yet proficient in English",
            "Multilingual and newcomer focus",
            "Citywide high school",
        ],
        "notes": (
            "Boston International High School serves grades 9-12 and is specifically "
            "designed for students who are not yet proficient in English, including "
            "recent immigrants and newcomers."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/boston-international-high-school",
        ],
    },
    {
        "name": "Newcomers Academy",
        "address": "100 Maxwell Street",
        "neighborhood": "Dorchester",
        "zipcode": "02124",
        "school_type": ["traditional"],
        "grades_served_text": "Varies (newcomer)",
        "program_tags": ["ESL", "newcomers"],
        "language_programs": [],
        "special_features": [
            "Intensive English language support for newly arrived immigrants",
            "Shares building with Boston International HS",
        ],
        "notes": (
            "Newcomers Academy is a specialized program for recent immigrant students "
            "not yet proficient in English. It co-locates at the Thompson building with "
            "Boston International High School."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/newcomers-academy",
        ],
    },
    {
        "name": "TechBoston Academy",
        "address": "9 Peacevale Road",
        "neighborhood": "Dorchester",
        "zipcode": "02124",
        "school_type": ["traditional"],
        "grades_served_text": "6-12",
        "program_tags": ["STEM", "technology"],
        "language_programs": ["Haitian Creole SEI"],
        "special_features": [
            "Technology and STEM focus",
            "Haitian Creole SEI language-specific program",
            "Citywide high school pathway",
        ],
        "notes": (
            "TechBoston Academy serves grades 6-12 with a technology and STEM emphasis. "
            "It hosts a Haitian Creole SEI language-specific program. The CSV also lists "
            "a 'TechBoston Acad Lower (6-9)' entry at the same address, indicating a "
            "lower-school division."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/techboston-academy",
            DISTRICT_SOURCES["sei_language_specific"],
        ],
    },
    {
        "name": "TechBoston Acad Lower (6-9)",
        "address": "9 Peacevale Road",
        "neighborhood": "Dorchester",
        "zipcode": "02124",
        "school_type": ["traditional"],
        "grades_served_text": "6-9",
        "program_tags": ["STEM", "technology"],
        "language_programs": ["Haitian Creole SEI"],
        "special_features": [
            "Lower division of TechBoston Academy",
            "Technology and STEM focus",
        ],
        "notes": (
            "TechBoston Academy Lower (grades 6-9) is the lower division of TechBoston "
            "Academy at the same Dorchester building."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/techboston-academy",
        ],
    },
    {
        "name": "Lee Elementary",
        "address": "155 Talbot Avenue",
        "neighborhood": "Dorchester",
        "zipcode": "02124",
        "school_type": ["traditional"],
        "grades_served_text": "K-8",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": (
            "Lee K-8 School in Dorchester. Note: BPS announced Lee as part of a 2024 "
            "mental health initiative with $21M in city funding."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/lee-elementary",
        ],
    },
    {
        "name": "Lee Academy",
        "address": "25 Dunbar Ave.",
        "neighborhood": "Dorchester",
        "zipcode": "02124",
        "school_type": ["pilot"],
        "grades_served_text": "6-12",
        "program_tags": ["pilot", "alternative"],
        "language_programs": [],
        "special_features": [
            "Pilot school",
        ],
        "notes": (
            "Lee Academy Pilot School at the Fifield building. Note: BPS announced "
            "closure of Lee Academy Pilot School; verify current status."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/lee-academy",
            "https://www.bostonpublicschools.org/about-bps/capital-planning/closures/laps",
        ],
    },
    {
        "name": "Holmes Elementary",
        "address": "40 School Street",
        "neighborhood": "Dorchester",
        "zipcode": "02124",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Neighborhood elementary in Dorchester.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/holmes-elementary",
        ],
    },
    {
        "name": "Comm Acad Sci Health",
        "address": "11 Charles Street",
        "neighborhood": "Dorchester",
        "zipcode": "02122",
        "school_type": ["traditional"],
        "grades_served_text": "9-12",
        "program_tags": ["health_careers", "STEM"],
        "language_programs": ["Haitian Creole SEI"],
        "special_features": [
            "Science and health focus",
            "Haitian Creole SEI language-specific program",
            "Citywide high school",
        ],
        "notes": (
            "Community Academy of Science and Health (CASH) serves grades 9-12 in "
            "Dorchester with a science and health curriculum focus. It hosts a Haitian "
            "Creole SEI language-specific program. Note: BPS announced a closure process "
            "for CASH; verify current status."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/community-academy-of-science-and-health",
            "https://www.bostonpublicschools.org/about-bps/capital-planning/closures/cash",
            DISTRICT_SOURCES["sei_language_specific"],
        ],
    },
    {
        "name": "Dorchester Academy",
        "address": "11 Charles Street",
        "neighborhood": "Dorchester",
        "zipcode": "02122",
        "school_type": ["alternative"],
        "grades_served_text": "9-12",
        "program_tags": ["alternative"],
        "language_programs": [],
        "special_features": [
            "Alternative high school program",
        ],
        "notes": (
            "Dorchester Academy is an alternative high school program at the Cleveland "
            "building in Dorchester."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/dorchester-academy",
        ],
    },
    {
        "name": "P.A. Shaw",
        "address": "429 Norfolk Street",
        "neighborhood": "Dorchester",
        "zipcode": "02124",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "P.A. Shaw Elementary School in Dorchester.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/pa-shaw",
        ],
    },
    {
        "name": "Greenwood Sarah K-8",
        "address": "189 Glenway Street",
        "neighborhood": "Dorchester",
        "zipcode": "02121",
        "school_type": ["traditional"],
        "grades_served_text": "K-8",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Sarah Greenwood K-8 School in Dorchester.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/greenwood-sarah-k-8",
        ],
    },
    {
        "name": "Burke High",
        "address": "60 Washington Street",
        "neighborhood": "Dorchester",
        "zipcode": "02121",
        "school_type": ["traditional"],
        "grades_served_text": "9-12",
        "program_tags": [],
        "language_programs": ["Cape Verdean Creole SEI"],
        "special_features": [
            "Citywide high school",
            "Cape Verdean Creole SEI language-specific program",
        ],
        "notes": (
            "Jeremiah E. Burke High School (now also referenced as Dr. Albert D. Holland "
            "High School of Technology per Wikipedia) serves grades 9-12. It hosts a "
            "Cape Verdean Creole SEI language-specific program."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/burke-high",
            DISTRICT_SOURCES["sei_language_specific"],
        ],
    },
    {
        "name": "Dearborn Middle School",
        "address": "60 Washington Street",
        "neighborhood": "Dorchester",
        "zipcode": "02121",
        "school_type": ["traditional"],
        "grades_served_text": "6-12",
        "program_tags": ["STEM"],
        "language_programs": ["Cape Verdean Creole SEI"],
        "special_features": [
            "STEM Academy focus",
            "Cape Verdean Creole SEI language-specific program",
            "Shares building with Burke High",
        ],
        "notes": (
            "Dearborn STEM Academy (6-12) shares the Burke High building. It offers a "
            "STEM-focused curriculum and hosts a Cape Verdean Creole SEI program."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/dearborn-stem-academy",
            DISTRICT_SOURCES["sei_language_specific"],
        ],
    },
    {
        "name": "Dever Elementary",
        "address": "325 Mt. Vernon Street",
        "neighborhood": "Dorchester",
        "zipcode": "02125",
        "school_type": ["traditional"],
        "grades_served_text": "K-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": (
            "Dever Elementary in Dorchester. Note: BPS announced a closure process for "
            "Dever; verify current status."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/dever-elementary",
            "https://www.bostonpublicschools.org/about-bps/capital-planning/closures/dever",
        ],
    },
    {
        "name": "McCormack Middle",
        "address": "315 Mt. Vernon Street",
        "neighborhood": "Dorchester",
        "zipcode": "02125",
        "school_type": ["traditional"],
        "grades_served_text": "6-8",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": (
            "John W. McCormack Middle School in Dorchester. Note: Wikipedia indicates "
            "McCormack merged with Boston Community Leadership Academy in 2021; verify "
            "current status."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/mccormack-middle",
        ],
    },
    {
        "name": "Everett Elementary",
        "address": "71 Pleasant Street",
        "neighborhood": "Dorchester",
        "zipcode": "02125",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Neighborhood elementary in Dorchester.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/everett-elementary",
        ],
    },

    # ── MATTAPAN ───────────────────────────────────────────────────────────

    {
        "name": "Taylor Elementary",
        "address": "1060 Morton Street",
        "neighborhood": "Mattapan",
        "zipcode": "02126",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": ["Haitian Creole SEI"],
        "special_features": [
            "Haitian Creole SEI language-specific program",
        ],
        "notes": (
            "Taylor Elementary in Mattapan hosts a Haitian Creole SEI language-specific "
            "program, serving Mattapan's large Haitian-American community."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/taylor-elementary",
            DISTRICT_SOURCES["sei_language_specific"],
        ],
    },
    {
        "name": "Mildred Avenue K-8",
        "address": "5 Mildred Avenue",
        "neighborhood": "Mattapan",
        "zipcode": "02126",
        "school_type": ["traditional"],
        "grades_served_text": "K-8",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Mildred Avenue K-8 School in Mattapan.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/mildred-avenue-k-8",
        ],
    },
    {
        "name": "Young Achievers K-8",
        "address": "20 Outlook Road",
        "neighborhood": "Mattapan",
        "zipcode": "02126",
        "school_type": ["pilot"],
        "grades_served_text": "K-8",
        "program_tags": ["pilot", "STEM"],
        "language_programs": [],
        "special_features": [
            "Pilot school with science and math focus",
            "Recipient of 2024 city mental health initiative funding",
        ],
        "notes": (
            "Young Achievers Science and Math K-8 (Pilot) in Mattapan focuses on STEM "
            "education. It was included in BPS's 2024 $21M mental health initiative."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/young-achievers-k-8",
        ],
    },
    {
        "name": "Mattahunt Elementary",
        "address": "100 Hebron Street",
        "neighborhood": "Mattapan",
        "zipcode": "02126",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Neighborhood elementary in Mattapan.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/mattahunt-elementary",
        ],
    },
    {
        "name": "Chittick Elementary",
        "address": "154 Ruskindale Road",
        "neighborhood": "Mattapan",
        "zipcode": "02126",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Neighborhood elementary in Mattapan.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/chittick-elementary",
        ],
    },
    {
        "name": "Ellison/ Parks ELC",
        "address": "108 Babson Street",
        "neighborhood": "Mattapan",
        "zipcode": "02126",
        "school_type": ["early_education"],
        "grades_served_text": "K0-K1",
        "program_tags": ["early_childhood"],
        "language_programs": [],
        "special_features": [
            "Early learning center for ages 3-4",
        ],
        "notes": (
            "Ellison/Parks Early Learning Center in Mattapan provides K0/K1 early "
            "childhood programming."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/ellisonparks-elc",
        ],
    },

    # ── ROSLINDALE ─────────────────────────────────────────────────────────

    {
        "name": "Philbrick Elementary",
        "address": "40 Philbrick Street",
        "neighborhood": "Roslindale",
        "zipcode": "02131",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": (
            "Note: BPS records reference a 'Sarah Roberts Elementary School' formed by "
            "the merger of Philbrick and Sumner schools for 2025-26. Verify current "
            "operating identity with BPS."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/philbrick-elementary",
        ],
    },
    {
        "name": "Haley Elementary",
        "address": "570 American Legion Highway",
        "neighborhood": "Roslindale",
        "zipcode": "02131",
        "school_type": ["pilot"],
        "grades_served_text": "K-8",
        "program_tags": ["pilot"],
        "language_programs": [],
        "special_features": [
            "Haley K-8 Pilot School",
        ],
        "notes": "Haley K-8 Pilot School in Roslindale.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/haley-elementary",
        ],
    },
    {
        "name": "Conley Elementary",
        "address": "450 Poplar Street",
        "neighborhood": "Roslindale",
        "zipcode": "02131",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Neighborhood elementary in Roslindale.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/conley-elementary",
        ],
    },
    {
        "name": "Irving Middle",
        "address": "105 Cummins Highway",
        "neighborhood": "Roslindale",
        "zipcode": "02131",
        "school_type": ["traditional"],
        "grades_served_text": "6-8",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Irving Middle School in Roslindale.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/irving-middle",
        ],
    },
    {
        "name": "Sumner Elementary",
        "address": "15 Basile Street",
        "neighborhood": "Roslindale",
        "zipcode": "02131",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": (
            "Charles Sumner Elementary in Roslindale. Note: BPS merged Sumner and "
            "Philbrick into Sarah Roberts Elementary for 2025-26; verify current status."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/sumner-elementary",
        ],
    },
    {
        "name": "Bates Elementary",
        "address": "426 Beech Street",
        "neighborhood": "Roslindale",
        "zipcode": "02131",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Neighborhood elementary in Roslindale.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/bates-elementary",
        ],
    },
    {
        "name": "Mozart Elementary",
        "address": "236 Beech Street",
        "neighborhood": "Roslindale",
        "zipcode": "02131",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Neighborhood elementary in Roslindale.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/mozart-elementary",
        ],
    },

    # ── JAMAICA PLAIN ──────────────────────────────────────────────────────

    {
        "name": "BTU K-8 Pilot",
        "address": "25 Walk Hill Street",
        "neighborhood": "Jamaica Plain",
        "zipcode": "02130",
        "school_type": ["pilot"],
        "grades_served_text": "K-8",
        "program_tags": ["pilot"],
        "language_programs": [],
        "special_features": [
            "Teacher-led pilot school governed by shared leadership",
        ],
        "notes": (
            "Boston Teachers Union K-8 Pilot School (BTU School) is a teacher-led BPS "
            "pilot school in Jamaica Plain employing shared leadership to support all "
            "students."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/btu-k-8-pilot",
            "https://www.btuschool.com/",
        ],
    },
    {
        "name": "Community Academy",
        "address": "25 Glen Road",
        "neighborhood": "Jamaica Plain",
        "zipcode": "02130",
        "school_type": ["alternative"],
        "grades_served_text": "Varies",
        "program_tags": ["alternative"],
        "language_programs": [],
        "special_features": [],
        "notes": (
            "Community Academy in Jamaica Plain. Note: BPS announced closure of "
            "Community Academy; verify current status."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/about-bps/capital-planning/closures/community-academy",
        ],
    },
    {
        "name": "English High",
        "address": "144 McBride Street",
        "neighborhood": "Jamaica Plain",
        "zipcode": "02130",
        "school_type": ["traditional"],
        "grades_served_text": "9-12",
        "program_tags": [],
        "language_programs": [],
        "special_features": [
            "Second oldest public high school in the United States (est. 1821)",
            "Citywide high school",
        ],
        "notes": (
            "The English High School, established in 1821, is the second-oldest public "
            "high school in the United States. It is a citywide BPS high school in "
            "Jamaica Plain."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/english-high-school",
        ],
    },
    {
        "name": "Kennedy John F Elemen",
        "address": "7 Bolster Street",
        "neighborhood": "Jamaica Plain",
        "zipcode": "02130",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "John F. Kennedy Elementary School in Jamaica Plain.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/kennedy-john-f-elementary",
        ],
    },
    {
        "name": "West Zone ELC",
        "address": "200 Heath Street",
        "neighborhood": "Jamaica Plain",
        "zipcode": "02130",
        "school_type": ["early_education", "inclusion"],
        "grades_served_text": "K0-K1",
        "program_tags": ["early_childhood", "special_education", "ESL"],
        "language_programs": [],
        "special_features": [
            "Integrated early childhood classrooms for students with disabilities",
            "ESL services",
        ],
        "notes": (
            "West Zone Early Learning Center provides K0/K1 programming at the Hennigan "
            "building. The school offers integrated early childhood classrooms for "
            "students with disabilities and ESL services."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/west-zone-early-learning-center",
        ],
    },
    {
        "name": "Hennigan K-8",
        "address": "200 Heath Street",
        "neighborhood": "Jamaica Plain",
        "zipcode": "02130",
        "school_type": ["traditional"],
        "grades_served_text": "K-8",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": (
            "Hennigan K-8 School shares the Hennigan building with West Zone ELC in "
            "Jamaica Plain."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/hennigan-k-8",
        ],
    },
    {
        "name": "Curley Lower (K1-5)",
        "address": "40 Pershing Road",
        "neighborhood": "Jamaica Plain",
        "zipcode": "02130",
        "school_type": ["traditional"],
        "grades_served_text": "K1-5",
        "program_tags": [],
        "language_programs": [],
        "special_features": [
            "Lower division of the James J. Curley K-8 School",
        ],
        "notes": (
            "James J. Curley Lower School (K1-5) in Jamaica Plain is the lower division "
            "of the Curley K-8 School."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/curley-lower",
        ],
    },
    {
        "name": "Curley Upper (6-8)",
        "address": "493 Centre Street",
        "neighborhood": "Jamaica Plain",
        "zipcode": "02130",
        "school_type": ["traditional"],
        "grades_served_text": "6-8",
        "program_tags": [],
        "language_programs": [],
        "special_features": [
            "Upper division of the James J. Curley K-8 School",
        ],
        "notes": (
            "James J. Curley Upper School (grades 6-8) in Jamaica Plain is the upper "
            "division of the Curley K-8 School."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/curley-upper",
        ],
    },
    {
        "name": "Manning Elementary",
        "address": "130 Louders Lane",
        "neighborhood": "Jamaica Plain",
        "zipcode": "02130",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Neighborhood elementary in Jamaica Plain.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/manning-elementary",
        ],
    },
    {
        "name": "Fenway High",
        "address": "67 Allegheny Street",
        "neighborhood": "Roxbury / Mission Hill",
        "zipcode": "02120",
        "school_type": ["pilot"],
        "grades_served_text": "9-12",
        "program_tags": ["pilot", "early_college"],
        "language_programs": [],
        "special_features": [
            "Pilot school founded 1983",
            "State-designated Early College High School",
            "College credit partnerships with UMass Boston and Wentworth Institute",
            "Citywide high school",
        ],
        "notes": (
            "Fenway High School is a BPS pilot high school and state-designated Early "
            "College High School. Students can earn up to two years of college credit "
            "through partnerships with UMass Boston and Wentworth Institute of Technology. "
            "The school emphasizes personalized education, intellectual habits of mind, "
            "and active citizenship."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/fenway-high-school",
            "https://www.fenwayhs.org/",
        ],
    },
    {
        "name": "Mission Hill K-8",
        "address": "20 Child St",
        "neighborhood": "Jamaica Plain",
        "zipcode": "02130",
        "school_type": ["pilot"],
        "grades_served_text": "K-8",
        "program_tags": ["pilot"],
        "language_programs": [],
        "special_features": [
            "Pilot school",
        ],
        "notes": (
            "Mission Hill K-8 School at the Agassiz building in Jamaica Plain. "
            "Note: Wikipedia indicates Mission Hill School (pilot) was closed in 2022 "
            "after a bullying investigation; however, the address appears in the 2024-2025 "
            "CSV as 'Mission Hill K-8'. Verify current operating status with BPS."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/mission-hill-k-8",
        ],
    },
    {
        "name": "Margarita Muniz Academy",
        "address": "20 Child St",
        "neighborhood": "Jamaica Plain",
        "zipcode": "02130",
        "school_type": ["dual_language", "high_school"],
        "grades_served_text": "7-12",
        "program_tags": ["dual_language", "early_college"],
        "language_programs": ["dual language (English/Spanish)"],
        "special_features": [
            "Dual language high school (English/Spanish)",
            "Early College starting in Grade 10",
            "Citywide high school",
        ],
        "notes": (
            "Margarita Muñiz Academy (also listed as Muniz, Margarita Academy) is a dual "
            "language high school serving grades 7-12 at the Agassiz building. It offers "
            "Early College programming starting in grade 10."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/muniz-margarita-academy",
        ],
    },

    # ── HYDE PARK ──────────────────────────────────────────────────────────

    {
        "name": "Roosevelt Upper (2-7)",
        "address": "95 Needham Road",
        "neighborhood": "Hyde Park",
        "zipcode": "02136",
        "school_type": ["traditional"],
        "grades_served_text": "2-7",
        "program_tags": [],
        "language_programs": [],
        "special_features": [
            "Upper division of the Roosevelt K-8 School",
        ],
        "notes": (
            "Roosevelt Upper School (grades 2-7) in Hyde Park is a division of the "
            "Roosevelt K-8 School."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/roosevelt-upper",
        ],
    },
    {
        "name": "Roosevelt K-8 (K1-1)",
        "address": "30 Millstone Road",
        "neighborhood": "Hyde Park",
        "zipcode": "02136",
        "school_type": ["traditional"],
        "grades_served_text": "K1-1",
        "program_tags": [],
        "language_programs": [],
        "special_features": [
            "Lower division of the Roosevelt K-8 School",
        ],
        "notes": (
            "Roosevelt K-8 Lower (K1-Grade 1) at the New Roosevelt building in Hyde Park."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/roosevelt-k-8",
        ],
    },
    {
        "name": "Channing Elementary",
        "address": "35 Sunnyside Street",
        "neighborhood": "Hyde Park",
        "zipcode": "02136",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Neighborhood elementary in Hyde Park.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/channing-elementary",
        ],
    },
    {
        "name": "Grew Elementary",
        "address": "40 Gordon Avenue",
        "neighborhood": "Hyde Park",
        "zipcode": "02136",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Neighborhood elementary in Hyde Park.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/grew-elementary",
        ],
    },
    {
        "name": "New Mission High",
        "address": "655 Metropolitan Ave",
        "neighborhood": "Hyde Park",
        "zipcode": "02136",
        "school_type": ["pilot"],
        "grades_served_text": "9-12",
        "program_tags": ["pilot"],
        "language_programs": [],
        "special_features": [
            "Pilot high school",
            "Citywide high school",
        ],
        "notes": (
            "New Mission High School is a BPS pilot high school located in Hyde Park."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/new-mission-high",
        ],
    },
    {
        "name": "Community Leadership Academy",
        "address": "655 Metropolitan Ave",
        "neighborhood": "Hyde Park",
        "zipcode": "02136",
        "school_type": ["horace_mann_charter"],
        "grades_served_text": "6-12",
        "program_tags": ["horace_mann_charter"],
        "language_programs": [],
        "special_features": [
            "Boston Community Leadership Academy",
            "In-district charter school",
        ],
        "notes": (
            "Boston Community Leadership Academy (in-district charter / Horace Mann) "
            "shares the Hyde Park EC building with New Mission High."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/community-leadership-academy",
        ],
    },

    # ── WEST ROXBURY ───────────────────────────────────────────────────────

    {
        "name": "West Roxbury Academy",
        "address": "1205 V.F.W. Parkway",
        "neighborhood": "West Roxbury",
        "zipcode": "02132",
        "school_type": ["traditional"],
        "grades_served_text": "9-12",
        "program_tags": [],
        "language_programs": [],
        "special_features": [
            "Citywide high school",
        ],
        "notes": "West Roxbury Academy is a citywide BPS high school in West Roxbury.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/west-roxbury-academy",
        ],
    },
    {
        "name": "Urban Science Academy",
        "address": "1205 V.F.W. Parkway",
        "neighborhood": "West Roxbury",
        "zipcode": "02132",
        "school_type": ["pilot"],
        "grades_served_text": "9-12",
        "program_tags": ["pilot", "STEM"],
        "language_programs": [],
        "special_features": [
            "Pilot high school with science focus",
            "Shares building with West Roxbury Academy",
        ],
        "notes": (
            "Urban Science Academy is a BPS pilot high school sharing the West Roxbury "
            "Education Complex with West Roxbury Academy."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/urban-science-academy",
        ],
    },
    {
        "name": "Kilmer Upper (4-8)",
        "address": "140 Russett Road",
        "neighborhood": "West Roxbury",
        "zipcode": "02132",
        "school_type": ["traditional"],
        "grades_served_text": "4-8",
        "program_tags": [],
        "language_programs": [],
        "special_features": [
            "Upper division of Kilmer K-8 School",
        ],
        "notes": "Kilmer K-8 Upper School (grades 4-8) in West Roxbury.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/kilmer-k-8",
        ],
    },
    {
        "name": "Kilmer Lower (K1-3)",
        "address": "35 Baker Street",
        "neighborhood": "West Roxbury",
        "zipcode": "02132",
        "school_type": ["traditional"],
        "grades_served_text": "K1-3",
        "program_tags": [],
        "language_programs": [],
        "special_features": [
            "Lower division of Kilmer K-8 School",
        ],
        "notes": "Kilmer K-8 Lower School (K1-Grade 3) in West Roxbury.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/kilmer-k-8",
        ],
    },
    {
        "name": "Beethoven Elementary",
        "address": "5125 Washington Street",
        "neighborhood": "West Roxbury",
        "zipcode": "02132",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Neighborhood elementary in West Roxbury.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/beethoven-elementary",
        ],
    },
    {
        "name": "Lyndon K-8",
        "address": "20 Mt. Vernon Street",
        "neighborhood": "West Roxbury",
        "zipcode": "02132",
        "school_type": ["pilot"],
        "grades_served_text": "K-8",
        "program_tags": ["pilot"],
        "language_programs": [],
        "special_features": [
            "Pilot K-8 school",
        ],
        "notes": "Lyndon K-8 Pilot School in West Roxbury.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/lyndon-k-8",
        ],
    },
    {
        "name": "Ohrenberger Elementary",
        "address": "175 West Boundary Road",
        "neighborhood": "West Roxbury",
        "zipcode": "02132",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [
            "Gifted & Talented program (per GreatSchools)",
        ],
        "notes": (
            "William H. Ohrenberger School in West Roxbury offers a Gifted & Talented "
            "program and serves PK-6."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/ohrenberger-elementary",
            "https://www.greatschools.org/massachusetts/boston/328-William-H-Ohrenberger/",
        ],
    },
    {
        "name": "Another Course to College",
        "address": "20 Warren Street",
        "neighborhood": "Brighton",
        "zipcode": "02135",
        "school_type": ["pilot"],
        "grades_served_text": "9-12",
        "program_tags": ["pilot", "alternative"],
        "language_programs": [],
        "special_features": [
            "Pilot high school with alternative/project-based model",
            "Citywide high school",
        ],
        "notes": (
            "Another Course to College (ACC) is a BPS pilot high school at the Taft "
            "building in Brighton. Note: BPS announced closure of ACC; verify current status."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/another-course-to-college",
            "https://www.bostonpublicschools.org/about-bps/capital-planning/closures/acc",
        ],
    },
    {
        "name": "Boston Green Academy",
        "address": "20 Warren Street",
        "neighborhood": "Brighton",
        "zipcode": "02135",
        "school_type": ["horace_mann_charter"],
        "grades_served_text": "6-12",
        "program_tags": ["horace_mann_charter", "sustainability"],
        "language_programs": [],
        "special_features": [
            "Horace Mann Charter School focused on environmental sustainability",
            "Formerly Odyssey High School",
        ],
        "notes": (
            "Boston Green Academy Horace Mann Charter School focuses on environmental "
            "sustainability and serves grades 6-12 at the Taft building in Brighton. "
            "Formerly Odyssey High School."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/boston-green-academy",
        ],
    },

    # ── BRIGHTON / ALLSTON ─────────────────────────────────────────────────

    {
        "name": "Edison K-8",
        "address": "60 Glenmont Road",
        "neighborhood": "Brighton",
        "zipcode": "02135",
        "school_type": ["traditional"],
        "grades_served_text": "K-8",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Edison K-8 School in Brighton.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/edison-k-8",
        ],
    },
    {
        "name": "Lyon K-8",
        "address": "50 Beechcroft Street",
        "neighborhood": "Brighton",
        "zipcode": "02135",
        "school_type": ["traditional"],
        "grades_served_text": "K-8",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Mary Lyon K-8 School in Brighton.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/lyon-k-8",
        ],
    },
    {
        "name": "Lyon, Mary 9-12",
        "address": "95 Beechcroft Street",
        "neighborhood": "Brighton",
        "zipcode": "02135",
        "school_type": ["pilot"],
        "grades_served_text": "9-12",
        "program_tags": ["pilot"],
        "language_programs": [],
        "special_features": [
            "Mary K. Lyon Pilot High School",
            "Citywide high school",
        ],
        "notes": (
            "Mary K. Lyon Pilot High School (9-12) in Brighton. Note: BPS announced "
            "closure of Mary Lyon Pilot High School; verify current status."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/lyon-high-school",
            "https://www.bostonpublicschools.org/about-bps/capital-planning/closures/mary-lyon",
        ],
    },
    {
        "name": "Winship Elementary",
        "address": "54 Dighton Street",
        "neighborhood": "Brighton",
        "zipcode": "02135",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Neighborhood elementary in Brighton.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/winship-elementary",
        ],
    },
    {
        "name": "Brighton High",
        "address": "25 Warren Street",
        "neighborhood": "Brighton",
        "zipcode": "02135",
        "school_type": ["traditional"],
        "grades_served_text": "9-12",
        "program_tags": [],
        "language_programs": [],
        "special_features": [
            "First BPS secondary school to earn Special Olympics National Banner (2024-2025)",
            "Citywide high school",
        ],
        "notes": (
            "Brighton High School serves grades 9-12 and made history in 2024-2025 as "
            "the first secondary school in BPS to earn Special Olympics National Banner "
            "recognition for inclusive sports and community."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/brighton-high-school",
        ],
    },
    {
        "name": "Baldwin ELPA",
        "address": "121 Corey Road",
        "neighborhood": "Brighton",
        "zipcode": "02135",
        "school_type": ["early_education", "pilot"],
        "grades_served_text": "K0-K2",
        "program_tags": ["early_childhood", "pilot"],
        "language_programs": [],
        "special_features": [
            "Baldwin Early Learning Pilot Academy",
            "Early education pilot program",
        ],
        "notes": (
            "Baldwin Early Learning Pilot Academy (ELPA) in Brighton is an early "
            "education pilot school serving K0-K2."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/baldwin-elpa",
        ],
    },
    {
        "name": "Horace Mann",
        "address": "40 Armington Street",
        "neighborhood": "Allston",
        "zipcode": "02134",
        "school_type": ["inclusion"],
        "grades_served_text": "PK-12",
        "program_tags": ["special_education", "deaf_hard_of_hearing"],
        "language_programs": [],
        "special_features": [
            "School for the Deaf and Hard of Hearing",
            "First Deaf principal in 151 years appointed recently",
            "Citywide specialized program",
        ],
        "notes": (
            "Horace Mann School for the Deaf and Hard of Hearing serves PK-12 students "
            "who are deaf or hard of hearing. In 2025, Dr. Michelle Eisan-Smith became "
            "the school's first Deaf principal in 151 years."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/horace-mann",
        ],
    },
    {
        "name": "Jackson/Mann K-8",
        "address": "40 Armington Street",
        "neighborhood": "Allston",
        "zipcode": "02134",
        "school_type": ["traditional"],
        "grades_served_text": "K-8",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": (
            "Jackson/Mann K-8 School in Allston shares the Jackson Mann building with "
            "Horace Mann School. Note: Wikipedia lists Jackson/Mann as closed in 2022; "
            "verify current status with BPS, as it appears in the 2024-2025 CSV."
        ),
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/jacksonmann-k-8",
        ],
    },
    {
        "name": "Gardner Elementary",
        "address": "30 Athol Street",
        "neighborhood": "Allston",
        "zipcode": "02134",
        "school_type": ["traditional"],
        "grades_served_text": "PK-6",
        "program_tags": [],
        "language_programs": [],
        "special_features": [],
        "notes": "Gardner Pilot Academy / Gardner Elementary in Allston.",
        "last_verified": "2026-03-14",
        "sources": [
            "https://www.bostonpublicschools.org/schools-container/school-profile/gardner-elementary",
        ],
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# SEI LANGUAGE-SPECIFIC PROGRAMS
# From official BPS SEI page, verified 2026-03-14
# ─────────────────────────────────────────────────────────────────────────────

SEI_LANGUAGE_SPECIFIC_EXAMPLES = [
    {
        "language": "Chinese",
        "schools": ["Harvard/Kent Elementary", "Quincy Lower (K-5)", "Charlestown High School"],
        "last_verified": "2026-03-14",
        "sources": [DISTRICT_SOURCES["sei_language_specific"]],
    },
    {
        "language": "Cape Verdean Creole",
        "schools": ["Burke High School", "Dearborn STEM Academy", "Orchard Gardens K-8"],
        "last_verified": "2026-03-14",
        "sources": [DISTRICT_SOURCES["sei_language_specific"]],
    },
    {
        "language": "Haitian Creole",
        "schools": [
            "Community Academy of Science and Health",
            "Ellison/Parks ELC (Mattapan)",
            "Taylor Elementary",
            "TechBoston Academy",
        ],
        "last_verified": "2026-03-14",
        "sources": [DISTRICT_SOURCES["sei_language_specific"]],
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# IMPORTANT OPERATIONAL NOTES
# Schools flagged as having open closure/merger/reconfiguration proceedings
# as of March 2026. Always verify current operating status before presenting
# to families.
# ─────────────────────────────────────────────────────────────────────────────

BPS_STRUCTURAL_CHANGES = [
    {
        "id": "clap_winthrop_merger",
        "affected_schools": ["Clap Elementary", "Winthrop Elementary"],
        "change_type": "merger",
        "new_entity": "Lilla G. Frederick Elementary School",
        "notes": "BPS capital planning references a merger of Clap and Winthrop into the Lilla G. Frederick Elementary School.",
        "source": "https://www.bostonpublicschools.org/about-bps/capital-planning/mergers/frederick",
    },
    {
        "id": "philbrick_sumner_merger",
        "affected_schools": ["Philbrick Elementary", "Sumner Elementary"],
        "change_type": "merger",
        "new_entity": "Sarah Roberts Elementary School",
        "notes": "BPS merged Philbrick and Sumner into Sarah Roberts Elementary School for 2025-26.",
        "source": "https://www.bostonpublicschools.org/about-bps/newsroom/news-blog",
    },
    {
        "id": "henderson_reconfiguration",
        "affected_schools": ["Henderson Lower (K-3)", "Henderson Upper (4-12)"],
        "change_type": "reconfiguration",
        "notes": "Henderson Inclusion School underwent a grade reconfiguration. See BPS capital planning page.",
        "source": "https://www.bostonpublicschools.org/about-bps/capital-planning/reconfigurations/henderson",
    },
    {
        "id": "closure_excel_high",
        "affected_schools": ["Excel High"],
        "change_type": "closure",
        "notes": "BPS announced closure proceedings for Excel High School.",
        "source": "https://www.bostonpublicschools.org/about-bps/capital-planning/closures/excel",
    },
    {
        "id": "closure_dever",
        "affected_schools": ["Dever Elementary"],
        "change_type": "closure",
        "notes": "BPS announced closure proceedings for Dever Elementary.",
        "source": "https://www.bostonpublicschools.org/about-bps/capital-planning/closures/dever",
    },
    {
        "id": "closure_cash",
        "affected_schools": ["Comm Acad Sci Health"],
        "change_type": "closure",
        "notes": "BPS announced closure proceedings for Community Academy of Science and Health.",
        "source": "https://www.bostonpublicschools.org/about-bps/capital-planning/closures/cash",
    },
    {
        "id": "closure_acc",
        "affected_schools": ["Another Course to College"],
        "change_type": "closure",
        "notes": "BPS announced closure of Another Course to College.",
        "source": "https://www.bostonpublicschools.org/about-bps/capital-planning/closures/acc",
    },
    {
        "id": "closure_mary_lyon",
        "affected_schools": ["Lyon, Mary 9-12"],
        "change_type": "closure",
        "notes": "BPS announced closure of Mary Lyon Pilot High School.",
        "source": "https://www.bostonpublicschools.org/about-bps/capital-planning/closures/mary-lyon",
    },
    {
        "id": "closure_lee_academy",
        "affected_schools": ["Lee Academy"],
        "change_type": "closure",
        "notes": "BPS announced closure of Lee Academy Pilot School.",
        "source": "https://www.bostonpublicschools.org/about-bps/capital-planning/closures/laps",
    },
]
