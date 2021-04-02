from pathlib import Path
from exception import MissConfigFileException, UnknowKeyOfConfigException
import json


class Initializer():
    def __init__(self, config_name = "config.json"):
        self._CONFIG_FILE_NAME = config_name
        self.config = {}
    
    def load_config(self):
        path_config = Path(f"./{self._CONFIG_FILE_NAME}")
        
        if path_config.exists():
            with open(path_config) as f:
                self.config = json.load(f)
        else:
            raise MissConfigFileException()

    def get(self, key):
        if not key in self.config:
            raise UnknowKeyOfConfigException(key)
        return self.config[key]



