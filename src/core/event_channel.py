import logging
from threading import Thread, Event
from core import helpers
from typing import List

class EventChannel(object):

    class Subscriber(object):
        
        def __init__(self):
            self.trigger = Event()
            self.args = None
            self.kwargs = None
            self.thread = Thread(target=self.run, daemon=True).start()
            self.callbacks = []
        
        def subscribe(self, callback):
            self.callbacks.append(callback)
                
        def unsubscribe(self, callback) -> bool:
            if callback not in self.callbacks:
                return False
            
            self.callbacks.remove(callback)
            return True
        
        def triggerevent(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs
            self.trigger.set()
            
        def run(self):
            while True:
                if self.trigger.wait(10):
                    self.trigger.clear()
                    for callback in self.callbacks:
                        callback(*self.args, **self.kwargs)

    def __init__(self):
        logger = logging.getLogger(__name__)
        helpers.init_logger(logger)
        self.logger = logger
        self.subscribers = {}

    def subscribe(self, event, callback):
        if event is None or event == "":
            self.logger.warning("Event cant be empty")
            return
        
        if not callable(callback):
            self.logger.warning(f"Callback for event {event} is not callable.")
            return
        
        if event not in self.subscribers.keys():
            self.subscribers[event] = EventChannel.Subscriber()
            
        subscriber: EventChannel.Subscriber = self.subscribers[event]
        subscriber.subscribe(callback)
        
    def unsubscribe(self, event, callback):
        if event is None or event != "":
            self.logger.warning("Event cant be empty")
            return
            
        if event not in self.subscribers.keys():
            self.logger.warning(f"Event {event} not found")
            return

        subscriber: EventChannel.Subscriber = self.subscribers[event]
        subscriber.unsubscribe(callback)
        
    def publish(self, event, *args, **kwargs):
        if event in self.subscribers.keys():            
            subscriber: EventChannel.Subscriber = self.subscribers[event]
            subscriber.triggerevent(*args, **kwargs)
                