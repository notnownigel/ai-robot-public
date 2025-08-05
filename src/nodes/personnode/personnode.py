import os
from threading import Thread, Event
from datetime import timedelta
from core import Node, TimeSeriesFilter, Person, Shared

class PersonNode(Node):
    def __init__(self):
        super().__init__(name=__name__)
    
    def start(self): 
        super().start()
        self.node_event_channel.subscribe("person-detected", self.detected)
        self.filter = TimeSeriesFilter(
            threshold=int(os.getenv("PERSON_FILTER_THRESHOLD")), 
            timespan=timedelta(seconds=int(os.getenv("PERSON_FILTER_TIMESPAN"))), 
            ignorespan=timedelta(seconds=int(os.getenv("PERSON_FILTER_IGNORESPAN"))), 
            notification=self.newperson)
        
        self.lonely_event = Event()
        Thread(target=self.lonely_check, daemon=True).start()

    def lonely_check(self):
        self.lonely_event.set()

        while self.running is True:
            if self.lonely_event.wait(int(os.getenv("BOREDOM_THRESHOLD"))):   
        
                if Shared.manual_mode is False:
                    self.node_event_channel.publish("stop-looking-around")
        
                self.lonely_event.clear()
                continue
            
            # timed out so - lonely
            if Shared.manual_mode is False:
                self.info(f"I'm lonely")
                self.node_event_channel.publish("start-looking-around")

    def detected(self, person: Person):
        self.lonely_event.set()
        self.filter.add(person.name, person)
        self.node_event_channel.publish("centre-thing", person)

    def newperson(self, person: Person):
        self.info(f"New Person: {person.name}")        
        self.node_event_channel.publish("llm-generate-greeting", person = person)
        

