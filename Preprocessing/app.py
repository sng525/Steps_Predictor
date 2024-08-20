from flask import Flask, request, jsonify
import data_cleaning_module

app = Flask(__name__)

@app.route('/clean-data', methods=['POST'])
def clean_data():
    raw_data = request.json
    cleaned_data = data_cleaning_module.clean(raw_data)
    return jsonify(cleaned_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
