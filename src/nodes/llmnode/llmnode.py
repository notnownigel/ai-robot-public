import os
import time
from threading import Thread
from core import Node

class LLMNode(Node):
    def __init__(self):
        super().__init__(name=__name__)
    
    def start(self): 
        super().start()
        Thread(target=self.init, daemon=True).start()

    def init(self):
        self.node_event_channel.publish("llm-status", status = "Starting LLM Node")
        time.sleep(25)
        # TODO: Check Ollama running status
        self.error("LLM not available. Node terminated.")
        self.node_event_channel.publish("llm-status", status = self.last_error)
        self.stop()

