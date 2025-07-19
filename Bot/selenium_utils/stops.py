from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time

class SeleniumHandler:
    def __init__(self, driver_path=None):
        options = Options()
        options.add_argument("--start-maximized")
        if driver_path:
            service = Service(driver_path)
            self.driver = webdriver.Firefox(service=service, options=options)
        else:
            self.driver = webdriver.Firefox(options=options)

    def open_stop(self):
        print('@@ OPEN STOPS @@')
        self.driver.get("https://stopots.com/pt/")
        time.sleep(10)
    
    def login_window(self):
        print('@@ CLICK LOGIN BUTTON @@')
        try:
            button = self.driver.find_element(By.XPATH, '//*[@id="top"]/div[1]/div[2]/div[1]/form/button')
            button.click()
            time.sleep(5)
        except Exception as e:
            print("ERROR: ", e)
        
    def close(self):
        print('@@ END PROCESS SELENIUM')
        self.driver.quit()

    def start(self):
        # Start Page StopS
        self.open_stop()
        time.sleep(2)
        
        # Click in button "Entrar como anonimo"
        self.login_window()
        time.sleep(5)
        
        # Exit selenium
        self.close()