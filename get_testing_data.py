import os
import pandas as pd

ground_truth_path = 'testing/testing.v2i.darknet/train'
os.chdir(ground_truth_path)
annotations = []
i = 0
for file in os.listdir(os.getcwd()):
    if file.endswith('.txt'):
        with open(file) as f:
            lines = f.readlines()
            for line in lines:
                clean_line = line.replace(' ', ', ')
                clean_line = clean_line.rstrip('\n').split(',')
                if i < 8:
                    longitude = 121.0880925
                    latitude = 14.63393491
                elif 8 <  i < 16:
                    longitude = 121.0880912
                    latitude = 14.63393474
                elif 16 < i < 24:
                    longitude = 121.0880894
                    latitude = 14.63393464
                elif 24 < i < 32:
                    longitude = 121.0880886
                    latitude = 14.6339351
                else:
                    longitude = 121.0880882
                    latitude =  14.63393523
                clean_line.append(longitude)
                clean_line.append(latitude)
                annotations.append(clean_line)
                i += 1

clean_annotations = [x for x in annotations if x]

final_annotations = []
for obj in clean_annotations:
    if obj[0] == '0':
        severity = 'Minimal'
    elif obj[0] == '1':
        severity = 'Tolerable'
    else:
        severity = 'Severe'
    alt_mult_w = 376 # Based on altitude (in cm)
    alt_mult_h = 675 # Based on altitude (in cm)
    width = float(obj[3])
    height = float(obj[4])
    actual_width = width * alt_mult_w * 0.01
    actual_height = height * alt_mult_h * 0.01
    size = (actual_width * actual_height)
    longitude2 = float(obj[5])
    latitude2 = float(obj[6])
    final_detection = [size, severity, longitude2, latitude2]
    final_annotations.append(final_detection)

df = pd.DataFrame(final_annotations, columns=['Size (m^2)', 'Severity', 'Longitude', 'Latitude'])
os.chdir('../../..')
df.to_csv('outputs/ground_truth.csv', index=False)