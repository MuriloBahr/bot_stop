from dataclasses import dataclass
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


@dataclass
class UtilsSelenium():
    
    
    def click_button(self, xpath):
        try:
            button = self.driver.find_element(By.XPATH, xpath)
            button.click()
            print('@@ CLICK SUCCESSFULLY @@')
        except Exception as e:
            print(f'Error: {e}')
    
    def insert_input(self, content, xpath, enter=False):
        try:
            insert = self.driver.find_element(By.XPATH, xpath)
            insert.clear()
            insert.send_keys(content)
            if enter:
                insert.send_keys(Keys.RETURN)
            print('@@ INSERT SUCCESSFULLY @@')
        except Exception as e:
            print(f'ERROR: {e}')
        