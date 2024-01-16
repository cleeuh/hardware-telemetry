import os
import subprocess
from datetime import datetime

def run_cmd(cmd):
    # command = f"iperf3 -c {cmd} --json"
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, executable='/bin/bash', stderr=subprocess.PIPE)
    if result.stderr:
        return result.stderr.decode('utf-8')
    else:
        return result.stdout.decode('utf-8')

def read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except:
        return "non-specific error"


class Fetch():
    def time():
        return f"{datetime.now().strftime('%H:%M:%S')}"


    def uptime():
        # return run_cmd('cat /proc/uptime')
        return run_cmd('uptime').strip()


    def memory():
        mems = cmd = run_cmd('cat /proc/meminfo')
        try:
            mems = [mem.split(":") for mem in mems.strip().split("\n")]
            mems = {mem[0]:mem[1].strip() for mem in mems}
        except:
            return {"error": cmd}

        return mems


    def temperature():
        temps = cmd = run_cmd('paste <(cat /sys/class/thermal/thermal_zone*/type) <(cat /sys/class/thermal/thermal_zone*/temp)')

        try:
            temps = [temp.split() for temp in temps.strip().split("\n")]
            temps = {temp[0]:temp[1].strip() for temp in temps}
        except:
            return {"error": cmd}

        return mems
            


    def cpu(utilization_delta_time_sec):
        # return run_cmd('cat /sys/devices/system/cpu/cpufreq/cpuload/cpu_usage')
        results = run_cmd(f'cat /proc/stat | grep cpu && sleep {utilization_delta_time_sec} && cat /proc/stat | grep cpu').strip().split("\n")

        results = [line.split() for line in results]

        cpu_init  = results[:len(results)//2][1:]
        cpu_final = results[len(results)//2:][1:]
        cpu_delta = []

        for core_i, core_f in zip(cpu_init, cpu_final):
            # [deltas.append(int(stat_f) - int(stat_i)) for stat_i in core_i[1:] for stat_f in core_f[1:]]
            deltas = []
            deltas.append(core_f[0]) # append core id (i.e., cpu1, cpu2)
            for stat_i, stat_f in zip(core_i[1:], core_f[1:]):
                deltas.append(int(stat_f) - int(stat_i))            
            cpu_delta.append(deltas)

        # deltas = [int(stat_f) - int(stat_i) for core_i, core_f in zip(cpu_init, cpu_final) for stat_i, stat_f in zip(core_i[1:], core_f[1:])]
        # n = 10
        # deltas = [deltas[i:i + n] for i in range (0, len(deltas), n)]
        # print(deltas)

        utilization = {"timing_sec": utilization_delta_time_sec}

        for cpu_stats in cpu_delta:
            core_id = cpu_stats[0]
            cpu_stats[0] = cpu_stats[0].replace("cpu", "")
            cpu_stats = [int(stat) for stat in cpu_stats]
            cpu_total = sum(cpu_stats[1:])
            cpu_idle = cpu_stats[4]
            utilization[core_id] = (1-(cpu_idle/cpu_total)) * 100 if cpu_total != 0 else 0
            # user        = cpu_stat[1]
            # nice        = cpu_stat[2]
            # system      = cpu_stat[3]
            # idle        = cpu_stat[4]
            # iowait      = cpu_stat[5]
            # irq         = cpu_stat[6]
            # softirq     = cpu_stat[7]
            # steal       = cpu_stat[8]
            # guest       = cpu_stat[9]
            # guest_nice  = cpu_stat[10]
            
        return utilization
    def network():
        # Speed & Ping
        print()
    def gpu():
        pass
    def sensors():
        pass