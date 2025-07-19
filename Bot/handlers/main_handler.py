from dataclasses import dataclass
from selenium_utils.stops import SeleniumHandler


@dataclass
class MainHandler():
    
    def handler_process_selenium(self):
        print('@@@ START PROCESS HANDLER SELENIUM @@')
        SeleniumHandler().start()
        
    def handler_process(self):
        print('@@ START PROCESS @@')
        self.handler_process_selenium()