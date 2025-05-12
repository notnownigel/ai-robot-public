    
from datetime import timedelta, datetime
from typing import Callable

class TimeSeriesFilter(object):
    def __init__(self, threshold: int, timespan: timedelta, ignorespan: timedelta, notification: Callable):
        self.threshold = threshold
        self.timespan = timespan
        self.ignorespan = ignorespan
        self.notification = notification
        self.reset()

    def reset(self):
        self.data = None
        self.key = None
        self.count = 0
        self.start_time = datetime.now()
        self.start_ignore = None

    def add(self, key: str, data: object):
        now = datetime.now()

        # First check if we are in ignore span
        if self.start_ignore is not None and now-self.start_ignore < self.ignorespan:
            return
    
        # If empty data, start new datas
        if self.count == 0:
            self.reset()

        if self.key is None:
            self.key = key
            
        # Check last data. If this is the same and within timespan, add to datas else reset
        if now-self.start_time < self.timespan and self.key == key:
            self.data = data
            self.count += 1
        else:
            self.reset()

        # If threshold met, notify and start ignorespan
        if self.count == self.threshold:
            self.notification(self.data)
            self.reset()
            self.start_ignore = datetime.now()

class MultiTimeSeriesFilter(object):
    def __init__(self, threshold: int, timespan: timedelta, ignorespan: timedelta, notification: Callable):
        self.filters = dict()
        self.threshold = threshold
        self.timespan = timespan
        self.ignorespan = ignorespan
        self.notification = notification

    def add(self, key: str, data: object):
        if key not in self.filters:
            self.filters[key] = TimeSeriesFilter(threshold=self.threshold, timespan=self.timespan, ignorespan=self.ignorespan, notification=self.notification)
        
        self.filters[key].add(key, data)
