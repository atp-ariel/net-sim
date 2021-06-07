from simulator import Simulator
from initializer import Initializer, BUNDLE_CONFIG

class Simulator_Singleton:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            init = Initializer()
            init.load_config()
    
            cls._instance = Simulator(init.get("signal-time"), f'{BUNDLE_CONFIG}/{init.get("script-name")}', init.get("error-detection"))
        return cls._instance