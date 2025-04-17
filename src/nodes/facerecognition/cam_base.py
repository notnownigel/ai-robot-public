import numpy as np
import logging
from core import helpers


class CamBase:
    def __init__(self):
        logger = logging.getLogger(__name__)
        helpers.init_logger(logger)
        self.logger = logger
        self.stopped = True 

 
    def start(self) -> None:
        pass

    def stop(self) -> None:  
        pass
  
    def get_frame(self) -> np.ndarray:
        pass
