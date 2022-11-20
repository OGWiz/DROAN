import cv2
from threading import Thread
from queue import Queue

class FileVideoStream:
    def __init__(self, path, queuesize = 128):
        self.stream = cv2.VideoCapture(path)
        self.stopped = False
        self.Q = Queue(maxsize=queuesize)

    def start(self):
        t = Thread(target = self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return
            
            if not self.Q.full():
                (grabbed, frame) = self.stream.read()
                if not grabbed:
                    self.stop()
                    return
            
            self.Q.put(frame)
    
    def read(self):
        return self.Q.get()
    
    def more(self):
        return self.Q.qsize() > 0

    def stop(self):
        self.stopped = True

'''
fvs = FileVideoStream("outputs/results1.avi").start()
    time.sleep(1)
    fps = FPS().start()
    while fvs.more():
	# grab the frame from the threaded video file stream, resize
	# it, and convert it to grayscale (while still retaining 3
	# channels)
        frame = fvs.read()
        frame = imutils.resize(frame, width=450)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = np.dstack([frame, frame, frame])
        # display the size of the queue on the frame
        cv2.putText(frame, "Queue Size: {}".format(fvs.Q.qsize()),
            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)	
        # show the frame and update the FPS counter
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) == ord('q'):
            break
        fps.update()
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    # do a bit of cleanup
    cv2.destroyAllWindows()
    fvs.stop()
'''