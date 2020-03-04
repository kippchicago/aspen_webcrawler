from utils import StudentIdentifyingInfo
import credentials

# StudentIdentifyingInfo Class
ascend_students = StudentIdentifyingInfo()

ascend_students.login_aspen_website(credentials.ASPEN_USERNAME, credentials.ASPEN_PASSWORD)
ascend_students.select_view("school")
ascend_students.select_school("ascend")
ascend_students.select_tab("Student")

selection_list = ["Last name", "First name", 'Date of Birth', "State ID", "Student ID"]
ascend_report = ascend_students.build_quick_report_students_tab(student_group='active',
                                                               selection_list=selection_list)

print(ascend_report)