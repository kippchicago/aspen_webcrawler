import pandas as pd
import time

from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.support.ui import Select

class AspenWebcrawlerCPS(object):

    def __init__(self):
        # Set Website to Crawl
        url = "https://aspen.cps.edu/aspen/logon.do"

        # ---------REGULAR BROWSER---------------------------------
        # self.browser = webdriver.Chrome('/usr/local/bin/chromedriver')
        #
        # ---------HEADLESS BROWSER---------------------------------
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('headless')
        self.browser = webdriver.Chrome('/usr/local/bin/chromedriver',
                                        chrome_options=chrome_options
                                        )
        # ---------NAVIGATE TO WEBSITE---------------------------------
        self.browser.get(url)

    def login_aspen_website(self, aspen_username, aspen_password):
        """

        :param aspen_username: This is the same CPS username used to log into cps email address
        :param aspen_password: This is the same CPS password used to log into cps email address
        :return: will log you into aspen website
        """
        time.sleep(1)

        # fill in username and Password and click submit
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

        self.browser.find_element_by_xpath(
            '//*[@id="header"]/table[1]/tbody/tr/td[3]/div/table/tbody/tr/td[2]/div/a').click()

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

    def select_filter(self, student_group):
        """
        :student_group: (str) filter selection (either "active" which is "All Active Students" or "former" which is "Former Students"
        :return:
        """

        # choose either active or former students
        self.browser.find_element_by_id("filterMenu").click()

        time.sleep(1)

        if student_group.lower() == "active":
            self.browser.find_element_by_xpath('//*[@id="filterMenu_Option1"]/td[2]').click()
        elif student_group.lower() == "former":
            self.browser.find_element_by_xpath('//*[@id="filterMenu_Option7"]/td[2]').click()
        else:
            raise Exception("Not a valid selection")


class StudentIdentifyingInfo(AspenWebcrawlerCPS):

    def __init__(self):
        AspenWebcrawlerCPS.__init__(self)

    def build_quick_report_students_tab(self, selection_list):
        """

        :selection_list: (list) list of report parameters you would like to choose
        :return:
        """

        # click report menu
        self.browser.find_element_by_xpath('//*[@id="reportsMenu"]').click()

        # switch windows (quick report opens up new window)
        window_before = self.browser.window_handles[0]

        # select "quick report"
        self.browser.find_element_by_xpath(
            '/html/body/form/table/tbody/tr[2]/td/div/table[2]/tbody/tr[1]/td[2]/table[1]/tbody/tr/td[2]/div[2]/table[1]/tbody/tr[24]/td[2]').click()
        window_after = self.browser.window_handles[1]
        self.browser.switch_to.window(window_after)

        # click next button twice
        self.browser.find_element_by_id("wizNextButton").click()
        self.browser.find_element_by_id("wizNextButton").click()

        # Remove all fields that are already in selected field.
        select = Selector(text=self.browser.page_source)
        selected_fields = select.xpath('//*[@id="selectedFieldIds"]/option//text()').extract()

        # collect list of all fields in "Selected Fields"
        selected_fields_converted = []
        for element in selected_fields:
            selected_fields_converted.append(element.strip())

        select = Select(self.browser.find_element_by_xpath('//*[@id="selectedFieldIds"]'))

        # Remove element from list that you would like to leave in selected field
        # NOTE: This is done because 'School > Name' does not appear in available field if removed
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
        custom_report = pd.read_html(content, flavor='html5lib', header=0)[0]

        return custom_report


class StudentAttendance(AspenWebcrawlerCPS):

    def __init__(self):
        AspenWebcrawlerCPS.__init__(self)

    def _cleanAttendance(self, attendance_file):
        """

        :param attendance_file:
        :return:
        """

        # Drop empty rows
        attendance_file.dropna(subset=['Student.1'], inplace=True)

        # Chose subset of columns to keep
        attendance_file = attendance_file[
            ['Student', 'Grade', 'Homeroom', 'Member', 'Present', 'Absent', 'Tardy', 'Dismiss']]

        # filter out renments of excel pagination
        attendance_file = attendance_file.loc[attendance_file['Student'] != "CHARTER"]
        attendance_file = attendance_file.loc[attendance_file['Student'] != "Student"]
        attendance_file = attendance_file.loc[~attendance_file['Student'].str.contains("Page [0-9]", regex=True)]

        return (attendance_file)

    def pull_attendance_report(self):
        """

        :return:
        """

        # click report menu
        self.browser.find_element_by_xpath('//*[@id="reportsMenu"]').click()

        # switch windows (quick report opens up new window)
        window_before = self.browser.window_handles[0]

        # click Student Membership under report menu
        self.browser.find_element_by_xpath('//*[@id="reportsMenu_Option11"]/td[2]').click()
        window_after = self.browser.window_handles[1]
        self.browser.switch_to.window(window_after)

        # Format: Select CSV
        self.browser.find_element_by_id('format').click()
        self.browser.find_element_by_xpath('//*[@id="format"]/option[2]').click()

        # Students to include: Select all students
        # self.browser.find_element_by_xpath('// *[ @ id = "tab_0"] / td[2] / select').click()
        # self.browser.find_element_by_xpath('//*[@id="tab_0"]/td[2]/select/option[2]').click()


        # click run
        self.browser.find_element_by_xpath(
            '/html/body/table/tbody/tr[2]/td/form/table/tbody/tr[5]/td/button[1]').click()

        window_final = self.browser.window_handles[1]
        self.browser.switch_to.window(window_final)

        time.sleep(3)

        content = self.browser.page_source

        # read in html table to pd.dataframe
        custom_report = pd.read_html(content,
                                     flavor='html5lib',
                                     header=13)[0]

        custom_report_clean = self._cleanAttendance(custom_report)

        return (custom_report_clean)
