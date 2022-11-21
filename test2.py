from threaded_video import ThreadedVideo
import cv2
import pandas as pd
from tkinter import *
from pandastable import Table
import matplotlib
matplotlib.use('TkAgg')

class Table:
    def __init__(self, root):
        for i in range(total_rows):
            for j in range(total_columns):
                 
                self.e = Entry(root, width=20, fg='blue',
                               font=('Arial',16,'bold'))
                 
                self.e.grid(row=i, column=j)
                self.e.insert(END, new_list[i][j])

results_path = "outputs/results.avi"

# Video threading for enhanced FPS
threaded_video = ThreadedVideo(results_path)
while True:
    try:
        threaded_video.show_frame()
    except AttributeError:
        pass
    except:
        break

cv2.destroyAllWindows()

# Read detections (Has time, class + id, width, and height)
df_detections = pd.read_csv('outputs/detections.csv')
list_of_detections = []
for _, row in df_detections.iterrows():
    detection_time = row[0]
    class_id = str(row[1])
    detection_class = class_id[:2]
    class_dict = {'d1': 'Low', 'd2': 'Medium', 'd3': 'Severe'}
    severity = class_dict.get(detection_class)
    width = row[2] / 416
    height = row[3] / 416
    size = width * height
    info_list = [size, severity, detection_time]
    list_of_detections.append(info_list)

df = pd.DataFrame(list_of_detections, columns=['Bbox Size', 'Severity', 'Time'])

# Using time of each detection, get actual size and gps coords
new_list = [['Size', 'Severity', 'Longitude', 'Latitude']]
for _, row in df.iterrows():
    detection_time = row[2]
    # With this, get time from flight logs and from that get gps coords
    altitude = "1"
    denominator = int(altitude)
    actual_size = row[0] / denominator
    longitude = "Test"
    latitude = "Test"
    new_list.append([row[0], row[1], longitude, latitude])
    
df_detections_clean = pd.DataFrame(new_list, columns = ['Size', 'Severity', 'Longitude', 'Latitude'])
total_rows = len(new_list)
total_columns = len(new_list[0])
  
# With tkinter, show results
root2 = Tk()
t = Table(root2)
root2.mainloop()