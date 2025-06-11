import os
import cv2
import logging
from threading import Thread, Event
from flask import Response, Flask, render_template, Markup, request
from core import Node, FPSMeter, SystemStatus, Shared, CameraCommand

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

webapp = Flask(__name__)
frame_to_render = None
frame_ready = Event()
fps = 0.0
current_status = SystemStatus(under_voltage=False, ipaddr="0.0.0.0", disk_space_used=0, disk_space_total=0, memory_used=0, memory_total=0, cpu_load=0, cpu_temp=0, battery_percent=100)

@webapp.route("/<name>")
def index(name):
    return render_template("index.html", name=name, title=os.getenv("DISPLAY_NAME"))

@webapp.route("/")
def home():
    return render_template("home.html", title=os.getenv("DISPLAY_NAME"))

@webapp.route("/video_feed")
def video_feed():
    return Response(generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")

@webapp.route('/status')
def getstatus():
    return {
        "fps": fps,
        "mode": "Manual" if Shared.manual_mode else "Automatic",
        "cpu_load": current_status.cpu_load,
        "cpu_temp": current_status.cpu_temp,
        "disk_space_used": current_status.disk_space_used,
        "disk_space_total": current_status.disk_space_total,
        "memory_used": current_status.memory_used,
        "memory_total": current_status.memory_total,
        "battery_percent": current_status.battery_percent
    }

@webapp.route('/nodes')
def getnodes():
    tbody = list()
    for node in Shared.nodes:
        tbody.append(f"<tr><td>{node.__class__.__name__}</td><td>{'&#10003;' if node.running else '&#x2717;'}</td><td>{node.last_message}</td><td>{node.last_error}</td></tr>") 
        
    return render_template("nodes.html", title=os.getenv("DISPLAY_NAME"), tbody=Markup("".join(tbody)))

@webapp.route("/shutdown")
def shutdown():
    Node.node_event_channel.publish("shutdown")
    return render_template("shutdown.html", title=os.getenv("DISPLAY_NAME"))

@webapp.route("/controller")
def controller():

    return render_template("controller.html", title=os.getenv("DISPLAY_NAME"), mode=int(Shared.manual_mode))

@webapp.route('/toggle-manual-mode', methods=['POST'])
def toggle_manual_mode():
    Shared.manual_mode = True if request.form.get("mode") == "1" else False
    return {}

#Only process movement when event threshold is met
drive_event_count = 0
drive_event_threshold = 15

@webapp.route('/drive-update', methods=['POST'])
def drive_update():
    global drive_event_count, drive_event_threshold
    if drive_event_count < drive_event_threshold:
        drive_event_count += 1
        return {}
    
    drive_event_count = 0

    match request.form.get("drive"):
        case 'north-west':
            Node.node_event_channel.publish("motor-translate-forward-left", Shared.SPEED_SLOW, 0.1)
        case 'north':
            Node.node_event_channel.publish("motor-forwards", Shared.SPEED_SLOW, 0.1)
        case 'north-east':
            Node.node_event_channel.publish("motor-translate-forward-right", Shared.SPEED_SLOW, 0.1)
        case 'west':
            Node.node_event_channel.publish("motor-pan-left", Shared.SPEED_SLOW, 0.1)
        case 'east':
            Node.node_event_channel.publish("motor-pan-right", Shared.SPEED_SLOW, 0.1)
        case 'south-west':
            Node.node_event_channel.publish("motor-translate-back-left", Shared.SPEED_SLOW, 0.1)
        case 'south':
            Node.node_event_channel.publish("motor-backwards", Shared.SPEED_SLOW, 0.1)
        case 'south-east':
            Node.node_event_channel.publish("motor-translate-back-right", Shared.SPEED_SLOW, 0.1)
        case 'turn-left':
            Node.node_event_channel.publish("motor-rotate-left", Shared.SPEED_SLOW, 0.1)
        case 'turn-right':
            Node.node_event_channel.publish("motor-rotate-right", Shared.SPEED_SLOW, 0.1)
        case 'up':
            Node.node_event_channel.publish("servo-command", CameraCommand(action=CameraCommand.CAMERA_RELATIVE, pos=(0, 2)))
        case 'down':
            Node.node_event_channel.publish("servo-command", CameraCommand(action=CameraCommand.CAMERA_RELATIVE, pos=(0, -2)))
        case 'left':
            Node.node_event_channel.publish("servo-command", CameraCommand(action=CameraCommand.CAMERA_RELATIVE, pos=(2, 0)))
        case 'right':
            Node.node_event_channel.publish("servo-command", CameraCommand(action=CameraCommand.CAMERA_RELATIVE, pos=(-2, 0)))
        case _:
            Node.node_event_channel.publish("motor-stop")

    return {}

def generate():
    while True:
        if frame_ready.wait(10):
            frame_ready.clear()
            yield(b'--frame\r\n' b'Content-Type: image/jpg\r\n\r\n' +  frame_to_render + b'\r\n')


class DisplayNode(Node):

    def __init__(self):
        super().__init__(name=__name__)
        self.fps = FPSMeter()
        Thread(target=self.run, daemon=True).start()
            
    def start(self): 
        super().start()
        self.fps.reset()
        self.node_event_channel.subscribe("display-node-frame", self.render)
        self.node_event_channel.subscribe("system-status", self.status_update)
    
    def stop(self):
        cv2.destroyAllWindows()
    
    def run(self):
        global webapp
        webapp.run(host= '0.0.0.0', port=int(os.getenv("DISPLAY_PORT")), debug=False, threaded=True) 
        
    def status_update(self, status):
        global current_status
        current_status = status

    def render(self, frame):
        global fps
        global frame_to_render
        global frame_ready
        self.fps.record()
        fps = self.fps.fps()
        frame_to_render = cv2.imencode(".jpg", cv2.resize(frame, (0,0), fx=0.8, fy=0.8))[1].tobytes()
        frame_ready.set()

                