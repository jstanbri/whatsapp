import requests

# Paste your credentials here
ACCESS_TOKEN = "EAAKIcdZASr8oBP8NTyTQBv4ZCE6OALtodqEWFVNxEzGobzujSoBGRgbZAmQMZBjTIlm0XYL9HX8ZAmgg02VWObarT31cZCSpxgupNaZAXB3IlcHS7EYEXg8nQMLqRCwasYy98a96m1iGihIO25Aj8yrlm5V1QbmIPhjOgwy5svdVx0cbf5tOzZCgDV4i5QHj5DZBG5k6WEkjMB6kJwPZCabQTWPpLHDBTNgQye4ZAOUAoz5zViJyFG1xZCQL14CSYt1Ma1V03FGjjiotFnQ6y6w3cQMZCmQc28mG4ndMk2dL1i2AZD"  # From Step 1
PHONE_NUMBER_ID = "856886180841184"  # From Step 2
TO_PHONE = "447496727058"  # YOUR phone number (with country code, no + or spaces)

url = f"https://graph.facebook.com/v24.0/{PHONE_NUMBER_ID}/messages"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "messaging_product": "whatsapp",
    "to": TO_PHONE,
    "type": "text",
    "text": {
        "body": "Hello! This is a test message from WhatsApp Cloud API 🚀"
    }
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(response.json())