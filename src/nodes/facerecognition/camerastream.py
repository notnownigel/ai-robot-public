import os
from .cam_pi import CamPi
from .cam_usb import CamUsb

# Class for threaded handling of picam2
class CameraStream:
    def __init__(self, title="Camera Stream"):
        self.title = title
        self.stopped = True 
 
    def start(self) -> None:
        self.stopped = False

        cameraType = os.getenv("CAMERA_TYPE")
        if cameraType == "PICAMERA":
            self.cam = CamPi()
        elif cameraType == "USB":
            self.cam = CamUsb()
        
        self.cam.start()

    def stop(self) -> None:
        self.cam.stop()
        self.stopped = True
  
    def frame_generator(self):
        try:
            while True:
                yield self.cam.get_frame()
        finally:
            self.stop()  # Stop the camera when the generator is closed
