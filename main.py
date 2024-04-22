from datetime import datetime
import os

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

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
        self.options = Options()
        self.options.add_argument(r"--user-data-dir=C:\Users\Server Gata\AppData\Local\Chromium\User Data")
        self.options.add_argument(r"--profile-directory=Default")
        self.options.add_argument(r"--disable-dev-shm-usage")
        self.options.add_argument("start-maximized"); # https://stackoverflow.com/a/26283818/1689770
        self.options.add_argument("enable-automation"); # https://stackoverflow.com/a/43840128/1689770
        self.options.add_argument("--no-sandbox"); # https://stackoverflow.com/a/50725918/1689770
        self.options.add_argument("--disable-dev-shm-usage"); # https://stackoverflow.com/a/50725918/1689770
        self.options.add_argument("--disable-browser-side-navigation"); # https://stackoverflow.com/a/49123152/1689770
        self.options.add_argument("--disable-gpu"); # https://stackoverflow.com/questions/51959986/how-to-solve-selenium-chromedriver-timed-out-receiving-message-from-renderer-exc
        self.options.add_experimental_option('extensionLoadTimeout', 60_000 * 5)

        # Create a new instance of the Chrome driver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager(version="111.0.5563.64").install()), options=self.options)

        self.target_path = target_path
        self.target_name = target_name

    def wait_for_full_load(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        sleep(1)


    def register_hours(self):
        pass

    def login_with_2FA(self):
        # First log in at BBVA sigin form
        self.driver.find_element(by = By.ID, value = "username").send_keys(os.getenv("BBVA_USER"))
        self.driver.find_element(by = By.ID, value = "password").send_keys(os.getenv("BBVA_PASS"))

        sleep(1)

        # Submit the form
        # self.driver.find_element(by = By.ID, value = '').click()
        self.driver.find_element(by = By.XPATH, value = '//*[@id="loginForm"]/div[2]/button[1]').click()
        
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
        sleep(2)

        # /html/body/div/main/section/div[2]/section/nav/ul/li[2]
        self.driver.find_element(by = By.XPATH, value = '//*[@id="app"]/main/section/div[2]/section/nav/ul/li[2]').click()

        # //*[@id="input-hours-f1ec2dbe-0067-11ef-8f49-bda173575d3b"]
        self.driver.find_element(by = By.XPATH, value = '//*[@id="input-hours-f1ec2dbe-0067-11ef-8f49-bda173575d3b"]').send_keys("8")

        # Click on the Guardar button
        self.driver.find_element(by = By.XPATH, value = '//*[@id="app"]/main/section/div[2]/section/nav/ul/li[2]/div/div[3]/div/div[2]/button[2]').click()
        sleep(2)

        return 

    def get_2FA_code(self):

        # Open new tab and navigate to URL_EMAIL_2FA
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
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
            print(e)
            pass
    
        self.wait_for_full_load()

        # We are into the outlook inbox now
        # 
        # Get the "aria-label" property of the first child of the element that has the XPATH = //*[@id="MailList"]/div/div/div/div/div/div/div/div[2]/div
        child = self.driver.find_element(by=By.XPATH, value='//*[@id="MailList"]/div/div/div/div/div/div/div/div[2]/div/div')
        print(child.get_attribute("aria-label"))
        str_raw = child.get_attribute("aria-label")
        es_idx = str_raw.find("es")
        str_raw = str_raw[es_idx:]
        # Remove all non numeric chars from str_raw
        str_raw = ''.join(filter(str.isdigit, str_raw))
        print(str_raw)

        # close the tab
        self.driver.close()

        return str_raw


    def do(self):
        # Open the URL
        self.driver.get(os.getenv("URL_TIME_REPORT"))

        # Wait for the page to load
        self.wait_for_full_load()
        sleep(2)

        # if the signin  form is present, call login_with_2FA, otherwise call register_hours
        try:
            self.driver.find_element(by = By.XPATH, value = '//*[@id="loginForm"]')
            self.login_with_2FA()
        except Exception as e:
            print(e)

        self.register_hours()

        self.driver.save_screenshot(f"{target_path}\\{target_name}")
        sleep(1)
        print("Screenshot saved on: " + f"{target_path}\\{target_name}")


if __name__ == "__main__":
    now = datetime.now()
    
    # redirect the output to a file (Logs)
    # sys.stdout = open(r"C:\Users\Server Gata\OneDrive - NEORIS\General - Test File Sync\logs" + f"\\{str(now).replace(' ', '¬').replace(':', '').replace('.','')}.txt", 'w')
    
    # get the day of week
    day_of_week = now.strftime("%A")
    
    # first make sure that today is a working day
    if day_of_week == "Saturday" or day_of_week == "Sunday":
        print(f"You do not have to fill your time report on {day_of_week}s")
        exit(0)
    
    current_date = now.strftime("%Y%m%d")
    target_name = current_date + " MADARIAGA COLLADO SANTIAGO HECTOR.png"
    target_path = r"C:\Users\Server Gata\OneDrive - NEORIS\General - Test File Sync\pics"
    
    # Load dotenv file
    env.load_dotenv()

    try:
        bot = TimeReportBot(target_path, target_name)
        bot.do()

    except Exception as e:
        print(e)
        print("Closing the script")
        # sys.stdout.close()
        exit(1)
