from httpcore import TimeoutException
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
import os

ACCOUNT_EMAIL = "silver@test.com"
ACCOUNT_PASSWORD = "7sYst6VWapcpK87"
GYM_URL = "https://appbrewery.github.io/gym/"

total_classes_booked = 0
waitlist_joined = 0
booked_now = 0
total_already_booked = 0

total_expected_bookings = 2 # Tuesday and Thursday 6pm classes
actual_bookings = 0

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

bot = webdriver.Chrome(options=chrome_options)

bot.implicitly_wait(5)
wait = WebDriverWait(bot, 10)
bot.get(GYM_URL)

def login():
    login_button = bot.find_element(By.CSS_SELECTOR, value="button.Navigation_button__uyKX2 ")
    login_button.click()

    email_input = bot.find_element(By.ID, value="email-input")
    email_input.send_keys(ACCOUNT_EMAIL)

    password_input = bot.find_element(By.ID, value="password-input")
    password_input.send_keys(ACCOUNT_PASSWORD)

    submit_button = bot.find_element(By.CLASS_NAME, value="Login_submitButton__tJFna ")
    submit_button.click()
    
    wait.until(ec.presence_of_element_located(By.ID, value="schedule-page"))
    

def retry(func, retries=7, description=None):
    for attempt in range(retries):
        print(f"Trying {description}. Attempt {attempt + 1}")
        try:
            return func()
        except TimeoutException as e:
            if attempt == retries - 1:
                raise e
            time.sleep(1)
    


def book_class(date, time):
    class_cards = bot.find_elements(By.CSS_SELECTOR, value="div[id^='class-card-']")
    for card in class_cards:
        book_date = card.find_element(By.XPATH, value="./ancestor::div[contains(@id, 'day-group')]")
        actual_date = book_date.find_element(By.CSS_SELECTOR, value="h2[id^='day-title-']")
        class_time = card.find_element(By.CSS_SELECTOR, value="p[id^='class-time-']")
        
        if date in actual_date.text and time in class_time.text:
            check_booked = card.find_element(By.CSS_SELECTOR, value="button[id^='book-button-']")
            
            if "Booked" in check_booked.text:
                print(f"❌ Already booked class on {actual_date.text} at {class_time.text}")
                global total_already_booked
                total_already_booked += 1
                return False
            elif "Waitlisted" in check_booked.text:
                print(f"⚠️ Already waitlisted for class on {actual_date.text} at {class_time.text}")
                total_already_booked += 1
                return False
            book_button = card.find_element(By.CSS_SELECTOR, value="button[id^='book-button-']")
            book_button.click()
            if "Waitlist" in book_button.text:
                print(f"⚠️ Joined waitlist for class on {actual_date.text} at {class_time.text}")
                global waitlist_joined
                waitlist_joined += 1
                return True
            elif "Booked" in book_button.text:
                print(f"✔️ Booked class on {actual_date.text} at {class_time.text}")
                return True
    print(f"❌ No class found on {date} at {time}")
    return False
    
if book_class("Tue", "6:00 PM"):
    total_classes_booked += 1
    booked_now += 1
    
if book_class("Thu", "6:00 PM"):
    total_classes_booked += 1
    booked_now += 1
    
            
# print("---BOOKING SUMMARY---")
# print(f"Total Tuesday & Wednesday 6pm classes booked: {total_classes_booked}")
# print(f"Classes booked now: {booked_now}")
# print(f"Already booked/waitlisted classes: {total_already_booked}")
# print(f"Waitlist joined: {waitlist_joined}")

my_bookings_page = bot.find_element(By.CSS_SELECTOR, value="nav.Navigation_nav__AzWPY a[id='my-bookings-link']")
my_bookings_page.click()

try:
    bookings = bot.find_elements(By.CSS_SELECTOR, value="div[id^='booking-card-']")
    waitlists = bot.find_elements(By.CSS_SELECTOR, value="div[id^='waitlist-card-']")
except NoSuchElementException:
    print("No bookings found.")

for booking in bookings:
    class_info = booking.find_element(By.CSS_SELECTOR, value="h3[id^='booking-class-name-']")
    print(f"✔️ Verified: {class_info.text}")
    actual_bookings += 1

for waitlist in waitlists:
    class_info = waitlist.find_element(By.CSS_SELECTOR, value="h3[id^='waitlist-class-name-']")
    print(f"✔️ Verified: {class_info.text}")
    actual_bookings += 1
    
    
print("---VERIFICATION RESULT---")
print(f"Expected: {total_expected_bookings} bookings")
print(f"Found: {actual_bookings} bookings")

if actual_bookings == total_expected_bookings:
    print("✅ Booking verification successful!")
else:
    print(f"❌ MISMATCH: Missing {total_expected_bookings - actual_bookings} bookings.")