from mlProject import logger
from mlProject.pipeline.data_ingestion import DataIngestionTrainingPipeine


STAGE_NAME= "DATA INGESTION"


try:
    logger.info(f">>>>>>>>> Stage started : {STAGE_NAME}")
    obj = DataIngestionTrainingPipeine()
    obj.main()
    logger.info(f">>>>>>>> Stage Completed : {STAGE_NAME}")
    
except Exception as e:
    logger.exception(e)
    raise e


#logger.info("Custom Log")