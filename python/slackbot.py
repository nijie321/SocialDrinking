import requests

def send_message(payload):
    # webhook url file
    webhook_url = ""
    with open('/home/pi/webhook_url', 'r') as f:
        webhook_url = f.read().strip()
    requests.post(webhook_url,json=payload)