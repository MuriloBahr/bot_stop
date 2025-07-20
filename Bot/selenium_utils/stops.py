from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
            name = config.DATA_JSON["config_stop"].get('nickname', None)
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
        wait = WebDriverWait(self.driver, 30)
        while True:
            delete_buttons = self.driver.find_elements(
                By.XPATH,
                f"{config.XPATH_THEME_LIST}//button"
            )
            if not delete_buttons:
                break

            for btn in delete_buttons:
                try:
                    wait.until(EC.element_to_be_clickable(btn)).click()
                except Exception as e:
                    print(f"ERROR while clearing theme: {e}")
    
    def add_themes(self):
        for theme in config.THEMES:
            self.insert_input(theme, config.XPATH_INSERT_THEMES, enter=True)
            time.sleep(0.5)
    
    def insert_password(self):
        self.insert_input(config.DATA_JSON["config_stop"].get('password', None), config.XPATH_PASSWORD)
    
    def click_create_room(self):
        self.click_button(config.XPATH_CLICK_CREATE_ROOM)
    
    def get_link_stop(self):
        print(self.get_input_value(config.XPATH_LINK_ROOM))
        print(self.get_input_value(config.XPATH_LINK_ROOM))
        print(self.get_input_value(config.XPATH_LINK_ROOM))
    
    def close_link_room(self):
        self.click_button(config.XPATH_CLOSE_LINK_ROOM)
        
    def talk_start(self):
        if self.content_changed(config.XPATH_LIST_USERS):
            self.insert_input('Peça para iniciar com: "INICIAR"', config.XPATH_CHAT, enter=True)
            time.sleep(1)
            self.insert_input('XD XD XD XD', config.XPATH_CHAT, enter=True)
        
    def wait_for_start_and_click(self):
        wait = WebDriverWait(self.driver, 30)
        print("@@ Waiting for INICIAR message @@")
        elapsed = 0
        while True:
            try:
                self.talk_start()
                li_elements = self.driver.find_elements(By.CSS_SELECTOR, "ul.historic li")

                found = False
                for li in li_elements:
                    span = li.find_element(By.TAG_NAME, "span")
                    if span.text.strip().upper() == "INICIAR":
                        found = True
                        break

                if found:
                    print("@@ INICIAR found! Clicking START button @@")
                    start_button = wait.until(
                        EC.element_to_be_clickable(
                            (By.XPATH, config.XPATH_START_GAME)
                        )
                    )
                    start_button.click()
                    break
            except Exception as e:
                print(f"ERROR checking INICIAR: {e}")
            time.sleep(1)
            elapsed += 1
    
    def close(self):
        print('@@ END PROCESS SELENIUM')
        self.driver.quit()

    def start(self):
        # Start Page StopS
        self.open_stop()

        # Click in button "Entrar como anonimo"
        self.login_window()

        # Insert name
        self.insert_name()

        # Create Room
        self.create_room()
        
        # Insert password
        self.insert_password()

        # Clear themes
        self.clear_themes()

        # Add Themes from json_config.json
        self.add_themes()
        
        # Click in "Criar Sala"
        self.click_create_room()
        
        # Get link room
        self.get_link_stop()
        
        # Close link room
        self.close_link_room()
        
        # Wait INICIAR from player
        self.wait_for_start_and_click()

        # Exit selenium
        self.close()
