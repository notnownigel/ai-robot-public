import os
import pygame
import time
from threading import Thread, Event
from core.node import Node
from gtts import gTTS
from io import BytesIO

class SpeechNode(Node):
    def __init__(self):
        self.messages = []
        super().__init__(name=__name__)
    
    def start(self): 
        super().start()
        self.node_event_channel.subscribe("speech-node-speak", self.speak)
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.set_volume(1.0)
        self.speak_event = Event()
        Thread(target=self.run, daemon=True).start()
    
    def run(self):
        while self.running is True:

            if self.speak_event.wait(10):
                self.speak_event.clear()
                while len(self.messages):
                    mp3 = BytesIO()
                    tts = gTTS(self.messages.pop(0), lang=os.getenv("SPEECH_LANGUAGE"))
                    tts.write_to_fp(mp3)
                    mp3.seek(0)
                    pygame.mixer.music.load(mp3, "mp3")
                    pygame.mixer.music.play()
            
                    while pygame.mixer.music.get_busy():
                        pygame.event.poll()
                        time.sleep(1)
                  
    def speak(self, phrase: str):
        phrase = phrase.strip('"')
        self.info(f"Speech says: {phrase}")
        self.messages.append(f"{phrase}")
        self.speak_event.set()
