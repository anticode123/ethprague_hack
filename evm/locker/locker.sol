// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import { IERC20 } from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import { SafeERC20 } from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

contract Locker {
    using SafeERC20 for IERC20;

    address public BRIDGE_OPERATOR;

    constructor(address bridge_operator) {
        BRIDGE_OPERATOR = bridge_operator;
    }

    event ERC20DepositInitiated(
        address indexed _evmtoken,
        uint256 _amount,
        address indexed _from,
        bytes32 indexed _to
    );

    function depositERC20( // need to make sure mapping evmtoken - svmtoken is unique, same applies on the other side, minting gets handled on other chain side
        address _evmtoken,
        uint256 _amount,
        bytes32 _to // _to is a svm address
    ) external virtual {
        _initiateERC20Deposit(_evmtoken, _amount, msg.sender, _to);
    }   
    function _initiateERC20Deposit(address _evmtoken, uint256 _amount,address _from, bytes32 _to) internal {

        IERC20(_evmtoken).safeTransferFrom(_from, address(this), _amount);

        emit ERC20DepositInitiated(_evmtoken, _amount, msg.sender, _to);
    }
}