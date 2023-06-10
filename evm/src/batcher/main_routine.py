import asyncio
import json
import requests
from web3 import Web3, HTTPProvider
from web3.exceptions import TransactionNotFound

# Your contract and account details
private_key = "<Ethereum Private Key>"
contract_address = "<Contract Address>"
contract_abi = <Contract ABI>  # This should be the actual contract ABI
chain_id = 1

# Connection to Ethereum node
web3 = Web3(HTTPProvider('http://localhost:8545'))  # replace with your node address

# Get the contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def prepare_data_for_smart_contract(data):
    parsed_data = json.loads(data)
    transactions = []
    for tx in parsed_data["result"]["transactions"]:
        from_address = tx["transaction"]["message"]["accountKeys"][0]
        to_address = tx["transaction"]["message"]["accountKeys"][1]
        gas_used = tx["meta"]["computeUnitsConsumed"]
        arguments = bytes(tx["transaction"]["message"]["instructions"][0]["data"], 'utf-8')

        transactions.append((from_address, to_address, gas_used, arguments))

    return transactions

async def add_transactions_to_smart_contract(transactions):
    try:
        # Create and sign the transaction
        nonce = web3.eth.getTransactionCount(web3.eth.defaultAccount)
        gas_price = web3.toWei('1', 'gwei')

        txn_dict = {
            'chainId': chain_id,  # replace with actual chain ID
            'gasPrice': gas_price,
            'nonce': nonce,
        }

        # Estimate gas
        gas_estimate = contract.functions.addTransactions(0, transactions).estimateGas(txn_dict)

        # Build the transaction with the estimated gas
        txn = contract.functions.addTransactions(0, transactions).buildTransaction({
            **txn_dict,
            'gas': gas_estimate,
        })

        signed_txn = web3.eth.account.signTransaction(txn, private_key)

        # Send the transaction
        txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

        # Wait for the transaction to be mined, and get the transaction receipt
        txn_receipt = web3.eth.waitForTransactionReceipt(txn_hash)

        print(f"Transaction successful with hash: {txn_hash.hex()}")
    except TransactionNotFound:
        print("Transaction was not found, check your transaction data and try again.")
    except Exception as e:
        print(f"An unexpected error occurred when sending the transaction: {e}")

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

async def monitor_transactions():
    current_slot = get_last_finalized_slot()

    while True:
        try:
            while get_last_finalized_slot() <= current_slot:
                transactions = get_slot_transactions(current_slot)
                
            current_slot += 1

            if transactions:
                prepared_transactions = prepare_data_for_smart_contract(json.dumps({"result": {"transactions": transactions}}))
                await add_transactions_to_smart_contract(prepared_transactions)

            await asyncio.sleep(1)  # Sleep for a while before checking for new transactions
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while requesting data from the Solana node: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# Run the monitor_transactions function in the event loop
asyncio.run(monitor_transactions())
