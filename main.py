import time
import fetcher

def main():
    # while(True):
    results = ""
    results += fetcher.Fetch.time()
    results += fetcher.Fetch.uptime()
    results += fetcher.Fetch.memory()
    results += fetcher.Fetch.temperature()
    results += fetcher.Fetch.cpu()
    print(results)
    time.sleep(0.25)


if __name__ == "__main__":
    main()