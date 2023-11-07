#downloading the data
import os
from pathlib import Path
import urllib.request as request
import zipfile
from src.mlProject import logger
from src.mlProject.utils.common import get_size
from src.mlProject.entity.config_entity import DataIngestionConfig


# Downloading the Json data from the link and saving it on device
class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config


    
    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(
                url = self.config.source_URL,
                filename = self.config.local_data_file
            )
            logger.info(f"{filename} download! with following info: \n{headers}")
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")

  