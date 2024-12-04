# Rivalz SDK & ADCS Contracts

This repository contains the official SDK wrappers and smart contracts for the Rivalz platform.

## Repository Structure

```
.
├── ocy/                    # SDK Implementations
│   ├── nodejs/            # Node.js/TypeScript SDK
│   │   ├── RivalzClient.ts
│   │   └── README.md
│   └── python/            # Python SDK
│       ├── rivalz_client.py
│       └── README.md
├── adcs/                  # Smart Contracts
│   ├── contracts/        # ADCS Consumer Contracts
│   └── README.md
└── documents/            # Example Documents
```

## Components

### 1. SDK Wrappers (ocy/)

#### Node.js/TypeScript SDK

- Type-safe wrapper for Rivalz client
- File size validation
- Async/await support
- Complete TypeScript typings
- File size limit: 10MB

Features:

- File upload/download management
- Knowledge base operations
- Chat session handling
- Document history tracking

#### Python SDK

- Python 3.7+ support
- Async/await implementation
- Type hints for better IDE support
- Similar feature set to Node.js SDK

### 2. ADCS Contracts (adcs/)

Smart contracts for the Automated Data Collection System:

- Mock ADCS Consumer implementation
- Multiple data type support
- Event emission for request tracking
- OpenZeppelin integration

Supported Networks:

- Arbitrum (Chain ID: 42161)
- Base (Chain ID: 8453)

## Quick Start

### Using the Node.js SDK

```typescript
import { RivalzClientSdk } from "./ocy/nodejs/RivalzClient";
import * as dotenv from "dotenv";

dotenv.config();

const client = new RivalzClientSdk(process.env.RIVALZ_SECRET_TOKEN);

// Upload a file
const result = await client.uploadFile("path/to/file.pdf", "document.pdf");
console.log(result.ipfs_hash);
```

### Using the Python SDK

```python
from rivalz_client_sdk import RivalzClientSdk
from dotenv import load_dotenv
import os

load_dotenv()

client = RivalzClientSdk(os.getenv("RIVALZ_SECRET_TOKEN"))

# Upload a file
result = await client.upload_file("path/to/file.pdf", "document.pdf")
print(result["ipfs_hash"])
```

### Deploying ADCS Contracts

```bash
# Using Hardhat
npx hardhat run scripts/deploy.js --network <network_name>

# Using Foundry
forge create --rpc-url <your_rpc_url> \
    --private-key <your_private_key> \
    src/mock/MockADCSConsumer.sol:MockADCSConsumer \
    --constructor-args <coordinator_address>
```

## Environment Setup

Create a `.env` file in the root directory:

```env
# SDK Configuration
RIVALZ_SECRET_TOKEN=your_secret_token_here

# Contract Deployment
TESTNET_DEPLOYER=your_private_key
COORDINATOR_ADDRESS=adcs_coordinator_address

# Network RPC URLs
ARBITRUM_PROVIDER=https://arb-mainnet.g.alchemy.com/v2/your-key
BASE_PROVIDER=https://base-mainnet.g.alchemy.com/v2/your-key

# Explorer API Keys
EXPLORER_API_KEY=your_explorer_api_key
ARBITRUM_API_KEY=your_arbiscan_api_key
BASE_API_KEY=your_basescan_api_key
```

## Documentation

- [Node.js SDK Documentation](./ocy/nodejs/README.md)
- [Python SDK Documentation](./ocy/python/README.md)
- [ADCS Contracts Documentation](./adcs/README.md)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see the [LICENSE](LICENSE) file for details
