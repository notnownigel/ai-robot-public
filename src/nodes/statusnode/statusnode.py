import subprocess
import time
from core.node import Node
from core import SystemStatus

class StatusNode(Node):
    def __init__(self):
        super().__init__(name=__name__)
    
    def start(self): 
        super().start()
        self.battery_percent = 100
        self.llm_status = ''
        self.node_event_channel.subscribe("ups-battery-percent", self.update_battery)
        self.node_event_channel.subscribe("llm-status", self.update_llm_status)
        self.run_every(10, self.monitor_status)
    
    def update_battery(self, percent:int):
        self.battery_percent = percent

    def update_llm_status(self, status:str):
        self.llm_status = status

    def monitor_status(self):
        under_voltage = self.get_under_voltage_status()
        ipaddr = self.get_ipaddr()
        disk_used, disk_total = self.get_disk_usage()
        memory_used, memory_total = self.get_memory_usage()
        cpu_temp = self.get_cpu_temp()
        cpu_load = self.get_cpu_load()

        if under_voltage:
            #Immediate alert when under-voltage
            self.error("Undervoltage detected")
            self.node_event_channel.publish("under-voltage-detected")
        
        status = SystemStatus(
            under_voltage = under_voltage,
            ipaddr = ipaddr,
            disk_space_used = disk_used,
            disk_space_total = disk_total,
            memory_used = memory_used,
            memory_total = memory_total,
            cpu_temp = cpu_temp,
            cpu_load = cpu_load,
            battery_percent = self.battery_percent,
            llm_status = self.llm_status
        )
    
        self.node_event_channel.publish("system-status", status)
    
    def get_under_voltage_status(self):
        s = subprocess.getoutput('vcgencmd get_throttled').rstrip('\n')
        return int(s.split("=")[1], 0) == 0x50005
    
    def get_ipaddr(self):
        s = subprocess.getoutput("hostname -I | cut -d\' \' -f1").rstrip('\n')
        return f"IP: {s}"
    
    def get_disk_usage(self):
        usage = subprocess.getoutput("df --total").split('\n').pop().split(' ')
        values = [v for v in usage if v != '']
        return (int(int(values[2])/1024), int(int(values[1])/1024))

    def get_memory_usage(self):
        usage = subprocess.getoutput("free -m").split('\n')[1].split(' ')
        values = [v for v in usage if v != '']
        return (int(values[2]),int(values[1]))
   
    def get_cpu_temp(self):
        s = subprocess.getoutput('vcgencmd measure_temp').split('=')
        values = [v for v in s if v != '']
        return float(values[1].rstrip("'C"))

    def get_cpu_stats(self):
        stat = subprocess.getoutput("cat /proc/stat").split('\n')[0].split(' ')
        values = [v for v in stat if v != '']
        del values[0]
        total = sum(int(x) for x in values)
        idle = int(values[3])
        return (total, idle)

    def get_cpu_load(self):
        (total_1, idle_1) = self.get_cpu_stats()
        time.sleep(1)
        (total_2, idle_2) = self.get_cpu_stats()

        total = int(total_2-total_1)
        idle = int(idle_2-idle_1)
        usage = int(total-idle)
        return int(float(usage * 100  / total))
