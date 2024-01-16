import time
import json
import fetcher
import communications

def main():
    token = communications.generate_idempotent_token()
    while(True):
        results = {}
        results["cur_time"] = fetcher.Fetch.time()
        results["uptime"]   = fetcher.Fetch.uptime()
        results["mem"]      = fetcher.Fetch.memory()
        results["therm"]     =  fetcher.Fetch.temperature()
        results["cpu_util"] = fetcher.Fetch.cpu(1)
        print(json.dumps(results, indent=2))
        communications.publish("http://0.0.0.0:12000/api/telemetry", token=token, data=results)
        time.sleep(0.25)


if __name__ == "__main__":
    main()