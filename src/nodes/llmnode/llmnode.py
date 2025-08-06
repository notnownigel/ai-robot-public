import os
import subprocess
import time
import random
import ollama
from threading import Thread
from core import Node, Person

class LLMNode(Node):
    def __init__(self):
        super().__init__(name=__name__)
    
    def start(self): 
        super().start()
        Thread(target=self.init, daemon=True).start()

    def init(self):
        self.node_event_channel.publish("llm-status", status = "Starting LLM Node")

        ver = self.check_version()
        
        if ver == '':
            self.error("LLM not available. Node terminated.")
            self.node_event_channel.publish("llm-status", status = self.last_error)
            self.stop()
        
        self.node_event_channel.publish("llm-status", status = ver)
        self.model = os.getenv("LLM_MODEL")
        self.start_ollama()
        self.node_event_channel.subscribe("llm-generate-greeting", self.greet)

    def check_version(self):
        s = subprocess.getoutput('ollama --version')
        if 'ollama: not found' in s:
            return ""
        
        return s

    def start_ollama(self):
        subprocess.getoutput('ollama start')
        
    def greet(self, person: Person):
        sentiments = os.getenv(f"LLM_SENTIMENT_{person.person_score}").split(':') 
        sentiment = sentiments[random.randint(0, len(sentiments)-1)]
        prompt = f"I'm {person.name}. Greet me using a brief {sentiment} response"
        response = ollama.generate(self.model, prompt=prompt)
        self.node_event_channel.publish("speech-node-speak", response['response'])


