import os
import subprocess
from datetime import datetime

def run_cmd(cmd):
    # command = f"iperf3 -c {cmd} --json"
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stderr:
        return result.stderr
    else:
        return result.stdout

def read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except:
        return "non-specific error"

class Fetch():
    def time():
        return f"{datetime.now().strftime('%H:%M:%S')}\n"
    def uptime():
        # return run_cmd('cat /proc/uptime')
        return run_cmd('uptime')
    def memory():
        return run_cmd('cat /proc/meminfo')
    def temperature():
        return run_cmd("paste <(cat /sys/class/thermal/thermal_zone*/type) <(cat /sys/class/thermal/thermal_zone*/temp)")
    def cpu():
        return run_cmd('cat /sys/devices/system/cpu/cpufreq/cpuload/cpu_usage')
    def network():
        # Speed & Ping
        print()
    def gpu():
        pass
    def sensors():
        pass