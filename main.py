from datetime import datetime
import os
import re
import sys

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import dotenv as env


from time import sleep

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TimeReportBot:

    def wait_spinning(self):
        wait = True
        while wait:
            try:
                self.driver.find_element(by = By.CLASS_NAME, value = "bg-spinner")
                print("Waiting for the page to load")
                
            except:
                print("Page loaded!")
                wait = False

            sleep(2)
        return 

    def __init__(self, target_path, target_name):
        # Create a new instance of Options with personal profile
        print("Init")
        # Fix: connect to existing versions of chrome 
        debugger_address = 'localhost:1258'
        # Create a new instance of the Chrome driver
        # Set up ChromeOptions and connect to the existing browser
        c_options = Options()
        c_options.add_experimental_option("debuggerAddress", debugger_address)


        self.driver = webdriver.Chrome(options=c_options)
        print("Driver initalized")
        self.target_path = target_path
        self.target_name = target_name

    def wait_for_full_load(self):
        # Wait for the page to load
        print("Waiting for the page to load")
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        sleep(1)
        print("Page loaded")
        return

    def register_hours(self):
        print("Registering hours")
        self.wait_spinning()
        # Step 1: proyecto 1
        self.driver.find_element(by = By.XPATH, value = '//*[@id="app"]/main/section/div[2]/section/nav/ul/li[2]').click()
        input_hours = self.driver.find_element(by=By.XPATH, value='//*[contains(@id, "input-hours")]')
        print(input_hours)
        input_hours.clear()
        input_hours.send_keys("6")

        input_minutes = self.driver.find_element(by=By.XPATH, value='//*[contains(@id, "input-minutes")]')
        input_minutes.clear()
        input_minutes.send_keys("50")

        # Click on the Guardar butt
        print("Saving proyect 1 hours")
        self.driver.find_element(by = By.XPATH, value = '//*[contains(@class, "accept")]').click()
        sleep(1)
        self.wait_spinning()
        # Step 2: proyecto 2
        print("Step 2")
        self.driver.find_element(by = By.XPATH, value = '//*[@id="app"]/main/section/div[2]/section/nav/ul/li[3]').click()
        input_hours = self.driver.find_element(by=By.XPATH, value='//*[@id="app"]/main/section/div[2]/section/nav/ul/li[3]/div/div[3]/div/div[1]/div/div/div[1]/div[1]/div/div/div/input')
        print(input_hours)
        input_hours.clear()
        input_hours.send_keys("1")

        input_minutes = self.driver.find_element(by=By.XPATH, value='//*[@id="app"]/main/section/div[2]/section/nav/ul/li[3]/div/div[3]/div/div[1]/div/div/div[2]/div[1]/div/input')
        input_minutes.clear()
        input_minutes.send_keys("10")

        # Click on the Guardar button
        print("Saving proyect 2s hours")
        self.driver.find_element(by = By.XPATH, value = '//*[@id="app"]/main/section/div[2]/section/nav/ul/li[3]/div/div[3]/div/div[2]/button[2]').click()
        sleep(1)
        self.wait_spinning()

        # Check if there is a modal
        try:
            # if the following button existsÑ '//*[@id="app"]/main/section/div[2]/section/nav/ul/li[3]/div/div[4]/div/div/div[6]/span/button[1]'
            # Click on it, if not, just continue with your execution
            self.driver.find_element(by = By.XPATH, value = '//*[@id="app"]/main/section/div[2]/section/nav/ul/li[3]/div/div[4]/div/div/div[6]/span/button[1]').click()
            print("Modal of confirmation displayed")
            self.sleep(1)
            self.wait_spinning()

        except e:
            print(e, "No modal of confirmation displayed")
            pass


        sleep(5)
        self.wait_for_full_load()
        self.wait_spinning()
        sleep(2)
        return

    def login_with_2FA(self):
        print("Logging in with 2FA")
        sleep(1.2)
        # First log in at BBVA sigin form
        self.driver.find_element(by = By.ID, value = "username").send_keys(os.getenv("BBVA_USER"))
        sleep(1.3)
        self.driver.find_element(by = By.ID, value = "password").send_keys(os.getenv("BBVA_PASS"))

        sleep(1.1)

        # Submit the form
        # self.driver.find_element(by = By.ID, value = '').click()
        self.driver.find_element(by = By.XPATH, value = '//*[@id="loginForm"]/div[2]/button[1]').click()
        sleep(2.1)
        
        self.wait_for_full_load()
        # click on //*[@id="msa***a@neoris.com"]
        self.driver.find_element(by = By.XPATH, value = '//*[@id="form"]/div/div[1]/div[2]/div[2]/div[2]').click()

        # Then click on the button with type="submit"
        self.driver.find_element(by = By.XPATH, value = '//*[@id="form"]/div/div[3]/button').click()

        # Wait for the page to load
        self.wait_for_full_load()
        
        sleep(5)
        FA_code = self.get_2FA_code()

        self.driver.find_element(by = By.XPATH, value = '//*[@id="otp_mail"]').send_keys(FA_code)

        # Click on the button with type="submit"
        self.driver.find_element(by = By.XPATH, value = '//*[@id="form"]/div/div[2]/button').click()
        self.wait_for_full_load()
        self.wait_spinning()
        sleep(15) # wait a little longer
        self.wait_for_full_load()
        self.wait_spinning()

        try:
            # /html/body/div/main/section/div[2]/section/nav/ul/li[2]
            self.driver.find_element(by = By.XPATH, value = '//*[@id="app"]/main/section/div[2]/section/nav/ul/li[2]').click()
        except:
            print("No element found, but we will save cookies")
            # save the session cookies to avoid the 2FA login next time
            cookies = self.driver.get_cookies()
            # write the cookies to a file
            with open("cookies.txt", "w") as file:
                file.write(str(cookies))
            self.driver.quit()
            exit(-2)

        return 

    def get_2FA_code(self):
        print("Getting 2FA code")
        # Open new tab and navigate to URL_EMAIL_2FA
        self.driver.switch_to.new_window('tab')
        self.driver.get(os.getenv("URL_MAIL_2FA")) # this is the outlook mail

        # If there is a login screen, send the credentials (env.2FA_MAIL, env.2FA_PASS) and log in into outlook 
        try:
            self.driver.find_element(by=By.XPATH, value='//*[contains(text(), "Iniciar sesión")]')
            self.driver.find_element(by=By.ID, value='i0116').send_keys(os.getenv("MAIL_2FA_USERNAME"))
            self.driver.find_element(by=By.ID, value='idSIButton9').click()
            sleep(2)
            self.driver.find_element(by=By.ID, value='i0118').send_keys(os.getenv("MAIL_2FA_PASSWORD"))
            self.driver.find_element(by=By.ID, value='idSIButton9').click()
        except Exception as e:
            print("No outlook login screen found")
            pass
    
        self.wait_for_full_load()
        sleep(2.7)

        # We are into the outlook inbox now
        # 
        # Get the "aria-label" property of the first child of the element that has the XPATH = //*[@id="MailList"]/div/div/div/div/div/div/div/div[2]/div
        self.wait_for_mail()
        child = self.driver.find_element(by=By.XPATH, value='//*[@id="MailList"]/div/div/div/div/div/div/div/div[2]/div/div')
        str_raw = child.get_attribute("aria-label")
        # Use REGEX to get the string with the code (6 digits)
        code = re.search(r"\d{6}", str_raw).group(0)
        print(f"2FA code: {code}")

        # change the focus to the first tab
        self.driver.switch_to.window(self.driver.window_handles[0])

        return code
    
    def wait_for_mail(self):
        wait = True
        count = 0
        while wait:
            print(count)
            if count > 10:
                count = 0
                print("Refreshing the page")
                self.driver.refresh()
            try:
                self.driver.find_element(by = By.XPATH, value = '//*[@id="MailList"]/div/div/div/div/div/div/div/div[2]/div/div')
                print("Waiting for the mail")
                wait = False
            except:
                print("No mail found")
                sleep(2)
                count += 1
                pass
        return


    def do(self):
        # Open the URL
        self.driver.get(os.getenv("URL_TIME_REPORT"))

        # Wait for the page to load
        self.wait_for_full_load()
        sleep(2)

        # FIx: check if the google sign in page is present (choose your account)
        try:
            self.driver.find_element(by = By.XPATH, value = '/html/body/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[1]/form/span/section/div/div/div/div/ul/li[1]/div')
            print("Google sign in page found")
            self.driver.find_element(by = By.XPATH, value = '/html/body/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[1]/form/span/section/div/div/div/div/ul/li[1]/div').click()
            sleep(2)
        except:
            print("No google sign in page found")
            pass

        # If the page is an error (no interactable elements) instead of the time report page, reload the page
        try:
            self.driver.find_element(by = By.XPATH, value = '//*[@id="loginForm"]')
        except:
            self.driver.get(os.getenv("URL_TIME_REPORT"))
            self.wait_for_full_load()
            sleep(2)

        # if the signin  form is present, call login_with_2FA, otherwise call register_hours
        try:
            self.driver.find_element(by = By.XPATH, value = '//*[@id="loginForm"]')
            self.login_with_2FA()
        except Exception as e:
            print(e)

        self.register_hours()

        self.driver.save_screenshot(f"{target_path}/{target_name}")
        sleep(1)
        print("Screenshot saved on: " + f"{target_path}/{target_name}")


if __name__ == "__main__":
    now = datetime.now()
    
    # redirect the output to a file (Logs)
    sys.stdout = open(f"{os.getenv('ONEDRIVE_AUX_PATH')}/logs/{str(now).replace(' ', '¬').replace(':', '').replace('.','')}.txt", 'w')
    
    # get the day of week
    day_of_week = now.strftime("%A")
    
    # first make sure that today is a working day
    if day_of_week == "Saturday" or day_of_week == "Sunday":
        print(f"You do not have to fill your time report on {day_of_week}s")
        exit(0)
    
    current_date = now.strftime("%Y%m%d")
    target_name = current_date + " MADARIAGA COLLADO SANTIAGO HECTOR.png"
    target_path = f"{os.getenv('ONEDRIVE_AUX_PATH')}/pics"
    
    # Load dotenv file
    env.load_dotenv()

    try:
        bot = TimeReportBot(target_path, target_name)
        bot.do()

    except Exception as e:
        bot.driver.save_screenshot(f"{os.getenv('ONEDRIVE_AUX_PATH')}/logs" + f"\\{target_name}") # for debugging
        bot.driver.quit()
        print("An error ocurred")
        print(e)
        sleep(1600)
        print("Closing the script")
        sys.stdout.close()
        # wait for any key press