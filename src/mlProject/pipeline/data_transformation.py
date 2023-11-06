from src.mlProject.config.configuration import ConfigurationManager
from src.mlProject.components.data_transformation import DataTransformation
from src.mlProject import logger

STAGE_NAME= "DATA TRANSFORMATION"
class DataTransformationTrainingPipeine:
    def __init__(self):
        pass
    
    def main(self):

        config = ConfigurationManager()
        data_transformation_config = config.get_data_transformation_config()
        data_transformation = DataTransformation(config=data_transformation_config)
        data_transformation.extract_split()

if __name__ == '__main__':
    try:
        logger.info(f">>>>>>>>> Stage started : {STAGE_NAME}")
        obj = DataTransformationTrainingPipeine()
        obj.main()
        logger.info(f">>>>>>>> Stage Completed : {STAGE_NAME}")
        
    except Exception as e:
        logger.exception(e)
        raise e





