
import requests
from .config import MERCHANT_TOKEN, REDIRECT_URL

def create_invoice(nickname, amount):
    url = "https://api.monobank.ua/api/merchant/invoice/create"
    headers = {"X-Token": MERCHANT_TOKEN, "Content-Type": "application/json"}
    payload = {
        "amount": amount * 100,
        "ccy": 980,
        "redirectUrl": REDIRECT_URL,
        "merchantPaymInfo": {
            "reference": f"donate_{nickname}_{amount}",
            "destination": f"Донат на сервер: {nickname}, {amount} грн"
        }
    }
    r = requests.post(url, headers=headers, json=payload)
    return r.json()['pageUrl'] if r.status_code == 200 else None
