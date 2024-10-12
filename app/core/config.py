import yaml

class Settings:
    def __init__(self):
        with open("config.yml", "r") as config_file:
            config = yaml.safe_load(config_file)
        
        self.BASE_URL = config.get("base_url")
        self.IMAGE_OUTPUT_PATH = config.get("image_output_path")
        self.BATCH_VECTOR_API = config.get("batch_vector_api")

settings = Settings()
