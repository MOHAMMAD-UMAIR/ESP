from pathlib import Path
from src.mlProject import logger
from src.mlProject.utils.common import *


from src.mlProject.entity.config_entity import DataTransformationConfig

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config


    def extract_split(self):
        print(Path(self.config.data_file))
        
        #content=load_json(Path(self.config.data_file))
        df_attack, df_campaign, df_intrusion, df_malware, df_relationship = load_create_df(Path(self.config.data_file))
        logger.info("Data_extracted and splitted")

        df_relationship = df_relationship[df_relationship['relationship_type'].isin(['uses', 'subtechnique-of'])]
        attack_to_adversery(df_attack,df_relationship,df_intrusion,df_campaign,Path(self.config.JSON_extract))
        

        logger.info("JSON data_extracted and splitted")

        

        