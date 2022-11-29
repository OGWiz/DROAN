# No GUI
import cv2
import subprocess
import pandas as pd
from tkinter import *
from tkinter import filedialog
from threaded_video import ThreadedVideo

if __name__ == '__main__':
    # Create tkinter instance and hide window
    root = Tk()
    root.wm_withdraw()

    # Ask for video
    video_path = filedialog.askopenfilename()
    # Ask for flight logs
    flight_log_path = filedialog.askopenfilename()

    # Delete tkinter instance
    root.destroy()

    # Check if flight logs are valid
    if flight_log_path.endswith('.csv'):
        df_true = pd.read_csv(flight_log_path)
    elif flight_log_path.endswith('.xlsx'):
        df_true = pd.read_excel(flight_log_path)
    else:
        print('Invalid data type')
        exit()

    # Convert video and flight logs to dataframe with needed info per frame
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = []

    while cap.isOpened():
        _ret, frame = cap.read()
        if frame is None:
            break
        frames.append(frame)
    cap.release()
    no_of_seconds = int(len(frames) / 30)
    a_list = []
    for i in range(no_of_seconds):
        true_row = df_true.iloc[i]
        latitude = str(true_row[4])
        longitude = str(true_row[5])
        altitude = str(true_row[6])
        the_list = [i, longitude, latitude, altitude]
        a_list.append(the_list)

    df_converted = pd.DataFrame(a_list, columns = ['Frame Number', 'Longitude', 'Latitude', 'Altitude'])
    df_converted.to_csv('outputs/converted.csv')

    # FOR TESTING:
    '''
    SAVE YOLO MODEL:
    call(["python", "save_model.py", "--weights", "./data/yolov4-custom_final.weights", "--output", 
    "./checkpoints/yolov4-416", "--input_size", "416", "--model", "yolov4"])

    *OLD* RUN YOLO ON VIDEO:
    call(["python", "detect_video.py", "--weights", "./checkpoints/yolov4-416", "--size", '416', 
    "--model", "yolov4", "--video", video_path, "--output", "./detections/results.mp4", "--dont_show", "--count"])
    '''

    # Run yolov4 with DEEPSORT tracking on video
    output_path = './outputs/results.avi'
    args = ["python", "object_tracker.py", "--weights", "./checkpoints/yolov4-416", "--size", '416', 
    "--model", "yolov4", "--video", video_path, "--output", output_path, "--dont_show", "--info"]
    subprocess.call(args, shell=False)

    # Play results video with video threading for enhanced FPS
    threaded_video = ThreadedVideo(output_path)
    while True:
        try:
            threaded_video.show_frame()
        except AttributeError:
            pass
        except:
            cv2.destroyAllWindows()
            for i in range (1,5):
                cv2.waitKey(1)
            break

    # Read detections (Has frame number, class + id, width, and height)
    df_detections = pd.read_csv('outputs/detections.csv')
    list_of_detections = []
    for _, row in df_detections.iterrows():
        frame_num = row[0]
        class_id = str(row[1])
        detection_class = class_id[:2]
        class_dict = {'d1': 'Minimal', 'd2': 'Tolerable', 'd3': 'Severe'}
        severity = class_dict.get(detection_class)
        width = row[2]
        height = row[3]
        info_list = [width, height, severity, frame_num, class_id]
        list_of_detections.append(info_list)

    df = pd.DataFrame(list_of_detections, columns=['Width', 'Height', 'Severity', 'Frame Number', 'Class ID'])
    # Using frame number of each detection, get actual size and gps coords
    new_list = []
    for _, row in df.iterrows():
        the_class_id = row[4]
        frame_no = int(row[3] / 30)
        true_row = df_converted.iloc[frame_no]
        longitude = true_row[1]
        latitude = true_row[2]
        true_alt = true_row[3]
        alt = float(true_alt) * 0.3048
        alt_mult_w = 376 # Based on altitude (in cm)
        alt_mult_h = 675 # Based on altitude (in cm)
        width = float(row[0])
        height = float(row[1])
        actual_width = (width / 416) * alt_mult_w * 0.01
        actual_height = (height / 416) * alt_mult_h * 0.01
        size = (actual_width * actual_height)
        new_list.append([size, row[2], longitude, latitude, frame_no, the_class_id])

    df_detections_clean = pd.DataFrame(new_list, columns = ['Size (m^2)', 'Severity', 'Longitude', 'Latitude', 'Time of Detection', 'Class ID'])
    df_detections_clean.to_csv('outputs/clean_detections.csv', index = False)
    
    # With tkinter, show results
    subprocess.call(["python", "show_table.py"], shell = False)


    # Add time and groond truth and accuracy