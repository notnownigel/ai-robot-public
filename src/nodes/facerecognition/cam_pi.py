import numpy as np
from .cam_base import CamBase
from picamera2 import Picamera2

class CamPi(CamBase):
    def __init__(self):
        super().__init__()

    def start(self) -> None:
        self.logger.info("Picamera Camera Init")
        self.cam = Picamera2()
        self.cam.configure(self.cam.create_preview_configuration({'format': 'RGB888'}))
        self.cam.start()
        self.stopped = False

    def stop(self) -> None:
        self.cam.stop()        
        self.stopped = True
  
    def get_frame(self) -> np.ndarray:
        return self.cam.capture_array()