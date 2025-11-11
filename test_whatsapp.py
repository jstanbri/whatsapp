import requests
import os
from dotenv import load_dotenv

load_dotenv()


# Paste your credentials here
ACCESS_TOKEN = os.environ.get("USER_ACCESS_TOKEN") 
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")  
TO_PHONE = os.environ.get("RECIPIENT_PHONE_NUMBER")
VERSION = os.environ.get("VERSION")

url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "messaging_product": "whatsapp",
    "to": TO_PHONE,
    "type": "text",
    "text": {
        "body": "Hello! This is a test message from WhatsApp Cloud API 🚀 via Jamesy Python Code"
    }
}

print({ACCESS_TOKEN})
response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(response.json())