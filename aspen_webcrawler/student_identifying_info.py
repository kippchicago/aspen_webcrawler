from utils import StudentIdentifyingInfo
import credentials

student_info = StudentIdentifyingInfo()

student_info.login_aspen_website(credentials.ASPEN_USERNAME,
                                      credentials.ASPEN_PASSWORD)
student_info.select_view('school')
student_info.select_school('ascend')
student_info.select_tab('Student')
student_info.select_filter('former')
report = student_info.build_quick_report_students_tab(['First name', 'Last name', 'Student ID', 'State ID', 'Grade', 'Homeroom'])

report.to_csv('../data/test.csv',
              index=False)