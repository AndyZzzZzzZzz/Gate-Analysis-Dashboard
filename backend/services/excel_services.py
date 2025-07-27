import pandas as pd
import os 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, '..', 'data', 'gatekeeper_d_cutoff_202223.xlsx')
EXCEL_PATH = os.path.abspath(EXCEL_PATH)

# read in data and parse sheets
# all_hseet = {sheet_name: dataFrame ..}
excel_file = pd.ExcelFile (EXCEL_PATH)
all_sheets = pd.read_excel(excel_file, sheet_name = None)
raw_data = all_sheets['Raw Grade Data']




def get_worst_subjects_data(subject: str) -> dict:
    """
        Fetch the top 10 worst performing courses within a given subject
        The courses are ranked with their highest rates of "D or less" performance
    """
    subject_data = raw_data[raw_data['Course Subject'] == subject]

    subject_data['Fail Rate'] = (subject_data['# D'] + subject_data['# F'])/subject_data['Total #']
    top10 = subject_data.sort_values('Fail Rate', ascending=False).head(10)
    
    failrate_dict = {}
    failrate_dict['Others'] = 1
    for _, row in top10.iterrows():
        course = row['Course Subject'] + row['Catalog Number']
        failrate = row['Fail Rate']
        failrate_dict[course] = failrate
        failrate_dict['Others'] -= failrate
    
    return failrate_dict


def get_faculty_data(faculty: str):

    pass

def get_course_data(course: str):
    pass

def get_population_data():
    pass
    