from datetime import datetime
import os
import pickle
from flask import Flask, request, jsonify
import pandas as pd
import data_extract_module

app = Flask(__name__)

base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, 'step_predict_model.pkl')

try:
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
except FileNotFoundError:
    raise Exception(f"Model file not found at {model_path}")
except Exception as e:
    raise Exception(f"Error loading model: {str(e)}")

""" @app.route('/clean-data', methods=['POST'])
def clean_data():
    raw_data = request.json
    cleaned_data = data_extract_module.extract_data(raw_data)
    return jsonify(cleaned_data)
 """

@app.route('/predict', methods=['GET'])
def predict():
    try:
        # extracted_data = data_extract_module.extract_data()

        data = {
             "active_energy_burned": [88.759],
            "basal_energy_burned": [1318.523],
            "exercise_time": [6],
            "stand_time": [37],
            "walking_running_distance": [4.475133]}
        
        df = pd.DataFrame(data)
        input_data = df.values

        prediction = model.predict(input_data)
        return jsonify({'prediction': int(prediction)})

    except Exception as e:
        return jsonify({'error': str(e)}), 400 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)
