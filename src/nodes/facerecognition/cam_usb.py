import numpy as np
import cv2
from .cam_base import CamBase

class CamUsb(CamBase):
    def __init__(self):
        super().__init__()
 
    def start(self) -> None:
        self.cam = cv2.VideoCapture(0)
        self.save_resolution(self.cam.get(3), self.cam.get(4))

        self.logger.info("USB Camera Init")

        if self.cam.isOpened() is False:
            self.logger.critical("[Exiting]: Error accessing webcam stream.")
            exit(0)
 
        self.grabbed , self.frame = self.cam.read()

        if self.grabbed is False :
            self.logger.critical('[Exiting] No more frames to read')
            exit(0)        
        
        self.stopped = False

    def stop(self) -> None:       
        self.cam.release() 
        self.stopped = True
  
    def get_frame(self) -> np.ndarray:
        self.grabbed , self.frame = self.cam.read()

        if self.grabbed is False:
            exit(0)        

        return self.frame
