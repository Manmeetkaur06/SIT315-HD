// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ImageLog {
    struct Entry {
        string imageHash;
        uint256 timestamp;
    }
    Entry[] public logs;

    function logImage(string memory imageHash) public {
        logs.push(Entry(imageHash, block.timestamp));
    }

    function getLog(uint256 idx) public view returns (string memory, uint256) {
        Entry memory e = logs[idx];
        return (e.imageHash, e.timestamp);
    }

    function getLogCount() public view returns (uint256) {
        return logs.length;
    }
}
