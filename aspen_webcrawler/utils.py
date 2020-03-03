import pandas as pd
from selenium import webdriver  # open webdriver for specific browser
from selenium.webdriver.common.keys import Keys  # for necessary browser action
from selenium.webdriver.common.by import By  # For selecting html code
from selenium.webdriver.support.ui import Select
import scrapy
from scrapy import Selector
from scrapy.linkextractors import LinkExtractor
import time

def say_hi():
    print("hi misa!")


class StudentIdentifyingInfo:

    def __init__(self):
        # Go to ASPEN Website
        url = "https://aspen.cps.edu/aspen/logon.do"

        self.browser = webdriver.Chrome('/usr/local/bin/chromedriver')
        # browser = webdriver.PhantomJS()
        # browser.get("https://python.org/")

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

    def build_report_students_tab(self):
        """

        :return:
        """

        # click students tab
        self.browser.find_element_by_xpath('//*[@id="topTabs"]/tr/td[5]/a').click()
        time.sleep(3)

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

        # Choose unwanted elements in the selected field
        select = Select(self.browser.find_element_by_xpath('//*[@id="selectedFieldIds"]'))

        select.select_by_visible_text("Name")
        select.select_by_visible_text("Address")
        select.select_by_visible_text("Calendar")
        select.select_by_visible_text("Enrollment status")
        select.select_by_visible_text("Grade level")
        select.select_by_visible_text("Homeroom")
        select.select_by_visible_text("Year of graduation")
        select.select_by_visible_text("Alerts")
        select.select_by_visible_text("Quick status")
        select.select_by_visible_text("Alerts")

        # remove unwated elements in the "selected field"
        self.browser.find_element_by_id("removeButton").click()

        # choose elements in the avaialbe field
        select = Select(self.browser.find_element_by_xpath('//*[@id="availableFieldIds"]'))

        select.select_by_visible_text("Last name")
        select.select_by_visible_text("First name")
        select.select_by_visible_text("State ID")

        # Add elements from available to selected field
        self.browser.find_element_by_id("addButton").click()

        # Hit next button three times
        self.browser.find_element_by_id("wizNextButton").click()
        self.browser.find_element_by_id("wizNextButton").click()
        self.browser.find_element_by_id("wizNextButton").click()

        # Click the finish button and switch to new popup window
        self.browser.find_element_by_id("finishButton").click()
        window_final = self.browser.window_handles[1]
        self.browser.switch_to.window(window_final)

        sel = Selector(text=self.browser.page_source)

        # select the entire table (with all student data )
        table = sel.xpath('/html/body/table/tbody')

        # put all data into dictionary
        data = []
        for row in table.xpath('/html/body/table/tbody/tr'):
            student_id = row.xpath('td[1]//text()').extract_first()
            dob = row.xpath('td[2]//text()').extract_first()
            organization_2_name = row.xpath('td[3]//text()').extract_first()
            school_name = row.xpath('td[4]//text()').extract_first()
            last_name = row.xpath('td[5]//text()').extract_first()
            first_name = row.xpath('td[6]//text()').extract_first()
            sasid = row.xpath('td[7]//text()').extract_first()

            person = {"student_id": student_id,
                      "dob": dob,
                      "organization_2_name": organization_2_name,
                      "school_name": school_name,
                      "last_name": last_name,
                      "first_name": first_name,
                      "sasid": sasid}

            data.append(person)

        # Change dictionary into dataframe
        custom_report = pd.DataFrame(data[1:])

        return custom_report
