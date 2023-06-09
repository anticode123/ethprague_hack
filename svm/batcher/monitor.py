import requests
import json
import time

def get_slot_transactions(slot):
    url = "http://127.0.01:8899"
    headers = {"Content-Type": "application/json"}

    # Construct the request body for the 'getConfirmedBlock' method
    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getConfirmedBlock",
        "params": [slot]
    }

    # Send the request to the Solana node
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check if there's an error
    if 'error' in response.json():
        return []

    # Parse the response
    transactions = response.json()['result']['transactions']

    return transactions

def get_last_finalized_slot():
    url = "http://127.0.01:8899"
    headers = {"Content-Type": "application/json"}

    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getEpochInfo",
    }

    # Send the request to the Solana node
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Parse the response
    last_finalized_slot = response.json()['result']['absoluteSlot']

    return last_finalized_slot

def store_transactions(transactions):
    # Implement your own logic here to store transactions
    # It could be storing in a database, writing to a file, etc.
    for tx in transactions:
        print(tx)

def monitor_transactions():
    current_slot = get_last_finalized_slot()

    while True:
        while get_last_finalized_slot() <= current_slot:
            transactions = get_slot_transactions(current_slot)
            
        current_slot += 1

        if transactions:
            store_transactions(transactions)

# Start the monitoring
monitor_transactions()