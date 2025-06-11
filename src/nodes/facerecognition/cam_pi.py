import numpy as np
from .cam_base import CamBase
from picamera2 import Picamera2
import libcamera

class CamPi(CamBase):
    def __init__(self):
        super().__init__()

    def start(self) -> None:
        self.logger.info("Picamera Camera Init")
        self.cam = Picamera2()
        width=640
        height=480
        lores = {'size': (width, height), 'format': 'RGB888'}
        controls = {'FrameRate': 30}
        config = self.cam.create_preview_configuration(lores=lores, controls=controls)
        config["transform"] = libcamera.Transform(hflip=1, vflip=1)
        self.cam.configure(config)
        self.save_resolution(width, height)
        self.cam.set_controls({'Saturation': 0})
        self.cam.start()
        self.stopped = False

    def stop(self) -> None:
        self.cam.stop()        
        self.stopped = True
  
    def get_frame(self) -> np.ndarray:
        return self.cam.capture_array('lores')