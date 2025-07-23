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
        
        self.wait = WebDriverWait(self.driver, 30)

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
                    self.wait.until(EC.element_to_be_clickable(btn)).click()
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
        print("@@ Waiting for INICIAR message @@")
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
                    start_button = self.wait.until(
                        EC.element_to_be_clickable(
                            (By.XPATH, config.XPATH_START_GAME)
                        )
                    )
                    start_button.click()
                    break
            except Exception as e:
                print(f"ERROR checking INICIAR: {e}")
            time.sleep(1)
    
    def get_letter_stop(self):
        return self.get_text(config.XPATH_LETTER)
    
    def insert_themes_answer(self):
        content_ia = None
        div_element = self.wait.until(
            EC.presence_of_element_located((By.XPATH, config.XPATH_THEMES_IN_GAME))
        )
        labels = div_element.find_elements(By.TAG_NAME, 'label')
        for label in labels:
            span = label.find_element(By.TAG_NAME, 'span')
            WebDriverWait(self.driver, 10).until(
                lambda d: span.text.strip() != ""
            )
            label_text = span.text.strip().lower()
            if label_text:
                content_ia = self.consulting_AI(label_text, self.get_letter_stop())
                input_element = label.find_element(By.TAG_NAME, 'input')
                input_element.clear()
                input_element.send_keys(content_ia)
        self.click_stop()
        self.click_avaliable()
                
    def click_stop(self):
        try:
            button_xpath = '//button[contains(@class, "bt-yellow") and contains(@class, "icon-exclamation")]'

            button = self.wait.until(
                EC.presence_of_element_located((By.XPATH, button_xpath))
            )
            self.wait.until(
                lambda d: "disable" not in button.get_attribute("class")
            )
            button.click()
        except Exception as error:
            ...
    
    def click_avaliable(self):
        button_xpath = '//*[@id="screenGame"]/div[2]/div[2]/div/button'

        while True:
            try:
                button = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, button_xpath))
                )

                button_text = button.text.strip().upper()
                print(f"Texto do botão: {button_text}")

                if button_text == "ESTOU PRONTO":
                    print("Botão com texto ESTOU PRONTO encontrado, saindo do loop.")
                    break
                button.click()
                print("Botão clicado.")

            except Exception as error:
                print("Botão não encontrado, tentando de novo...")
            time.sleep(1)
    
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
        for _ in range(10):
            # Wait INICIAR from player
            self.wait_for_start_and_click()
            
            # Get letter stop
            self.get_letter_stop()
            
            # Insert Answers from themes
            self.insert_themes_answer()
        
