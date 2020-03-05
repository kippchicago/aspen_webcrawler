from utils import StudentAttendance
import credentials


ascend_attendance = StudentAttendance()
ascend_attendance.login_aspen_website(credentials.ASPEN_USERNAME, credentials.ASPEN_PASSWORD)
ascend_attendance.select_view("school")
ascend_attendance.select_school("one")
ascend_attendance.select_tab("Student")
ascend_attendance.select_filter('active')
one_attendance_active = ascend_attendance.pull_attendance_report()

one_attendance_active.to_csv('../data/one_attendance_active.csv',
                                index=False)