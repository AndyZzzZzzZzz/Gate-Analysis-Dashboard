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
        Fetch the top 10 worst performing courses within a given subject.
        The courses are ranked by the highest number of students who received "D or less".
    """
    subject_data = raw_data[raw_data['Course Subject'] == subject]

    subject_data['Total Failed'] = subject_data['# D'] + subject_data['# F']
    top10 = subject_data.sort_values('Total Failed', ascending=False).head(10)
    
    failed_dict = {}
    top10_courses = set()
    failed_dict['Others'] = 0
    for _, row in top10.iterrows():
        course = row['Course Subject'] + row['Catalog Number']
        total_failed = int(row['Total Failed'])  # convert to Python int
        failed_dict[course] = total_failed
        top10_courses.add(course)

    # Sum 'Others'
    for _, row in subject_data.iterrows():
        course = row['Course Subject'] + row['Catalog Number']
        if course not in top10_courses:
            failed_dict['Others'] += int(row['Total Failed'])  
    
    return failed_dict


def get_faculty_data(faculty: str):

    pass

def get_course_data(course: str):
    pass

def get_population_data():
    pass
    