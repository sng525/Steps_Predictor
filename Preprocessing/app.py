from flask import Flask, request, jsonify
import data_extract_module
import pickle

import pandas as pd

app = Flask(__name__)

with open('step_predict_model.pkl', 'rb') as file:
    model = pickle.load(file)


@app.route('/clean-data', methods=['POST'])
def clean_data():
    raw_data = request.json
    cleaned_data = data_extract_module.clean_data(raw_data)
    return jsonify(cleaned_data)

@app.route('/predict', methods=['GET'])
def predict(data): 
    # data = pd.read_csv("steps_count.csv")
    prediction = model.predict(data)
    return jsonify(prediction)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
