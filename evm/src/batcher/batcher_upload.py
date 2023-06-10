import json

def prepare_data_for_smart_contract(data):
    # Parse the JSON data
    parsed_data = json.loads(data)

    # Initialize the list of transactions
    transactions = []

    # Loop over the transactions in the data
    for tx in parsed_data["result"]["transactions"]:
        # Extract the transaction data
        from_address = tx["transaction"]["message"]["accountKeys"][0]
        to_address = tx["transaction"]["message"]["accountKeys"][1]
        gas_used = tx["meta"]["computeUnitsConsumed"]
        arguments = tx["transaction"]["message"]["instructions"][0]["data"]

        # Add the transaction to the list
        transactions.append((from_address, to_address, gas_used, arguments))

    # Return the list of transactions
    return transactions
