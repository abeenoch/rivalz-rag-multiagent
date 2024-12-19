


RIVALZ-HACKATHON-MULTIAGENT
Multi-Agent RAG System.
Overview
This project demonstrates a multi-agent Retrieval-Augmented Generation (RAG) system, built and submitted as my participation of the RIVALS AI world hackathon.

The system leverages a RAG pipeline and three agents to handle tasks like:

Responding to to queries regarding Rivalz and other block chain related topics.
Querying and monitoring DeFi protocols.
Discuss staking and other onchain activities.
Give financial advice based on data received from various API's dynamically.
Features
Multi-Agent System: Uses three agents to handle various tasks like TVL monitoring.
Real-Time TVL Fetching: Fetches TVL data across multiple chains using the DeFiLlama API.
Real-Time Coin price Fetching: Fetched coin prices accross multiple chains using coingecko API.
Real-Time Internet Search: Search the internet in real time for information using duckduckgo API.
Customizable: Agents can be tailored for specific DeFi protocols and workflows.
Error Handling: Includes retries and logging for better fault tolerance.
*RAG-Pipeline: For more accurate responses, used RIVALZ for vector storage.
API: Used FASTAPI for building the backend API that handles requests and serves data.
#TOOLS

OPENAI SWARM: For multiagent orchestration.
RIVALZ CLIENT: For knowledge base creation vector storage and retrival.
DUCKDUCKGO: Used this for internet search.
FASTAPI: Used this for backend.# Rivalz SDK & ADCS Contracts

This repository contains the official SDK wrappers and smart contracts for the Rivalz platform.


## Contributing-Running-server-swagger-docs
1. python -m venv env
2. pip install -r requirements.txt

3. Create a `.env` file:

```env
RIVALZ_SECRET_TOKEN=your_secret_token_here
```
4. uvicorn ocy.main:app --reload


# Rivalz SDK Python Wrapper

Simple Python wrapper for the Rivalz SDK with async/await support and file size validation.

## Setup

1. Install dependencies:

```bash
pip install rivalz-client python-dotenv
```

2. Create a `.env` file:

```env
RIVALZ_SECRET_TOKEN=your_secret_token_here
```

## Usage

```python
import asyncio
from rivalz_client_sdk import RivalzClientSdk
from dotenv import load_dotenv
import os

load_dotenv()

async def example():
    client = RivalzClientSdk(os.getenv("RIVALZ_SECRET_TOKEN"))

    # Upload a file
    result = await client.upload_file("path/to/file.pdf", "document.pdf")
    print(result["ipfs_hash"])

    # Create a knowledge base
    kb = await client.create_rag_knowledge_base("path/to/doc.pdf", "My KB")

    # Wait for knowledge base to be ready
    while kb["status"] != "ready":
        kb = await client.get_knowledge_base(kb["id"])
        await asyncio.sleep(1)

    # Chat with the knowledge base
    response = await client.create_chat_session(kb["id"], "What is this about?")
    print(response["message"])

if __name__ == "__main__":
    asyncio.run(example())
```

## Available Methods

### File Management

- `upload_file(file_path: str, file_name: str) -> Dict[str, str]`
- `upload_passport(passport_path: str, file_name: str) -> Dict[str, str]`
- `download_file(ipfs_hash: str, save_directory: str) -> str`
- `download(ipfs_hash: str) -> str`
- `delete_file(ipfs_hash: str) -> str`

### Knowledge Base

- `create_rag_knowledge_base(document_path: str, knowledge_base_name: str) -> Dict`
- `add_document_to_knowledge_base(document_path: str, knowledge_base_id: str) -> Dict`
- `delete_document_from_knowledge_base(document_id: str, knowledge_base_id: str) -> str`
- `get_knowledge_bases() -> List[Dict]`
- `get_knowledge_base(knowledge_base_id: str) -> Dict`

### Chat

- `create_chat_session(knowledge_base_id: str, message: str, chat_session_id: Optional[str] = None) -> Dict`
- `get_chat_sessions() -> List[Dict]`
- `get_chat_session(chat_session_id: str) -> Dict`

### Document History

- `get_uploaded_documents() -> List[Dict]`
- `get_uploaded_history(page: int, page_size: int) -> Dict[str, Union[int, List[Dict]]]`

## Features

- Python 3.7+ support
- Async/await support
- File size validation (10MB limit)
- Type hints
- Error handling
- Environment variable configuration

## Error Handling

```python
try:
    await client.upload_file("large_file.pdf", "large.pdf")
except ValueError as e:
    print(f"Upload failed: {e}")  # File size limit error
except Exception as e:
    print(f"SDK error: {e}")  # Other SDK errors
```

## Type Hints

The wrapper includes type hints for better IDE support and code completion:

```python
from typing import Dict, List, Optional, Union

async def get_knowledge_bases() -> List[Dict]:
    ...

async def create_chat_session(
    knowledge_base_id: str,
    message: str,
    chat_session_id: Optional[str] = None
) -> Dict:
    ...
```
