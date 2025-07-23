from dataclasses import dataclass
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configs.configs import config


@dataclass
class UtilsSelenium():
    
    driver: any
    wait_time: int = 30
    last_list_html = "" 
    

    def click_button(self, xpath):
        try:
            button = WebDriverWait(self.driver, self.wait_time).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            button.click()
            print('@@ CLICK SUCCESSFULLY @@')
        except Exception as e:
            print(f'Error: {e}')

    def insert_input(self, content, xpath, enter=False):
        try:
            insert = WebDriverWait(self.driver, self.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            insert.clear()
            insert.send_keys(content)
            if enter:
                insert.send_keys(Keys.RETURN)
            print('@@ INSERT SUCCESSFULLY @@')
        except Exception as e:
            print(f'ERROR: {e}')

    def get_input_value(self, xpath):
        value = None
        try:
            input_element = WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            value = input_element.get_attribute("value")
        except Exception as e:
            print(f'ERROR: {e}')
        return value
    
    def get_text(self, xpath):
        text = None
        try:
            while True:
                element = WebDriverWait(self.driver, self.wait_time).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                if element.text.isalpha() and len(element.text) == 1:
                    text = element.text
                    break
        except Exception as e:
            print(f'ERROR: {e}')
        print(f'@@ GETTING LETTER: {text}')
        return text
    
    def content_changed(self, xpath):
        try:
            current_content = self.driver.find_element(By.XPATH, xpath).get_attribute("innerHTML")
            if self.last_list_html != current_content:
                self.last_list_html = current_content
                return True
            return False
        except Exception:
            return False
        
    def consulting_AI(self, theme, letter):
        from handlers.main_handler import MainHandler
        print('@@@ CONSULTING GEMINI @@')
        response = None
        prompt = f"Você é o melhor jogador de STOP do mundo. Sua tarefa é responder apenas com uma única palavra ou expressão curta que corresponda exatamente ao tema e à letra indicados. Se não existir, responda apenas XXXXXXX — sem explicação, sem pontuação extra, sem frases. Tema (CEP = cidade, estado ou país, Nome = Nome de pessoas): {theme} Letra inicial: {letter}"
        response = MainHandler().handler_process_gemini(prompt)
        return response            
        
        
