import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.exception import CustomException
from src.logger import logging
from src.components.data_transformation import DataTransformation
from src.components.data_cleaning import DataCleaning
from src.utils import save_object

import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
import xml.etree.ElementTree as ET

from dotenv import load_dotenv

load_dotenv()

@dataclass
class DataIngestionConfig:
    raw_data_path: str = os.getenv('RAW_DATA_PATH')
    train_data_path: str = os.getenv('TRAIN_DATA_PATH')
    test_data_path: str = os.getenv('TEST_DATA_PATH')
    xml_file_path: str = os.getenv('XML_FILE_PATH')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info('Data ingestion initiated for XML.')

        file_path = self.ingestion_config.xml_file_path
        logging.info(f"XML file path from environment: {file_path}")
        
        if file_path is None:
            raise ValueError("XML file path is not set. Check the environment variable.")

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            logging.info('Read dataset as XML')

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            logging.info("Raw data cloned successfully.")
            tree.write(self.ingestion_config.raw_data_path)



            logging.info('train test split initiated')
            data = []
            for record in root.findall('Record'):
                if record.get('type'):
                    child_elems={
                        'type': record.get('type'),
                        'start_date': record.get('startDate'),
                        'value': record.get('value')
                    }
                    data.append(child_elems)
            
            df = pd.DataFrame(data)
            logging.info(f"unique_types = {df['value'].apply(type).unique()}")

            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False)
            logging.info('Data ingestion complete')
            logging.info(f"unique_types before data transformation = {df['value'].apply(type).unique()}")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
            

        except Exception as e:
            raise CustomException(e, sys)
        
from src.logger import logging
if __name__ == '__main__':
    try:
        ingestion_obj = DataIngestion()
        train_data, test_data = ingestion_obj.initiate_data_ingestion()

        # cleaning_obj = DataCleaning()
        # cleaned_train_data, cleaned_test_data = cleaning_obj.initiate_data_cleaning(train_data, test_data)

        # data_transformation = DataTransformation()
        # train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data, test_data)

    except Exception as e:
        logging.error(f"An error occured: {e}")
        raise

