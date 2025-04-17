from dataclasses import dataclass

@dataclass()
class Thing(object):
    bbox: tuple
    offset: tuple
    
@dataclass()
class Person(Thing):
    name: str
    match_score: float
    person_score: int
