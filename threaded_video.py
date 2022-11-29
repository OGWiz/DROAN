import cv2, time
from threading import Thread

class ThreadedVideo(object):
    def __init__(self, path):
        self.capture = cv2.VideoCapture(path)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)
       
        # FPS = 1/X
        # X = desired FPS
        self.FPS = 1/30
        self.FPS_MS = int(self.FPS * 1000)
        
        # Start frame retrieval thread
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        
    def update(self):
        while self.capture.isOpened():
            (self.status, self.frame) = self.capture.read()
            if not self.status:
                break
            time.sleep(self.FPS)
            
    def show_frame(self):
        cv2.namedWindow("Results", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("Results", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Results", self.frame)
        cv2.waitKey(self.FPS_MS)