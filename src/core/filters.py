    
from datetime import timedelta, datetime
from typing import Callable, Any
from dataclasses import dataclass
 
@dataclass
class FilterData:
    key: str
    data: object

class TimeSeriesFilter(object):
    ''' Time Series Filter 
    Looks for a running sequence of data over a gven timespan
    If threshold is met, the filter calls the notification callback.
    Once the time series is met, the data is ignored until ignorespan is reached.

    Note: This implementation resets the time series if the data is different to the recorded data series
    ''' 
    
    def __init__(self, threshold: int, timespan: timedelta, ignorespan: timedelta, notification: Callable):
        self.threshold = threshold
        self.timespan = timespan
        self.ignorespan = ignorespan
        self.notification = notification
        self.reset()

    def reset(self):
        self.datas = []
        self.start_time = datetime.now()
        self.start_ignore = None

    def add(self, key: str, data: object):
        ''' Add data to filter
        Triggers notification if time series criteria are met 
        '''

        now = datetime.now()

        # First check if we are in ignore span
        if self.start_ignore is not None and now-self.start_ignore < self.ignorespan:
            return
    
        # If empty data, start new datas
        if len(self.datas) == 0:
            self.reset()

        filterData = FilterData(key, data)

        # Check last data. If this is the same and within timespan, add to datas else reset
        last_data = self.datas[0] if len(self.datas) > 0 else filterData

        if now-self.start_time < self.timespan and last_data.key == filterData.key:
            self.datas.append(filterData)
        else:
            self.reset()

        # If threshold met, notify and start ignorespan
        if len(self.datas) == self.threshold:
            self.notification(self.datas[0].data)
            self.reset()
            self.start_ignore = datetime.now()

class MultiTimeSeriesFilter(object):
    ''' Multiple Object Time Series Filter 
    Uses TimeSeriesFilter to implement time series logic for multiple objects. 
    So if the filter sees a run of object1 it will fire for that object. 
    If it sees another object it will pass this to another TimeSeriesFilter
    ''' 
    def __init__(self, threshold: int, timespan: timedelta, ignorespan: timedelta, notification: Callable):
        self.filters = dict()
        self.threshold = threshold
        self.timespan = timespan
        self.ignorespan = ignorespan
        self.notification = notification

    def add(self, key: str, data: object):
        ''' Add data to filter
        Triggers notification if time series criteria are met 
        '''

        if key not in self.filters:
            self.filters[key] = TimeSeriesFilter(threshold=self.threshold, timespan=self.timespan, ignorespan=self.ignorespan, notification=self.notification)
        
        self.filters[key].add(key, data)
