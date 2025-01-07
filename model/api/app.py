from flask import Flask, jsonify, abort, request
import requests
import subprocess
import os
import sys

module_dir = os.path.abspath(r"C:\Users\olish\Documents\ml_projects\Steps_Predictor\ml_model")
sys.path.insert(0, module_dir)

import model_training

app = Flask(__name__)

BASE_URL = "http://localhost:5170"
RETRIEVED_FILE_DIR = r"files"
RETRIEVED_FILE_NAME = r"retrieved_file.csv"
#MODEL_DIR = 'ml_model\model_training.py'

@app.route('/get-file/<filename>', methods=['GET'])

def get_file(filename):

    file_url = f'{BASE_URL}/files?fileName={filename}'
    response = requests.get(file_url)

    print(f"File URL: {file_url}")

    try:
        print(f"Response Status Code: {response.status_code}")

        if response.status_code==200:
            print("response code is 200")

            # Debugging directory existence
            if not os.path.exists(RETRIEVED_FILE_DIR):
                print(f"Directory {RETRIEVED_FILE_DIR} does not exist, creating it.")
                os.makedirs(RETRIEVED_FILE_DIR, exist_ok=True)
            else:
                print(f"Directory {RETRIEVED_FILE_DIR} already exists.")

            # Debugging file path
            retreived_file_path = os.path.join(RETRIEVED_FILE_DIR, RETRIEVED_FILE_NAME)
            print(f"Retrieved File Path: {retreived_file_path}")

            retreived_file_path = os.path.normpath(retreived_file_path)
            print(f"Normalized File Path: {retreived_file_path}")

            # Debugging response content length
            content_length = len(response.content)
            print(f"Content length: {content_length} bytes")

            with open(retreived_file_path, 'wb') as file:
                file.write(response.content) 
            print("File written successfully.")

            filepath = "files/retrieved_file.csv"
            try:
                model_training.main(filepath, 'Species')
                print("model trainining pipeline executed successfuly")
                return jsonify({'message':'file retrieved and model pipeline executed'}), 200
            except Exception as e:
                print("Error running model pipeline")
                return jsonify({'error': 'error running model pipeline'}), 500
        
        elif response.status_code == 404:
            print("file not found on the server.")
            return jsonify({'error': 'file not found'}), 404
            
        elif response.status_code == 404:
                print("File not found on the server.")
                return jsonify({'error': 'File not found'}), 404
        
        else:
            print(f"Failed to retrieve file. Status code: {response.status_code}")
            return jsonify({'error':'failed to retrieve file'}), response.status_code
    
    except Exception as e:
        print(f"Exception occurred: {e}")
        return jsonify({'error': str(e)}), 500
    
if __name__=='__main__':
    app.run(debug=True)


#if the model training process is resource-intensive, 
# consider managing concurrent executions or using a task queue 
# (like Celery) to handle background tasks efficiently.