// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

/**
 * @title PeriodicHashUpdater
 * @dev A contract that updates the hash of a provided JSON-like structure every 10 seconds.
 */
contract PeriodicHashUpdater {
    /// @notice Stores the hash of the data structure.
    bytes32 public currentHash;

    /// @notice Stores the timestamp of the last update.
    uint256 public lastUpdateTime;

    /// @notice Minimum time interval (in seconds) between updates.
    uint256 public constant UPDATE_INTERVAL = 10 seconds;

    /**
     * @dev Event emitted when the hash is updated.
     * @param newHash The new hash after the update.
     * @param timestamp The time when the update occurred.
     */
    event HashUpdated(bytes32 indexed newHash, uint256 timestamp);

    /**
     * @dev Constructor to initialize the contract with an initial hash.
     * @param initialData The initial data to hash and store.
     */
    constructor(bytes memory initialData) {
        currentHash = keccak256(initialData);
        lastUpdateTime = block.timestamp;
        emit HashUpdated(currentHash, lastUpdateTime);
    }

    /**
     * @notice Updates the stored hash if the minimum time interval has passed.
     * @param newData The new data to hash and store.
     * @dev Reverts if called before the `UPDATE_INTERVAL` has passed.
     */
    function updateHash(bytes memory newData) external {
        require(block.timestamp >= lastUpdateTime + UPDATE_INTERVAL, "Update interval has not passed.");
        currentHash = keccak256(newData);
        lastUpdateTime = block.timestamp;
    
        emit HashUpdated(currentHash, lastUpdateTime);
    }

    /**
     * @notice Checks if the hash can be updated based on the time interval.
     * @return True if the hash can be updated, false otherwise.
     */
    function canUpdate() external view returns (bool) {
        return block.timestamp >= lastUpdateTime + UPDATE_INTERVAL;
    }
}
