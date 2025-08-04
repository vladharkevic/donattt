
import requests, time, json, os
from .config import MONOBANK_TOKEN

TXN_LOG = 'used_txns.json'

def get_transactions():
    url = 'https://api.monobank.ua/personal/statement/0/' + str(int(time.time()))
    headers = {'X-Token': MONOBANK_TOKEN}
    r = requests.get(url, headers=headers)
    return r.json() if r.status_code == 200 else []

def load_used_txns():
    if not os.path.exists(TXN_LOG): open(TXN_LOG, 'w').write('[]')
    with open(TXN_LOG) as f: return json.load(f)

def save_used_txn(txn_id):
    used = load_used_txns()
    used.append(txn_id)
    with open(TXN_LOG, 'w') as f: json.dump(used, f)

def find_payment(amount_uah):
    txns = get_transactions()
    used = load_used_txns()
    now = int(time.time())

    for txn in reversed(txns):
        if txn['operationAmount'] < 0:
            value = abs(txn['operationAmount']) / 100
            if abs(value - amount_uah) < 0.1 and now - txn['time'] < 300 and txn['id'] not in used:
                save_used_txn(txn['id'])
                return True
    return False
