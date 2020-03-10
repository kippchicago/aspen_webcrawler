from utils import StudentAttendance
import credentials

student_attendance = StudentAttendance()

student_attendance.login_aspen_website(credentials.ASPEN_USERNAME,
                                      credentials.ASPEN_PASSWORD)
student_attendance.select_view('school')
student_attendance.select_school('ascend')
student_attendance.select_tab('Student')
student_attendance.select_filter('former')
report = student_attendance.pull_attendance_report()

report.to_csv('../data/attendance_ascend_former.csv',
              index=False)