import time
import glob
import os
import getpass
import selenium
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver


#This Question is used use to determine which day is updated.
provided = int(input("What Day is it?, Options are 1-5 which represent M-F          "))


# New Jira filters to get tickets per day!
#         (user, dateFrom, dateTo)
#         (jsmith, "2018/06/01", "2018/08/31")
friday = datetime.date.today()
thursday1 = friday - datetime.timedelta(days=1)
thursday = str(thursday1)
wednesday = friday - datetime.timedelta(days=2)
tuesday = friday - datetime.timedelta(days=3)
monday = friday - datetime.timedelta(days=4)



#Grab's the current user and uses it to search in Jira for the tickets the user updated that day.
current_user = "adekal339"
#jira_filter_url = "https://ccp.sys.comcast.net/issues/?jql=issuekey%20in%20updatedBy(" + current_user + "%2C%20-14h)"
jira_filter_url = "https://ccp.sys.comcast.net/issues/?jql=issuekey%20in%20updatedBy(" + current_user + "," + thursday + "," + thursday + ")"




current_user = os.getlogin()
firefox_profiles_list = glob.glob("C:\\Users\\" + current_user + "\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\*") # * means all if need specific format then *.csv
firefox_profile = max(firefox_profiles_list, key=os.path.getmtime)
firefox_path = firefox_profile.split("\\")
final_firefox_path = "\\\\".join(firefox_path)

fp = webdriver.FirefoxProfile(final_firefox_path)
driver = webdriver.Firefox(fp)


driver.get(jira_filter_url)

#Attempt to replace time sleep with wait for presence of element to continue.
#time.sleep(5)
WebDriverWait(driver, 100).until(ec.presence_of_element_located((By.CLASS_NAME, "ui-sortable")))

main = driver.find_element_by_class_name("ui-sortable")

elems = main.find_elements_by_xpath("//a[@href]")
value = []
for elem in elems:
    value.append(elem.get_attribute("href"))


newvalue = set(value)
newestvalue = [k for k in newvalue if 'https://ccp.sys.comcast.net/browse/INFRA-' in k]
print(newestvalue)



