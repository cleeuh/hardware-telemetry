import requests

def publish(url, data):
    results = requests.post(url, json=data)
    return results

