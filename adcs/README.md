# Mock ADCS Consumer Contract

A mock implementation of an ADCS (Automated Data Collection System) consumer contract for testing and demonstration purposes.

## Overview

This contract implements various data request and fulfillment functions for different data types:

- Uint256
- Bool
- Bytes32
- Bytes
- StringAndBool (for meme coin data)

## Compilation and Deployment

### Prerequisites

- Node.js v14+ and npm
- Hardhat or Foundry
- An Ethereum wallet with testnet/mainnet ETH
- ADCS Coordinator contract address

### Environment Setup

Create a `.env` file in the root directory:

```env
# Deployment
TESTNET_DEPLOYER=your_private_key_here
COORDINATOR_ADDRESS=adcs_coordinator_contract_address

# Network RPC URLs
ARBITRUM_PROVIDER=https://arb-mainnet.g.alchemy.com/v2/your_key
BASE_PROVIDER=https://base-mainnet.g.alchemy.com/v2/your_key

# Explorer API Keys
EXPLORER_API_KEY=your_explorer_api_key
ARBITRUM_API_KEY=your_arbiscan_api_key
BASE_API_KEY=your_basescan_api_key
```

### Supported Networks

- **Arbitrum**

  - ChainID: 42161
  - Explorer: https://arbiscan.io

  - Coordinator address: 0x07811b8B6151db734b8D1568918d3A62607879a7
- **Base**
  - ChainID: 8453
  - Explorer: https://basescan.org

  - Coordinator address: 0x91c5d6e9F50ec656e7094df9fC035924AAA428bb

### Using Hardhat

1. Install dependencies:

```bash
npm install
```

2. Create `.env` file:

```env
PRIVATE_KEY=your_wallet_private_key
RPC_URL=your_network_rpc_url
```

3. Compile the contract:

```bash
npx hardhat compile
```

4. Deploy:

```bash
npx hardhat run scripts/deploy.js --network <network_name>
```

### Using Foundry

1. Install dependencies:

```bash
forge install OpenZeppelin/openzeppelin-contracts
```

2. Compile:

```bash
forge build
```

3. Deploy:

```bash
forge create --rpc-url <your_rpc_url> \
    --private-key <your_private_key> \
    src/mock/MockADCSConsumer.sol:MockADCSConsumer \
    --constructor-args <coordinator_address>
```

### Verification

After deployment, verify your contract on Etherscan:

#### Hardhat:

```bash
npx hardhat verify --network <network_name> <contract_address> <coordinator_address>
```

#### Foundry:

```bash
forge verify-contract <contract_address> \
    src/mock/MockADCSConsumer.sol:MockADCSConsumer \
    --constructor-args $(cast abi-encode "constructor(address)" <coordinator_address>) \
    --chain <chain_id>
```

## Features

- Multiple data type support
- Event emission for request tracking
- OpenZeppelin's Ownable integration
- Gas-limit customization per request
- Flexible job ID configuration

## Contract Functions

### Request Functions

```solidity
function requestUint256Data(
    uint32 _callbackGasLimit,
    bytes32 _jobId,
    string memory _from,
    string memory _to
) external returns (uint256 requestId)

function requestBoolData(
    uint32 _callbackGasLimit,
    bytes32 _jobId,
    string memory _from
) external returns (uint256 requestId)

function requestBytes32Data(
    uint32 _callbackGasLimit,
    bytes32 _jobId,
    string memory _from
) external returns (uint256 requestId)

function requestMemeData(
    uint32 _callbackGasLimit,
    bytes32 _jobId
) external returns (uint256 requestId)

function requestBytesData(
    uint32 _callbackGasLimit,
    bytes32 _jobId,
    string memory _from
) external returns (uint256 requestId)
```

### State Variables

- `lastUint256`: Latest received uint256 value
- `lastBool`: Latest received boolean value
- `lastBytes32`: Latest received bytes32 value
- `lastBytes`: Latest received bytes value
- `lastestMemeCoin`: Latest received StringAndBool struct

### Events

```solidity
event DataRequestedUint256(uint256 indexed requestId)
event DataRequestedBool(uint256 indexed requestId)
event DataRequestedBytes32(uint256 indexed requestId)
event DataRequestedBytes(uint256 indexed requestId)
event DataRequestedStringAndBool(uint256 indexed requestId)
```

## Usage Example

```solidity
// Deploy contract
MockADCSConsumer consumer = new MockADCSConsumer(coordinatorAddress);

// Request uint256 data
uint256 requestId = consumer.requestUint256Data(
    200000,  // callback gas limit
    "0x1234....", // job ID
    "ETH",  // from
    "USD"   // to
);

// The result will be stored in lastUint256 after fulfillment
uint256 result = consumer.lastUint256();
```

## Inheritance

The contract inherits from:

- `ADCSConsumerFulfillUint256`
- `ADCSConsumerFulfillBool`
- `ADCSConsumerFulfillBytes32`
- `ADCSConsumerFulfillBytes`
- `ADCSConsumerFulfillStringAndBool`
- `Ownable`

## Dependencies

- OpenZeppelin Contracts v4.8.20
  - `IERC20`
  - `Ownable`
- ADCS Consumer Base Contract

## Security

- Only the contract owner can perform privileged operations
- Gas limits are customizable per request
- Uses OpenZeppelin's battle-tested contracts

## Events

All request functions emit events that can be used to track the request status:

- Request ID is indexed for efficient filtering
- Each data type has its own event for clear tracking
