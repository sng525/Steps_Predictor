import sys
import os
from dataclasses import dataclass
import numpy as np
import pandas as pd

from src.exception import CustomException
from src.logger import logging

@dataclass
class DataCleaningConfig:
    train_df_cleaned_obj_file_path: str = os.path.join('artefacts', 'train_df.pkl')
    test_df_cleaned_obj_file_path: str = os.path.join('artefacts', 'test_df.pkl')

class DataCleaning:
    def __init__(self):
        self.data_cleaning_config = DataCleaningConfig()

    def filter_type(self, filter_for, df):
        filtered_df = df[df['type'].isin(filter_for)]
        return filtered_df

        
    def initiate_data_cleaning(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            filter_for = ['HKQuantityTypeIdentifierStepCount']

            train_df_filtered = self.filter_type(filter_for, train_df)
            test_df_filtered = self.filter_type(filter_for, test_df)
            logging.info(f"unique values in train_df: {train_df['type'].unique()}")
            logging.info(f"unique values in filtered: {train_df_filtered['type'].unique()}")
            
            cols_to_keep = ['start_date', 'value']

            train_df_dropped = train_df_filtered[cols_to_keep]
            test_df_dropped = test_df_filtered[cols_to_keep]
            logging.info(f"columns BEFORE dropping: {train_df.columns}")
            logging.info(f"columns AFTER dropping: {train_df_dropped.columns}")

            train_df_dropped['start_date'] = pd.to_datetime(train_df_dropped['start_date']).dt.date
            test_df_dropped['start_date'] = pd.to_datetime(test_df_dropped['start_date']).dt.date
           
            logging.info(f"train_df, start_date type: {type(train_df['start_date'].unique())}")
            logging.info(f"train_df_dropped, start_date type: {type(train_df_dropped['start_date'].unique())}")
            
            cleaned_train_df= train_df_dropped.reset_index(drop=True)
            cleaned_test_df = test_df_dropped.reset_index(drop=True)

            logging.info("Datasets cleaned successfully.")
            logging.info(f'cleaned_train_df: {cleaned_train_df.head(2)}')
            logging.info(f'cleaned_test_df: {cleaned_test_df.head(2)}')
            logging.info(f'cleaned_test_df: {type(cleaned_test_df)}')

            return(
                cleaned_train_df,
                cleaned_test_df,
            )
        
        except Exception as e:
            logging.error(f"Error in initiate_data_cleaning: {e}")
            raise CustomException(e, sys)
        
        #Requires converting value col to int