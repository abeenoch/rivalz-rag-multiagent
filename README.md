# RIVALZ-HACKATHON-MULTIAGENT
# Multi-Agent RAG System.

## Overview
This project demonstrates a multi-agent Retrieval-Augmented Generation (RAG) system, built and submitted as my participation of the RIVALS AI world hackathon.

The system leverages a RAG pipeline and three agents to handle tasks like:
- Responding to to queries regarding Rivalz and other block chain related topics.
- Querying and monitoring DeFi protocols.
- Discuss staking and other onchain activities.
- Give financial advice based on data received from various API's dynamically.

---

## Features
- **Multi-Agent System**: Uses three agents to handle various tasks like TVL monitoring.
- **Real-Time TVL Fetching**: Fetches TVL data across multiple chains using the DeFiLlama API.
- **Real-Time Coin price Fetching**: Fetched coin prices accross multiple chains using coingecko API.
- **Real-Time Internet Search**: Search the internet in real time for information using duckduckgo API.
- **Customizable**: Agents can be tailored for specific DeFi protocols and workflows.
- **Error Handling**: Includes retries and logging for better fault tolerance.
- ***RAG-Pipeline**: For more accurate responses, used RIVALZ for vector storage.
- **API**: Used FASTAPI for building the backend API that handles requests and serves data.

#TOOLS
- **OPENAI SWARM**: For multiagent orchestration.
- **RIVALZ CLIENT**: For knowledge base creation vector storage and retrival.
- **DUCKDUCKGO**: Used this for internet search.
- **FASTAPI**: Used this for backend.


