from utils import StudentIdentifyingInfo
import credentials

# StudentIdentifyingInfo Class
ascend_students = StudentIdentifyingInfo()

ascend_students.login_aspen_website(credentials.ASPEN_USERNAME, credentials.ASPEN_PASSWORD)
ascend_students.select_view("school")
ascend_students.select_school("bloom")
ascend_students.select_tab("Student")
ascend_report = ascend_students.build_quick_report_students_tab(["Last name", "First name", "State ID"])

ascend_report.to_csv('../data/ascend_report.csv')

