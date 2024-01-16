import requests
import uuid
import hashlib

def publish(url, token, data):
    data["token"] = token
    results = requests.post(url, json=data)
    return results

def generate_idempotent_token():
    system_uuid = str(uuid.getnode())  # Get the hardware address as a 48-bit positive integer
    token = uuid.uuid5(uuid.NAMESPACE_DNS, system_uuid)  # Generate a UUID based on DNS and the hardware address
    return str(token)