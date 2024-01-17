import os
import subprocess
import json
import time
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


class CPU():
    def calc_delta(cpu_init, cpu_final):
        cpu_delta = []
        for core_i, core_f in zip(cpu_init, cpu_final):
            # [deltas.append(int(stat_f) - int(stat_i)) for stat_i in core_i[1:] for stat_f in core_f[1:]]
            deltas = []
            deltas.append(core_f[0]) # append core id (i.e., cpu1, cpu2)
            for stat_i, stat_f in zip(core_i[1:], core_f[1:]):
                deltas.append(int(stat_f) - int(stat_i))            
            cpu_delta.append(deltas)

        return cpu_delta

    def calc_utilization(cpu_delta, utilization):
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
        thermals = cmd = run_cmd('paste <(cat /sys/class/thermal/thermal_zone*/type) <(cat /sys/class/thermal/thermal_zone*/temp)')

        try:
            thermals = [thermal.split() for thermal in thermals.strip().split("\n")]
            thermals = {thermal[0]:int(thermal[1].strip()) for thermal in thermals}
        except:
            return {"error": cmd}

        return thermals
            

    def cpu():
        file_path = '/tmp/hardware_telemetry_last_cpu_util.json'
        results = run_cmd('cat /proc/stat | grep cpu').strip().split("\n")
        cpu_cur = [line.split() for line in results]

        if not os.path.exists(file_path):
            json.dump(cpu_cur, open(file_path, 'w'))
            return {"error": "no inital values found, please wait for next reading"}
        else:
            cpu_cur_time = time.time()
            # cpu_cur_time = os.path.getctime(file_path)
            cpu_last = json.load(open(file_path))
            cpu_last_time = os.path.getctime(file_path)

            json.dump(cpu_cur, open(file_path, 'w'))

            cpu_delta = CPU.calc_delta(cpu_last, cpu_cur)[1:]
            return CPU.calc_utilization(cpu_delta, {"delta_time_sec": cpu_cur_time - cpu_last_time})


    def cpu_accurate(utilization_delta_time_sec=1):
        # return run_cmd('cat /sys/devices/system/cpu/cpufreq/cpuload/cpu_usage')
        results = run_cmd(f'cat /proc/stat | grep cpu && sleep {utilization_delta_time_sec} && cat /proc/stat | grep cpu').strip().split("\n")
        results = [line.split() for line in results]

        cpu_init  = results[:len(results)//2][1:]
        cpu_final = results[len(results)//2:][1:]
        cpu_delta = CPU.calc_delta(cpu_init, cpu_final)
        return CPU.calc_utilization(cpu_delta, {"delta_time_sec": utilization_delta_time_sec})


    def network():
        # Speed & Ping
        print()


    def gpu():
        pass


    def sensors():
        pass