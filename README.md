DROAN - An Intelligent Vision-Based Approach for Road Damage Detection using a Semi-Automated Aerial Drone

This repository contains the python scripts for the thesis of DLSU-MEM students Julio Manuel A. Diokno, Allen Philip D. Matias, Ellysa D. Pua, Fiorell Ernest A. Rodriguez, and Aliah Jean B. Tan.

The main program of the repository is titled main_file.py, while the program for the YOLOv4 model with the DeepSORT tracking algorithm embedded into it is found in the file object_tracker.py. The exact codes for playing the results video using threading can be seen in threaded_video.py, and showing the table for the detected damages is done using the show_table.py file. To obtain the confusion matrix of the testing done using the model, the testing_accuracy.py script was used. Lastly, the map_test.py file can be used to plot the longitude and latitude of the detected damages onto a map.

The yolov4 and deepsort files are cloned from the Github repositories of TheAIGuy [1], and some functions of the program are adapted from creditable works of X. Lu [2], D. Farrell [3], and Nathancy [4].

[1] The AI Guy, yolov4-deepsort: Object tracking implemented with YOLOv4, DeepSort, and TensorFlow.
[2] “User Xiaoyu Lu,” Stack Overflow. [Online]. Available: https://stackoverflow.com/users/7037228/xiaoyu-lu. 
[3] “Code Examples — pandastable documentation,” Readthedocs.io. [Online]. Available: https://pandastable.readthedocs.io/en/latest/examples.html. 
[4] “User nathancy,” Stack Overflow. [Online]. Available: https://stackoverflow.com/users/11162165/nathancy.
