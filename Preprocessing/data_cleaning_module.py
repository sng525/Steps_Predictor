def clean_data(data):
    cleaned_data = {
        "date": data.get("date"),
        "steps": data.get("steps")
    }
    return cleaned_data