from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    DEEP_SEEK_KEY: str = os.getenv("DEEP_SEEK_KEY")
    DEBUG: bool = os.getenv("DEBUG") == "True"

config = Config()
    