from utils import StudentIdentifyingInfo

import credentials

# StudentIdentifyingInfo Class
ascend_students = StudentIdentifyingInfo()

ascend_students.login_aspen_website(credentials.ASPEN_USERNAME, credentials.ASPEN_PASSWORD)
ascend_students.select_view("school")
ascend_students.select_school("bloom")
ascend_report = ascend_students.build_report_students_tab()

<<<<<<< HEAD
ascend_report.to_csv("../data/ascend_report.csv")
=======
ascend_report.to_csv("ascend_report.csv")
>>>>>>> dce66f06cde778874b7f172dcb960831af1c101c
