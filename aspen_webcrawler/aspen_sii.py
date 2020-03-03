from utils import StudentIdentifyingInfo

import credentials

# StudentIdentifyingInfo Class
ascend_students = StudentIdentifyingInfo()

ascend_students.login_aspen_website(credentials.ASPEN_USERNAME, credentials.ASPEN_PASSWORD)
ascend_students.select_view("school")
ascend_students.select_school("bloom")
ascend_report = ascend_students.build_report_students_tab()

ascend_report.to_csv("../data/ascend_report.csv")