# File to read in BPS csv data and create more narrative descriptions of each school for the chatbot to use as context
"""
Key Features:
- Reads BPS school data from a CSV file
- Cleans and processes the data
- Generates narrative descriptions for each school
Example Usage:
    # Run the script to generate cleaned data:
    python BPS_cleaner.py
    # This will create a new CSV file with cleaned and narrative descriptions for each school.
Inputs:
- A CSV file containing BPS school data with columns such as:
    - BLDG_ID (not used in the narrative, but can be included for reference)
    - BLDG_NAME (Useful in narrative for directions to the school)
    - ADDRESS (Useful in narrative for providing the school's location)
    - CITY (Useful in narrative for providing the school's location)
    - ZIPCODE (Useful in narrative for providing the school's location)
    - CSP_SCH_ID (not used in the narrative, but can be included for reference)
    - SCH_ID (not used in the narrative, but will be used for crawler to link to the correct school)
    - SCH_NAME (Useful in narrative for providing the school's name)
    - SCH_LABEL (Abbreviation of the school name, not used in the narrative)
    - SCH_TYPE (Useful in narrative for providing the type of school, e.g., "Elementary", "High School")
    - SHARED (Indicates if the school shares a building with another school, not used in the narrative)
    - COMPLEX (Indicates if the school is part of a complex, not used in the narrative)
    - shape_wkt (Not used in the narrative)
    - POINT_X (Not used in the narrative)
    - POINT_Y (Not used in the narrative)
"""
import pandas as pd

# Read the CSV file containing BPS school data
