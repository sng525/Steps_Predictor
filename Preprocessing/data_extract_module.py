from collections import defaultdict
import pandas as pd
from datetime import datetime
import xml.etree.ElementTree as ET # https://docs.python.org/3/library/xml.etree.elementtree.html

xml_path = "apple_health_export/export.xml"
tree = ET.parse(xml_path)
root = tree.getroot()

types_set = [
    "HKQuantityTypeIdentifierWalkingSpeed",
    "HKQuantityTypeIdentifierPhysicalEffort", 
    "HKQuantityTypeIdentifierBasalEnergyBurned",
    "HKQuantityTypeIdentifierHeartRate",
    "HKQuantityTypeIdentifierAppleExerciseTime",
    "HKQuantityTypeIdentifierAppleStandTime",
    "HKQuantityTypeIdentifierWalkingStepLength",
    "HKQuantityTypeIdentifierDistanceWalkingRunning",
    "HKQuantityTypeIdentifierRespiratoryRate",
    "HKQuantityTypeIdentifierStepCount",
    "HKQuantityTypeIdentifierActiveEnergyBurned"
]
records = []

# def extract_types():
#     for record in root.findall('.//Record'):
#         type_attribute = record.get('type')
#         if type_attribute:
#             types_set.add(type_attribute)

def extract_data():
    for record in root.findall('.//Record[@type]'):
        if record.get('type') in types_set:
            records.append({
            'type': record.get('type'),
            'source_name': record.get('sourceName'),
            'start_date': record.get('startDate'),
            'end_date': record.get('endDate'),
            'value': record.get('value'),
            'unit': record.get('unit'),
    })


        # datetime_obj = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S %z')
        # date_only = datetime_obj.date()
        # records[date_only] += value

    df = pd.DataFrame(records, columns=['type', 'source_name', 'start_date', 'end_date', 'value', 'unit'])
    df.to_csv("steps_count.csv", index=False)

extract_data()

# extract_types()
# for type_value in types_set:
#     print(type_value)

    
