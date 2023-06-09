# ethprague_hack
solana VM L3 built using op-stack on top of mantle

## "bridge"
set of 2 smart contracts that create a bridge - lock erc20 on L2 unlocks SPL20 for any address
- take the evm counterpart from op-stack

- basic setup:
    BRIDGE_OPERATOR = address_on_mantle
    BRIDGE_OPERATOR = address_on_svm

user on mantle bridging to svm:
    - deposit_onto_svm(token, amount, svm_address) // transfer erc20 into the contract (check for fee on transfer tokens)
        - calls _initiateDeposit()
        - emits event deposit_logged(token, amount, svm_address, deposit_address)
        - locker logs deposit event

        - BRIDGE_OPERATOR mints those tokens on SVM and sends them to the deposit address
            - done through MintAndSend of the bridge contract

user on svm bridging back:
    - withdraw_onto_evm(token, amount, evm_address) // transfer the minted spl into the contract
        - emits event withdrawal_logged(token, amount, evm_address, deposit_address)
        


### locker on SVM


### locker on the L2

## batcher/sequencer
- first create proof of concept in solidity

- takes: solana block, parses transactions and pushes them into a mapping.

1. monitor.py continously pulling all txs from solana blocks and storing them into "some data structure"

2. batchsend.py - once in a while (how often?), this gets pushed into a smart contract onto an L2 with cheap calldata - mantle

3. batcher - contract that accepts appends into a mapping from a whitelisted address



data structure something like:
- transactions[block_1, block_2 ... block_n], where block_n is:
    - block_n[tx1, tx2...tx_n]
        - tx_n[from, to, gas, arguments...]

-> look at how optimism is doing it and do the same

- then optimise using solady

### batcher
pushes SVM tx from L3 onto L2 - using libzip bytearrays



__________

### test performance
- max out tps on the local machine to get


### todos after hackathon
- contract on L1 Goerli that automates deposit into the SVM directly

- get error handling and proper production-ready setup, including dependancies and fail errors + tests
- perform min max theroetical testing - with blobs, with/without celestia etc.
- validity proofs / some zk hack to prove txs were published correctly (validity proofs at first, then zk proof ideally)
    - the blocks of sealevel are public, what's uploaded public too, should be possible to have literally anyone compare and dispute those two

- role to decentralisation - decentralise the sealevel node set (reasonably, not overly so tho to keep perf), 
- while making sure there is still zk proof of this correct txs upload