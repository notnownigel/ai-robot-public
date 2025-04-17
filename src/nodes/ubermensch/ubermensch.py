import os
import signal
from core import Shared
from core.node import Node

class Ubermensch(Node):
    
    def __init__(self, *args):
        super().__init__(name=__name__)

        signal.signal(signal.SIGTSTP, self.signal_handler)
        self.node_event_channel.subscribe("under-voltage-detected", self.stop)
        self.node_event_channel.subscribe("shutdown", self.stop)

        if args is not None:
            for node in args:
                Shared.nodes.append(node)
                node.start()

        signal.pause()

    def stop(self):
        self.warning(f"Shutting Down...")        
        super().stop()
        for node in Shared.nodes:
            node.stop()

        os.kill(os.getpid(), signal.SIGUSR1)
        
    def signal_handler(self, sig, _):
        signal.signal(sig, signal.SIG_IGN) # ignore additional signals
        self.stop()
