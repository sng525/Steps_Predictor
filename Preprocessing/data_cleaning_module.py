import json


def clean_data(data):
    first_10_entries = data[:10]
    cleaned_data = json.dumps(first_10_entries, indent=4)
    return cleaned_data