import pandas as pd
from selenium import webdriver
import numpy as np
from selenium.webdriver.common.keys import Keys  # for necessary browser action
from selenium.webdriver.common.by import By  # For selecting html code
from selenium.webdriver.support.ui import Select
import scrapy
from scrapy import Selector
from scrapy.linkextractors import LinkExtractor
import time
import html5lib
from bs4 import BeautifulSoup

class StudentIdentifyingInfo:

    def __init__(self):
        # Go to ASPEN Website
        url = "https://aspen.cps.edu/aspen/logon.do"

        self.browser = webdriver.Chrome('/usr/local/bin/chromedriver')

        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('headless')

        # self.browser = webdriver.Chrome('/usr/local/bin/chromedriver',
        #                                 chrome_options=chrome_options
        #                                 )
        # navigate to the webpage
        self.browser.get(url)

    def login_aspen_website(self, aspen_username, aspen_password):
        """

        :param aspen_username: This is the same CPS username used to log into cps email address
        :param aspen_password: This is the same CPS password used to log into cps email address
        :return: will log you into aspen website
        """

        # Put in username and Password and click submit
        username = self.browser.find_element_by_name("username")
        username.clear()
        username.send_keys(aspen_username)

        password = self.browser.find_element_by_name("password")
        password.clear()
        password.send_keys(aspen_password)
        self.browser.find_element_by_id("logonButton").click()

        time.sleep(2)

    def select_view(self, view):
        """

        :param view: (str) this parameter takes one of three strings - "school", "staff" or "health".
        :return: will navigate to chosen view in aspen.
        """
        # Selects view button

        self.browser.find_element_by_id("contextMenu").click()

        if view.lower() == "school":
            self.browser.find_element_by_id("contextSchool").click()

        elif view.lower() == "health":
            self.browser.find_element_by_id("contextHealth").click()

        elif view.lower() == "staff":
            self.browser.find_element_by_id("contextStaff").click()
        else:
            raise Exception("Incorrect Selection: must choose 'school', 'health', or 'staff', view")

    def select_school(self, school):
        """

        :param school: this parameter takes one of four strings - "ACADEMY", "ASCEND", "BLOOM" or "ONE"
        :return: wll navigate to that school page
        """
        window_before = self.browser.window_handles[0]

        self.browser.find_element_by_xpath('//*[@id="header"]/table[1]/tbody/tr/td[3]/div/table/tbody/tr/td[2]/div/a').click()

        window_after = self.browser.window_handles[1]
        self.browser.switch_to.window(window_after)

        time.sleep(2)

        if school.lower() == "academy":
            self.browser.find_element_by_id("skl01000000769").click()

        elif school.lower() == "ascend":
            self.browser.find_element_by_id("skl01000000088").click()

        elif school.lower() == "bloom":
            self.browser.find_element_by_id("skl01000000817").click()
        elif school.lower() == "one":
            self.browser.find_element_by_id("skl01000000853").click()
        else:
            raise Exception("Incorrect Selection: must choose academy, ascend, bloom, or one")

        self.browser.find_element_by_id("okButton").click()

        self.browser.switch_to.window(window_before)

    def select_tab(self, top_tab_selection):
        """

        :param top_page_tab: (str) can choose one of the top tabs in the school view.
        :return: Navigates to a tab within school view
        """
        time.sleep(2)

        self.browser.find_element_by_id("topTabs")
        self.browser.find_element_by_link_text(top_tab_selection.capitalize()).click()

        time.sleep(2)


    def build_quick_report_students_tab(self, student_group, selection_list):
        """
        :student_group: (str) filter selection (either "active" which is All Active Students or "former" which is "Former Students"
        :selection_list: (list) list of report parameters you would like to choose
        :return:
        """

        # choose either active or former students
        self.browser.find_element_by_id("filterMenu").click()

        time.sleep(3)

        if student_group.lower() == "active":
            self.browser.find_element_by_xpath('//*[@id="filterMenu_Option1"]/td[2]').click()
        elif student_group.lower() == "former":
            self.browser.find_element_by_xpath('//*[@id="filterMenu_Option7"]/td[2]').click()
        else:
            raise Exception("Not a valid selection")


        # click report menu
        self.browser.find_element_by_xpath('//*[@id="reportsMenu"]').click()

        # switch windows (quick report opens up new window)
        window_before = self.browser.window_handles[0]
        self.browser.find_element_by_xpath('//*[@id="reportsMenu_Option24"]/td[2]').click()
        window_after = self.browser.window_handles[1]
        self.browser.switch_to.window(window_after)

        # click next button twice
        self.browser.find_element_by_id("wizNextButton").click()
        self.browser.find_element_by_id("wizNextButton").click()

        # Remove all fields that are already in selected field.
        select = Selector(text=self.browser.page_source)
        selected_fields = select.xpath('//*[@id="selectedFieldIds"]/option//text()').extract()

        selected_fields_converted = []
        for element in selected_fields:
            selected_fields_converted.append(element.strip())

        select = Select(self.browser.find_element_by_xpath('//*[@id="selectedFieldIds"]'))

        # leave in this field
        selected_fields_converted.remove('School > Name')

        for element in selected_fields_converted:
            select.select_by_visible_text(element)

        self.browser.find_element_by_id("removeButton").click()

        # Choose elements and add to selected field
        select = Select(self.browser.find_element_by_xpath('//*[@id="availableFieldIds"]'))

        for selection in selection_list:
            select.select_by_visible_text(selection)

        self.browser.find_element_by_id("addButton").click()

        # Hit next button three times
        self.browser.find_element_by_id("wizNextButton").click()
        self.browser.find_element_by_id("wizNextButton").click()
        self.browser.find_element_by_id("wizNextButton").click()

        # Click the finish button and switch to new popup window
        self.browser.find_element_by_id("finishButton").click()
        window_final = self.browser.window_handles[1]
        self.browser.switch_to.window(window_final)

        # find table and save to html
        self.browser.find_element_by_xpath('/html/body/table')
        content = self.browser.page_source

        # read in html table to pd.dataframe
        # the zero is on the end because the function reads a list of tables by default
        # since there is only one table we can just pick the first one
        custom_report = pd.read_html(content, flavor='html5lib', header=0)[0]

        # sel = Selector(text=self.browser.page_source)
        #
        # # select the entire table (with all student data )
        # table = sel.xpath('/html/body/table/tbody')
        #
        # # put all data into dictionary
        # selection_list.insert(0, 'School > Name')
        # count = int(len(selection_list))
        # data = []
        # for row in table.xpath('/html/body/table/tbody/tr'):
        #     student_id = row.xpath('td[1]//text()').extract_first()

            # student_id = row.xpath('td[1]//text()').extract_first()
            # dob = row.xpath('td[2]//text()').extract_first()
            # organization_2_name = row.xpath('td[3]//text()').extract_first()
            # school_name = row.xpath('td[4]//text()').extract_first()
            # last_name = row.xpath('td[5]//text()').extract_first()
            # first_name = row.xpath('td[6]//text()').extract_first()
            # sasid = row.xpath('td[7]//text()').extract_first()

        #     person = {"student_id": student_id,
        #               "dob": dob,
        #               "organization_2_name": organization_2_name,
        #               "school_name": school_name,
        #               "last_name": last_name,
        #               "first_name": first_name,
        #               "sasid": sasid}
        #
        #     data.append(person)
        #
        # # Change dictionary into dataframe
        # custom_report = pd.DataFrame(data[1:])

        return custom_report


