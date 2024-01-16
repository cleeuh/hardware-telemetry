import time
import json
import fetcher

def main():
    while(True):
        results = {}
        results["cur_time"] = fetcher.Fetch.time()
        results["uptime"]   = fetcher.Fetch.uptime()
        results["mem"]      = fetcher.Fetch.memory()
        results["therm"]     =  fetcher.Fetch.temperature()
        results["cpu_util"] = fetcher.Fetch.cpu(1)
        print(json.dumps(results, indent=2))
        time.sleep(0.25)


if __name__ == "__main__":
    main()