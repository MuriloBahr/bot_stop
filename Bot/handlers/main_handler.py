from dataclasses import dataclass
from selenium_utils.stops import SeleniumHandler
from geminiAI import GeminiAI


@dataclass
class MainHandler():
    
    def handler_process_gemini(self, prompt):
        print('@@@ START PROCESS HANDLER GEMINI')
        return GeminiAI().generate(prompt)
    
    def handler_process_selenium(self):
        print('@@@ START PROCESS HANDLER SELENIUM @@')
        SeleniumHandler().start()
        
    def handler_process(self):
        print('@@ START PROCESS @@')
        self.handler_process_selenium()