import yaml
import os # Import the os module

class Settings:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_dir, "config.yml")  # Absolute path
        with open(config_path, "r") as config_file:
            config = yaml.safe_load(config_file)
        
        self.BASE_URL = config.get("base_url")
        self.IMAGE_OUTPUT_PATH = config.get("image_output_path")
        self.BATCH_VECTOR_API = config.get("batch_vector_api")
        self.DATA_OUTPUT_PATH = config.get("data_output_path")  # New config value

settings = Settings()
