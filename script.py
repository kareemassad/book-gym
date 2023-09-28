from selenium import webdriver
from datetime import date, timedelta
import sys

# Gym Location; Currently supports "grc" or "rrc"
gym_name: str = "grc"
# Party_count; Currently supports 1 or 2
party_count: int = 2
# Duration; Default 60
duration: int = 60
# days booking ahead; Default 2
days_ahead: int = 2
# Options: 8:15 PM, 7:00 PM, 5:45 PM, 4:30 PM, 3:15 PM, 2:00 PM, 12:00 PM, 10:45 AM, 9:30 AM, 8:15 AM, 7:00 AM.
desired_time: str = "8:15 PM"

# today's date; output style: Friday October 1, 2021
today = date.today()
today_date = today.strftime("%A %B %d, %Y")
# target date will be 2 days from today. Ex. if today is 2020-09-29, target date will be 2020-10-01
# tar_style = "Friday October 1, 2021"
target_date = (today + timedelta(days=days_ahead)).strftime("%A %B %#d, %Y")


if gym_name == "grc":
    gym_name = "Goulburn Recreation Centre"
    gym_url = "https://reservation.frontdesksuite.ca/rcfs/cardelrec/Home/Index?pageid=a10d1358-60a7-46b6-b5e9-5b990594b108&culture=en&uiculture=en"

elif gym_name == "rrc":
    gym_name = "Richcraft Recreation Complex"
    gym_url = "https://reservation.frontdesksuite.ca/rcfs/richcraftkanata/Home/Index?pageid=b3b9b36f-8401-466d-b4c4-19eb5547b43a&culture=en&uiculture=en"
else:
    sys.exit("Invalid gym target")

# NOTE: Will have at this point: gym_name, gym_url, party_count, duration, today_date, target_date

# pick browser
driver = webdriver.Chrome("chromedriver\chromedriver.exe")
# pick site being used
driver.get(gym_url)

# Pick "Cardio and weight room – 60 minutes"
element = driver.find_element_by_xpath(
    '//div[@class="content"][.="Cardio and weight room – 60 minutes"]'
).click()

# "How many people in your group?"
party_count_element = driver.find_element_by_xpath('//input[@name="ReservationCount"]')
# default is 1
curr_party_count = party_count_element.get_attribute("value")

# Ensure the party count is correct
if party_count == curr_party_count:
    print("Party count is set correctly")
else:
    driver.execute_script(
        "arguments[0].value = arguments[1];", party_count_element, party_count
    )

# Submit group size
driver.find_element_by_xpath('//button[@id="submit-btn"]').click()

# div with class = "date-text" then span with class = "header-text".
target_date_element = driver.find_element_by_xpath(
    f'//div[@class="date-text"]//span[@class="header-text"][.="{target_date}"]'
)
# Open dropdown menu
target_date_element.click()

print(target_date_element.text)

date_box_element = driver.find_element_by_xpath(
    f'//a[@class="mdc-button mdc-button--unelevated time-container mdc-ripple-upgraded"]//span[@class="mdc-button__label available-time"][.="{desired_time}"]'
)
date_box_element.click()
# date_box_element = driver.find_element_by_xpath(
#     "//*[contains(text(), '" + target_date + "')] | //*[@value='" + target_date + "']"
# )

# print("date_box_element")
# print(date_box_element)
# date_box_element.click()