# ['Photo',
#  'Last name',
#  'First name',
#  'Middle name',
#  'Title',
#  'Suffix',
#  'Gender',
#  'Date of Birth',
#  'Globally Unique Identifier',
#  'Globally Unique Identifier 2',
#  'Phone 1',
#  'Globally Unique Identifier 3',
#  'Phone 2',
#  'Name',
#  'Phone 3',
#  'Address',
#  'Primary email-Correo electrónico primario',
#  'Student ID',
#  'Alternate email',
#  'State ID',
#  'Google Docs email',
#  'Year of graduation',
#  'Grade level',
#  'Contact',
#  'Homeroom',
#  'Student',
#  'Next homeroom',
#  'Staff',
#  'Homeroom teacher',
#  'User',
#  'Race',
#  'Enrollment status',
#  'Security code',
#  'Private',
#  'Registration Gateway access',
#  'Home Language',
#  'Phone 1 Type',
#  'Registration Gateway exported',
#  'Calendar',
#  'Phone 2 Type',
#  'Phone 3 Type',
#  'Phone 4 Type',
#  'Phone 5 Type',
#  'Used For Auto Notification',
#  'Used For Auto Notification Phone 2',
#  'Sped Status',
#  'Used For Auto Notification Phone 3',
#  'Used For Auto Notification Phone 4',
#  '504 Indicator',
#  'Used For Auto Notification Phone 5',
#  'Location Phone 1',
#  'Location Phone 2',
#  'Location Phone 3',
#  'Location Phone 4',
#  'Location Phone 5',
#  'Is Listed Phone 1',
#  'Is Listed Phone 2',
#  'Is Listed Phone 3',
#  'Academic track type',
#  'Is Listed Phone 4',
#  'Medicaid number',
#  'Is Listed Phone 5',
#  'Alerts',
#  'Hispanic or Latino',
#  'Quick status',
#  'Phone 4',
#  'Phone 5',
#  'BirthDate Verification',
#  'Graduation history notes',
#  'Citizenship Status',
#  'Goes By Gender',
#  'Ethnic Category',
#  'Native Language',
#  'Phone 1 Ext',
#  'Phone 2 Ext',
#  'Phone 3 Ext',
#  'Phone 4 Ext',
#  'Phone 5 ext',
#  'Legal Gender',
#  'Use Goes By or Legal First',
#  'Use Goes By or Legal Last',
#  'Use Goes By or Legal Gender',
#  'Portal Email Date',
#  'I agree',
#  'SMS Notification Number',
#  'HLS Locked',
#  'Constraint Social Science',
#  "Mother's Maiden Name",
#  'Goes By First',
#  'Legal Full Name',
#  'Goes By Middle',
#  'School Name Tag',
#  'Goes By Last',
#  'Email 3',
#  'Email 4',
#  'Legal First Name',
#  'Service Learning Hours',
#  'Legal Last Name',
#  'Use Goes By or Legal Middle',
#  'Promotion Status',
#  'Pronouns',
#  'Graduation Requirements Met',
#  'Legal Middle Name',
#  'GraduationDate',
#  'Primary Email Lock Field',
#  'Registration Grade Level',
#  'Zoned School',
#  'Deployed to Active Duty',
#  'Military Family',
#  'SAT Opt-In',
#  'Religious Exemption Vision',
#  'Religious Exemption Hearing',
#  'Apply for Illinois Medical Card/All Kids?',
#  'Dental Compliant',
#  'Health Exams Compliant',
#  'Next Zoned School',
#  'Banned from Selective Enrollment',
#  'Proof of Residency Provided',
#  'Glasses Provider',
#  'Birth Certificate on File',
#  'Hearing Compliant',
#  'Immunizations Compliant',
#  'Vision Screening Compliant',
#  'Reason for No Glasses',
#  'Graduation Requirements Met Date',
#  'Eligible For Graduation',
#  'Eligible For Graduation Date',
#  'Has Fmly Interest Health Ins',
#  'Has Health Insurance',
#  'CPS Insurance Option',
#  'Additional MedicalID',
#  'Dental Exception Reason',
#  'Dental Waiver Reason',
#  'Reason no hearing aid',
#  'Student Wears Glasses',
#  'Date Glasses Obtained',
#  'Can Call Ambulance',
#  'Can Call Doctor',
#  'Can Treat Medical',
#  'Has Medical Alert',
#  'Vision Exam Compliant',
#  'US Constitution Test',
#  'Weighted Year GPA',
#  'Year of 8th Grade Graduation',
#  'Semester 2 Term GPA',
#  'Constraint World Language',
#  'Semester 1 Term GPA',
#  'Constraint Science',
#  'Un-Weighted GPA',
#  'Weighted GPA',
#  'Weighted Class Rank',
#  'No English in Home',
#  'IEP Indicator',
#  'Medical Release on File',
#  'Doctor Phone Number',
#  'Student Does Not Speak English',
#  'Date Registered',
#  'Has Graduated',
#  'Home Address in School Area',
#  'Report Card Language',
#  'Food Stamp Number',
#  'Home Language Survey Date',
#  'Glasses Required',
#  'Years Immigrated',
#  'Medical Number',
#  'Year Entered 9th Grade',
#  'Original Enrollment Date',
#  'FRM Status',
#  'Hearing Device Code -R',
#  'Hearing Device Code -L',
#  'FRM Evaluation Date',
#  'FRM Status LY',
#  'Meets Grade Requirement',
#  'Meets Age Requirement',
#  'Meets Medical Requirement',
#  'Transfer Student',
#  'Prior Semester Earned Credit',
#  'Dental Compliance End Date',
#  'Health Exams Compliance End Date',
#  'Hearing Compliance End Date',
#  'Immunizations Compliance End Date',
#  'Vision Screening Compliance End Date',
#  'Vision Exam Compliance End Date',
#  'Religious Exemption - Health Exam',
#  'Health Exam Waiver',
#  'Constraint English',
#  'Constraint Math',
#  'SSMIdentifier',
#  'PROJECTION_ENROLLMENT_PROGRAM',
#  'Summer Homeroom',
#  'Doctor Name',
#  'Medical Alert Contact',
#  'Dentist Name',
#  'Dentist Phone',
#  'School Counselor',
#  'Diploma Type',
#  'Home School Exception Reason Other Comment',
#  'Next Zoned School Exception Reason',
#  'Doctor Address']