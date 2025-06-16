from datetime import timedelta, datetime
from typing import Callable

class TimeSeriesFilter(object):
    def __init__(self, threshold: int, timespan: timedelta, ignorespan: timedelta, notification: Callable):
        self.filterpools = dict()
        self.threshold = threshold
        self.timespan = timespan
        self.ignorespan = ignorespan
        self.notification = notification

    def add(self, key: str, data: object):
        
        # create filter pool if not found
        if key not in self.filterpools:
            self.filterpools[key] = FilterPool(threshold=self.threshold, timespan=self.timespan, ignorespan=self.ignorespan, notification=self.notification)

        # add to filter pool        
        self.filterpools[key].add(data)

        # prune all filter pools        
        self.prune()
        
        # check filter pool
        self.filterpools[key].check()
        
    def prune(self):
        for _, filterpool in self.filterpools.items():
            filterpool.prune()
            
class FilterPool(object):
    def __init__(self, threshold: int, timespan: timedelta, ignorespan: timedelta, notification: Callable):
        self.threshold = threshold
        self.timespan = timespan
        self.ignorespan = ignorespan
        self.notification = notification
        self.ignore_until = datetime.min
        self.reset()
        
    def reset(self):
        self.data = None
        self.pool = []
        
    def add(self, data: object):
        ts = datetime.now()
        # if in ignore span, ignore
        if ts < self.ignore_until:
            return
        
        # else add event to pool
        self.data = data
        self.pool.append(ts)
    
    def prune(self):
        window_start = datetime.now() - self.timespan
        self.pool[:] = [ts for ts in self.pool if ts >= window_start]
    
    def check(self):
        if len(self.pool) == self.threshold:
            self.ignore_until = datetime.now() + self.ignorespan
            self.notification(self.data)
            self.reset()
