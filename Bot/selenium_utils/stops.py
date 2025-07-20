from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from . import UtilsSelenium
from configs.configs import config
import time

class SeleniumHandler(UtilsSelenium):
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
    
    def login_window(self):
        print('@@ CLICK LOGIN BUTTON @@')
        self.click_button(config.XPATH_LOGIN)
    
    def insert_name(self):
        print('@@ INSERTING NAME @@')
        try:
            name = 'TOGURO'
            self.insert_input(name, config.XPATH_INPUT_NAME)
        except Exception as e:
            print(f'ERROR: {e}')
    
    def create_room(self):
        print('@@ CREATING ROOM @@')
        try:
            self.click_button(config.XPATH_CREATE_ROOM)
        except Exception as e:
            print(f'ERROR: {e}')
    
    def clear_themes(self):
        while True:
            delete_buttons = self.driver.find_elements(
                By.XPATH,
                f"{config.XPATH_THEME_LIST}//button"
            )
            if not delete_buttons:
                break
            for btn in delete_buttons:
                btn.click()
                time.sleep(0.5)
    
    def add_themes(self):
        for theme in config.THEMES:
            self.insert_input(theme, config.XPATH_INSERT_THEMES, enter=True)
            time.sleep(0.5)
        
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
        
        # Insert name
        self.insert_name()
        time.sleep(2)
        
        # Create Room
        self.create_room()
        time.sleep(5)

        # Clear themes
        self.clear_themes()
        time.sleep(2)
        
        # Add Themes from json_config.json
        self.add_themes()
        time.sleep(10)
        
        # Exit selenium
        self.close()