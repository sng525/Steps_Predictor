from src.components.data_ingestion import DataIngestion 
import pytest
from unittest.mock import patch, MagicMock
import os

@pytest.fixture
def data_ingestion():
    return DataIngestion()

@patch('src.componants.data_ingestion.ET')
@patch('src.componants.data_ingestion.os.makedirs')
@patch('src.companants.data_ingestion.train_test_split')
@patch('src.componants.data_ingestion.logging')
def test_initiate_data_ingestion(mock_logging, mock_train_test_split, mock_makedirs, mock_ET, data_ingestion):
    #Arrange
    mock_tree = MagicMock()
    mock_root = MagicMock()

    mock_ET.parse.return_value = mock_tree
    mock_tree.get_root.return_value = mock_root
    mock_makedirs.return_value = None

    mock_train_test_split.return_value = (mock_tree, mock_tree)

    #Act
    traind_data_path, test_data_path = data_ingestion.initiate_data_ingestion()

    #Assert
    assert traind_data_path == data_ingestion.ingestion_config.train_data_path
    assert test_data_path == data_ingestion.ingestion_config.test_data_path

    mock_makedirs.assert_called_once_with(os.path.dirname(data_ingestion.ingestion_cofig.raw_data_path))
    mock_train_test_split.assert_called_once_with(mock_tree, test_size=0.2, random_state=42)

    mock_tree.write.assert_any_call(data_ingestion.ingestion_cofig.raw_data_path, index=False, header=True)
    mock_tree.write.assert_any_call(data_ingestion.ingestion_cofig.train_data_path, index=False, header=True)
    mock_tree.write.assert_any_call(data_ingestion.ingestion_config.test_data_path, index=False, header=True)