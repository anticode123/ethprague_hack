from web3 import Web3, HTTPProvider
import json



# Function to prepare data
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

# Connection to Ethereum node
web3 = Web3(HTTPProvider('http://localhost:8545'))  # replace with your node address

# Your Ethereum account private key
private_key = "<Ethereum Private Key>"

# Contract details
contract_address = "<Contract Address>"
contract_abi = <Contract ABI>  # This should be the actual contract ABI

# Get the contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Your data
data = "<Your JSON Data>"

# Prepare the data for the smart contract
transactions = prepare_data_for_smart_contract(data)

# Create and sign the transaction
nonce = web3.eth.getTransactionCount(web3.eth.defaultAccount)
txn = contract.functions.addTransactions(0, transactions).buildTransaction({
    'chainId': 1,  # replace with actual chain ID
    'gas': 70000,  # replace with estimated gas
    'gasPrice': web3.toWei('1', 'gwei'),
    'nonce': nonce,
})

signed_txn = web3.eth.account.signTransaction(txn, private_key)

# Send the transaction
txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

# Wait for the transaction to be mined, and get the transaction receipt
txn_receipt = web3.eth.waitForTransactionReceipt(txn_hash)

print(f"Transaction successful with hash: {txn_hash.hex()}")
