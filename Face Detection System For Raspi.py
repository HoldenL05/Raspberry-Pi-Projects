#import the necesary packages
from thread import start_new_thread
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture =  PiRGBArray(camera, size=(640, 480))
inThread = False
# allow the camera to warmup
time.sleep(0.1)
face_cascade = cv2.CascadeClassifier('haar.xml')
face = []
def face(img):
    global inThread
    global face_cascade
    global faces
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    print "Found"+str(len(faces))+" face(s)"
    inThread = False

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        if not inThread:
                start_new_thread(face,(image,))
                inThread = True
        for (x,y,w,h) in faces:
                cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)

        # show the frame
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF

        # clear tge stream in preperation for the next frame
        rawCapture.truncate(0)

        #if the 'q' key was pressed, break from loop
        if key == ord("q"):
                breaks
