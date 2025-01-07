import sys
import os
from dataclasses import dataclass
import numpy as np
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline
from src.exception import CustomException
from src.logger import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    features_preprocessor_obj_file_path: str = os.path.join('artefacts', 'features_preprocessor.pkl')
    
class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def filter_type(self, filter_for, df):
        filtered_df = df[df['type'].isin(filter_for)]
        return filtered_df
    
    def to_datetime(self, df):
        df['start_date'] = pd.to_datetime(df['start_date'])
        return df

    def get_features_transformer_object(self):
        try:
            filter_for = ['HKQuantityTypeIdentifierStepCount']

            features_preprocessor = ColumnTransformer(
                transformers=[
                    ('start_date_transform', FunctionTransformer(self.to_datetime), ['start_date']),
                    ('filter_transform', FunctionTransformer(lambda df: self.filter_type(filter_for, df)), ['type']),
                ],
                #remainder='drop'
            )           
            return features_preprocessor

        except Exception as e:
            logging.error(f"Error in get_features_transformer_object: {e}")
            raise CustomException(e, sys)


    def initiate_data_transformation(self, train_path, test_path):        
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            features_preprocessing_object = self.get_features_transformer_object()

            train_df_preprocessed = features_preprocessing_object.fit_transform(train_df)
            test_df_preprocessed = features_preprocessing_object.transform(test_df)

            logging.info(f"train_df_preprocessed type: {type(train_df_preprocessed)}")
            logging.info(f"train_df: {train_df_preprocessed}")

            target_col_name = "value"
            filter_for = ['HKQuantityTypeIdentifierStepCount']
            
            features_train_df = train_df.drop(columns=[target_col_name], axis=1)
            target_train_df = train_df[target_col_name]

            features_test_df = self.filter_type(filter_for, test_df.drop(columns=[target_col_name], axis=1))
            target_test_df = features_test_df[target_col_name]

            logging.info('Initiating application of preprocessing objects on train and test dataframes')

            features_train_arr = features_preprocessing_object.fit_transform(features_train_df)
            features_test_arr = features_preprocessing_object.transform(features_test_df)

            train_arr = np.c_[features_train_arr, np.array(target_train_df)]
            test_arr = np.c_[features_test_arr, np.array(target_test_df)]

            save_object(
                file_path=self.data_transformation_config.features_preprocessor_obj_file_path,
                obj=features_preprocessing_object
            )

            logging.info("Data tansformation complete.")
            logging.info(f"train arr: {train_arr}")
            logging.info(f"test arr: {test_arr}")

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.features_preprocessor_obj_file_path,      
            )

        except Exception as e:
            logging.error(f"Error in initiate_data_transformation: {e}")
            raise CustomException(e, sys)