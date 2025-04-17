import logging
from core import helpers
from core.event_channel import EventChannel
from threading import Thread, Event

# Base class for Node
class Node(object):
    node_event_channel = EventChannel()
    
    def __init__(self, name):
        self.node_event_channel = Node.node_event_channel
        self.name = name
        self.last_message = "-"
        self.last_error = "-"
        logger = logging.getLogger(self.name)
        helpers.init_logger(logger)
        self.logger = logger
        self.running = False

    def run_every(self, timeout: int, callback):
        self.run_every_trigger = Event()
        self.run_every_timeout = timeout
        self.run_every_callback = callback
        Thread(target=self.timer_run, daemon=True).start()

    def timer_run(self):
        while self.running:
            self.run_every_trigger.wait(30)
            self.run_every_trigger.clear()
            self.run_every_callback()

    def info(self, msg: str, *args, **kwargs):
        self.last_message = msg.format(*args, **kwargs)
        self.logger.info(msg, *args, **kwargs)
 
    def warning(self, msg: str, *args, **kwargs):
        self.last_error = msg.format(*args, **kwargs)
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        self.last_error = msg.format(*args, **kwargs)
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs):
        self.last_error = msg.format(*args, **kwargs)
        self.logger.critical(msg, *args, **kwargs)

    def start(self):
        if self.running is False:
            self.info("Starting Node...")
            self.running = True
            
    def stop(self):
        self.info("Stopping Node.")

        if self.running is True:
            self.running = False
