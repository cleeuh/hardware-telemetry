import time
import json
import fetcher
import communications
import os


def main():
    url = os.environ.get("TELEMETRY_URL", "http://0.0.0.0:12000/api/telemetry")
    token = communications.generate_idempotent_token()

    # Use cron, dont use while loop
    # while(True):
    # time.sleep(0.25)
    results = {}
    results["cur_time"] = fetcher.Fetch.time()
    results["uptime"]   = fetcher.Fetch.uptime()
    results["mem"]      = fetcher.Fetch.memory()
    results["therm"]     =  fetcher.Fetch.temperature()
    results["cpu_util"] = fetcher.Fetch.cpu()
    # results["cpu_util"] = fetcher.Fetch.cpu(1)
    communications.publish(url, token=token, data=results)
    # print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()