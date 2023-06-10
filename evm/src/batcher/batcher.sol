// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

contract TransactionsBatch {
    // Define a custom transaction type
    struct Transaction {
        address from;
        address to;
        uint computeUnitsConsumed;
        bytes data;
    }

    // Define a custom block type
    struct Block {
        Transaction[] transactions;
    }

    // Define an array to hold all blocks
    Block[] internal blocks;

    // Batch add transactions to a block
    function addTransactions(uint _blockIndex, Transaction[] memory _transactions) public {
        // Ensure only the contract owner can add transactions
        require(msg.sender == owner, "Only contract owner can add transactions");

        // Ensure the block index is valid
        require(_blockIndex < blocks.length, "Invalid block index");

        // Add all transactions to the block
        for (uint i = 0; i < _transactions.length; i++) {
            blocks[_blockIndex].transactions.push(_transactions[i]);
        }
    }

    // Batch add new blocks
    function addBlocks(uint _numBlocks) public {
        // Ensure only the contract owner can add blocks
        require(msg.sender == owner, "Only contract owner can add blocks");

        // Add new blocks
        for (uint i = 0; i < _numBlocks; i++) {
            Block memory newBlock;
            blocks.push(newBlock);
        }
    }

    // Get a transaction from a block
    function getTransaction(uint _blockIndex, uint _transactionIndex) public view returns (address, address, uint, bytes memory) {
        // Ensure the block index is valid
        require(_blockIndex < blocks.length, "Invalid block index");

        // Ensure the transaction index is valid
        require(_transactionIndex < blocks[_blockIndex].transactions.length, "Invalid transaction index");

        // Retrieve the transaction
        Transaction memory transaction = blocks[_blockIndex].transactions[_transactionIndex];

        return (transaction.from, transaction.to, transaction.computeUnitsConsumed, transaction.data);
    }

    address private owner;

    // Ensure only contract owner can deploy the contract
    constructor() {
        owner = msg.sender;
    }
}
