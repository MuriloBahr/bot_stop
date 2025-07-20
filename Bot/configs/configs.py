from dataclasses import dataclass, field
import os
import json
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    
    
    BASE_DIR = os.path.dirname(__file__)
    
    DEEP_SEEK_KEY: str = os.getenv("DEEP_SEEK_KEY")
    DEBUG: bool = os.getenv("DEBUG") == "True"
    
    XPATH_LOGIN = '//*[@id="top"]/div[1]/div[2]/div[1]/form/button'
    XPATH_CREATE_ROOM = '//*[@id="screenHome"]/div[2]/div[2]/button[2]'
    XPATH_INPUT_NAME = '//*[@id="screenHome"]/div[2]/div[1]/div[2]/input'
    XPATH_THEME_LIST = '//*[@id="screenCreate"]/div[2]/div[2]/div[2]/div[1]/div'
    XPATH_INSERT_THEMES = '//*[@id="screenCreate"]/div[2]/div[2]/form/input[1]'
    
    THEMES: list = field(default_factory=list)

    def __post_init__(self):
        self.load_json()

    def load_json(self):
        with open(os.path.join(self.BASE_DIR, "json_config.json"), "r") as f:
            data = json.load(f)
            self.THEMES = data["config_stop"]["THEMES"]

config = Config()
    