import os
import time
from threading import Thread
from core.node import Node
from core import SystemStatus

class StatusNode(Node):
    def __init__(self):
        super().__init__(name=__name__)
    
    def start(self): 
        super().start()
        self.battery_percent = 100
        self.node_event_channel.subscribe("ups-battery-percent", self.update_battery)
        self.run_every(10, self.monitor_status)
    
    def update_battery(self, percent:int):
        self.battery_percent = percent

    def monitor_status(self):
        disk_used, disk_total = self.get_disk_usage()
        memory_used, memory_total = self.get_memory_usage()
        under_voltage = self.get_under_voltage_status()
        
        if under_voltage:
            #Immediate alert when under-voltage
            self.error("Undervoltage detected")
            self.node_event_channel.publish("under-voltage-detected")
            
        status = SystemStatus(
            under_voltage = under_voltage,
            ipaddr = self.get_ipaddr(),
            disk_space_used = disk_used,
            disk_space_total = disk_total,
            memory_used = memory_used,
            memory_total = memory_total,
            cpu_temp = self.get_cpu_temp(),
            cpu_load = self.get_cpu_load(),
            battery_percent = self.battery_percent
        )
        
        self.node_event_channel.publish("system-status", status)

    def get_ipaddr(self):
        cmd = "hostname -I | cut -d\' \' -f1"
        s = os.popen(cmd).readline().rstrip('\n')
        return f"IP: {s}"
    
    def get_disk_usage(self):
        cmd = "df --total"
        usage = os.popen(cmd).readlines().pop().split(' ')
        values = [v for v in usage if v != '']
        return (int(int(values[2])/1024), int(int(values[1])/1024))

    def get_memory_usage(self):
        cmd = "free -m"
        usage = os.popen(cmd).readlines()[1].split(' ')
        values = [v for v in usage if v != '']
        return (int(values[2]),int(values[1]))
   
    def get_cpu_temp(self):
        s = os.popen('vcgencmd measure_temp').readline().rstrip("'C\n")
        return float(s.split("=")[1])

    def get_under_voltage_status(self):
        s = os.popen('vcgencmd get_throttled').readline().rstrip('\n')
        return int(s.split("=")[1], 0) == 0x50005
    
    def get_cpu_load(self):
        f1 = os.popen("cat /proc/stat", 'r')
        stat1 = f1.readline()
        count = 10
        data_1 = []
        for i  in range (count):
            data_1.append(int(stat1.split(' ')[i+2]))
        total_1 = data_1[0]+data_1[1]+data_1[2]+data_1[3]+data_1[4]+data_1[5]+data_1[6]+data_1[7]+data_1[8]+data_1[9]
        idle_1 = data_1[3]

        time.sleep(1)

        f2 = os.popen("cat /proc/stat", 'r')
        stat2 = f2.readline()
        data_2 = []
        for i  in range (count):
            data_2.append(int(stat2.split(' ')[i+2]))
        total_2 = data_2[0]+data_2[1]+data_2[2]+data_2[3]+data_2[4]+data_2[5]+data_2[6]+data_2[7]+data_2[8]+data_2[9]
        idle_2 = data_2[3]

        total = int(total_2-total_1)
        idle = int(idle_2-idle_1)
        usage = int(total-idle)
        return int(float(usage * 100  / total))
