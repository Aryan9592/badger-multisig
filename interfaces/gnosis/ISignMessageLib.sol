// SPDX-License-Identifier: UNLICENSED
// !! THIS FILE WAS AUTOGENERATED BY abi-to-sol v0.5.3. SEE SOURCE BELOW. !!
pragma solidity ^0.7.0;

import "./IGnosisSafe_v1_3_0.sol";

interface ISignMessageLib is IGnosisSafe_v1_3_0 {
    function getMessageHash(bytes memory message)
        external
        view
        returns (bytes32);

    function signMessage(bytes memory _data) external;
}

// THIS FILE WAS AUTOGENERATED FROM THE FOLLOWING ABI JSON:
/*
[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"msgHash","type":"bytes32"}],"name":"SignMsg","type":"event"},{"inputs":[{"internalType":"bytes","name":"message","type":"bytes"}],"name":"getMessageHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"signMessage","outputs":[],"stateMutability":"nonpayable","type":"function"}]
*/