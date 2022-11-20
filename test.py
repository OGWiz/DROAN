import pandas as pd
from show_table import TableApp

df_detections = pd.read_csv('outputs/detections.csv')

list_of_detections = []
for _, row in df_detections.iterrows():
    detection_time = row[0]
    class_id = str(row[1])
    detection_class = class_id[:2]
    class_dict = {'d1': 'Low', 'd2': 'Medium', 'd3': 'Severe'}
    severity = class_dict.get(detection_class)
    width = row[2]
    height = row[3]
    size = width * height
    info_list = [size, severity, detection_time]
    list_of_detections.append(info_list)

df = pd.DataFrame(list_of_detections, columns=['Bbox Size', 'Severity', 'Time'])

# Using time of each detection, get actual size and gps coords
new_list = []
for _, row in df.iterrows():
    detection_time = row[2]
    # With this, get time from flight logs and from that get gps coords
    altitude = "1"
    denominator = int(altitude)
    actual_size = row[0] / denominator
    longitude = "***"
    latitude = "***"
    new_list.append([row[0], row[1], longitude, latitude])
    
df_detections_clean = pd.DataFrame(new_list, columns = ['Size', 'Severity', 'Longitude', 'Latitude'])
df_detections_clean.to_csv('outputs/clean_detections.csv', index = False)

# With tkinter, show results
TableApp()