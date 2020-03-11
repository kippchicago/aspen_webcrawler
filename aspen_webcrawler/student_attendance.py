from utils import StudentAttendance
import credentials

student_attendance = StudentAttendance()

student_attendance.login_aspen_website(secrets.ASPEN_USERNAME,
                                       secrets.ASPEN_PASSWORD)

student_attendance.select_view('school')
student_attendance.select_school('ascend')
student_attendance.select_tab('Student')
student_attendance.select_filter('active')
report = student_attendance.pull_attendance_report()

report.to_csv('../data/attendance_ascend_active.csv',
              index=False)
