from datetime import datetime

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager


from time import sleep

import sys

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

    def __init__(self, URL, target_name):
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
        self.driver.get(URL)
        sleep(1)
        # click on the PLUS icon
        
        # try catch "NoSuchElementException" from selenium.common.exceptions
        # wait for the page to load
        wait = True
        while wait:
            try:
                self.driver.find_element(by = By.XPATH, value = "//*[contains(text(),'Hoy')]")
                print("Home page loaded!")
                wait = False
            except:
                print("Waiting for the home page to load")
                sleep(2)
                wait = True

        try:
            try: 
                print("Click on the plus icon")
                self.driver.find_element(by = By.XPATH, value = '//*[@id="app"]/main/section/div[2]/section/nav/ul/li[2]/div[2]/div[1]/div').click()
            except:
                print("Click on the plus icon (2)")         
                self.driver.find_element(by = By.XPATH, value = '//*[@id="app"]/main/section/div[3]/section/nav/ul/li[2]/div[2]/div[1]/div').click()
        except:
            print("Element not found")
            print("Trying to click on the SDA TOOL plus icon")
            self.driver.find_element(by = By.XPATH, value = "//*[contains(text(),'42585')]").click()
            
            self.wait_spinning()
            # send 8 hours to the hours field   
            self.driver.find_element(by = By.XPATH, value = '//*[@id="hours"]/div[1]/div[1]/div/div/div/*').clear()
            sleep(1)
            self.driver.find_element(by = By.XPATH, value = '//*[@id="hours"]/div[1]/div[1]/div/div/div/*').send_keys("8")
            sleep(1)
            # click on the save button
            # XPATH //*[@id="app"]/main/section/div[2]/section/nav/ul/li[2]/div/div[3]/div/div[2]/button[2]
            print("Save")
            self.driver.find_element(by = By.XPATH, value = "//*[contains(text(),'Guardar')]").click()
            wait = True

            self.wait_spinning()

            self.driver.save_screenshot(f"{target_path}\\{target_name}")
            sleep(1)
            print("Screenshot saved on: " + f"{target_path}\\{target_name}")
            exit(0)

        # click on Projects with code
        wait = True
        self.wait_spinning()
        self.driver.find_element(by = By.XPATH, value = '//*[@id="app"]/main/div/section[3]/div/div[1]/div').click()
        # click on the SDA TOOL software project
        self.wait_spinning()
        print("Click on the SDA TOOL software project")
        self.driver.find_element(by = By.XPATH, value = '//*[@id="app"]/main/div/section[4]/div/div/div[1]').click()
        self.wait_spinning()
        # omit features
        print("Click on the omit features")
        self.driver.find_element(by = By.XPATH, value = '//*[@id="app"]/main/div/section[2]/span').click()
        self.wait_spinning()
        # click on development
        print("Click on development")
        self.driver.find_element(by = By.XPATH, value = '//*[@id="app"]/main/div/section[2]/div/div[4]/div').click()
        # click on LRBA
        self.wait_spinning()
        print("Click on LRBA")
        self.driver.find_element(by = By.XPATH, value = '//*[@id="app"]/main/div/section[2]/div/div[13]/div/div[1]/div[2]').click()
        self.wait_spinning()
        # write 8 hours in the hours field
        self.driver.find_element(by = By.XPATH, value = '//*[@id="hours"]/div[1]/div[1]/div/div/div/*').clear()
        sleep(1)
        self.driver.find_element(by = By.XPATH, value = '//*[@id="input-hours-id"]').send_keys("8")
        # CLick on the Save button
        self.wait_spinning()
        self.driver.find_element(by = By.XPATH, value = '//*[@id="app"]/main/div/section[4]/button').click()
        self.wait_spinning()
        # Scroll down
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)
        self.driver.save_screenshot(f"{target_path}\\{target_name}")
        self.wait_spinning()
        sleep(1)
        print("Screenshot saved on: " + f"{target_path}\\{target_name}")


if __name__ == "__main__":
    now = datetime.now()
    
    # redirect the output to a file (Logs)
    sys.stdout = open(r"C:\Users\Server Gata\OneDrive - NEORIS\General - Test File Sync\logs" + f"\\{str(now).replace(' ', '¬').replace(':', '').replace('.','')}.txt", 'w')
    
    # get the day of week
    day_of_week = now.strftime("%A")
    
    # first make sure that today is a working day
    if day_of_week == "Saturday" or day_of_week == "Sunday":
        print(f"You do not have to fill your time report on {day_of_week}s")
        exit(0)
    
    current_date = now.strftime("%Y%m%d")
    target_name = current_date + " MADARIAGA COLLADO SANTIAGO HECTOR.png"
    target_path = r"C:\Users\Server Gata\OneDrive - NEORIS\General - Test File Sync\pics"
    URL = "https://timereport-eng.com/"

    try:
        bot = TimeReportBot(URL, target_name)
    except Exception as e:
        print(e)
        print("Closing the script")
        sys.stdout.close()
        exit(1)
