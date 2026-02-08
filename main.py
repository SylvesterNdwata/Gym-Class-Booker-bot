from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import os

ACCOUNT_EMAIL = "silver@test.com"
ACCOUNT_PASSWORD = "7sYst6VWapcpK87"
GYM_URL = "https://appbrewery.github.io/gym/"

total_classes_booked = 0
waitlist_joined = 0
booked_now = 0
total_already_booked = 0

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

bot = webdriver.Chrome(options=chrome_options)

bot.implicitly_wait(5)
bot.get(GYM_URL)

login_button = bot.find_element(By.CSS_SELECTOR, value="button.Navigation_button__uyKX2 ")
login_button.click()

email_input = bot.find_element(By.ID, value="email-input")
email_input.send_keys(ACCOUNT_EMAIL)

password_input = bot.find_element(By.ID, value="password-input")
password_input.send_keys(ACCOUNT_PASSWORD)

submit_button = bot.find_element(By.CLASS_NAME, value="Login_submitButton__tJFna ")
submit_button.click()

class_cards = bot.find_elements(By.CSS_SELECTOR, value="div[id^='class-card-']")

# book_date = bot.find_element(By.CSS_SELECTOR, value="h2[id^='day-title-']")
# class_time = bot.find_element(By.CSS_SELECTOR, value="p[id^='class-time-']")
# print(book_date.text)
# print(class_time.text)

def book_class(date, time):
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
    
            
print("---BOOKING SUMMARY---")
print(f"Total Tuesday & Wednesday 6pm classes booked: {total_classes_booked}")
print(f"Classes booked now: {booked_now}")
print(f"Already booked/waitlisted classes: {total_already_booked}")
print(f"Waitlist joined: {waitlist_joined}")
