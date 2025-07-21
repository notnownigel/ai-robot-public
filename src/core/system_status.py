from dataclasses import dataclass

@dataclass
class SystemStatus:
    under_voltage: bool
    ipaddr: str
    disk_space_used: int
    disk_space_total: int
    memory_used: int
    memory_total: int
    cpu_temp: float
    cpu_load: int
    battery_percent: int
    llm_status: str
