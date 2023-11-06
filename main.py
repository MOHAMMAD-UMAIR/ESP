from src.mlProject import logger
from src.mlProject.pipeline.data_ingestion import DataIngestionTrainingPipeine
from src.mlProject.pipeline.data_transformation import DataTransformationTrainingPipeine


STAGE_NAME= "DATA INGESTION "


try:
    logger.info(f">>>>>>>>> Stage started : {STAGE_NAME}")
    obj = DataIngestionTrainingPipeine()
    obj.main()
    logger.info(f">>>>>>>> Stage Completed : {STAGE_NAME}")
    
except Exception as e:
    logger.exception(e)
    raise e


STAGE_NAME= "DATA TRANSFORMATION"

try:
    logger.info(f">>>>>>>>> Stage started : {STAGE_NAME}")
    obj = DataTransformationTrainingPipeine()
    obj.main()
    logger.info(f">>>>>>>> Stage Completed : {STAGE_NAME}")
    
except Exception as e:
    logger.exception(e)
    raise e

#logger.info("Custom Log")