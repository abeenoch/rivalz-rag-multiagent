from dotenv import load_dotenv
import logging
import requests
import time
from pathlib import Path
from rivalz_client_sdk import RivalzClientSdk
import os
_ = load_dotenv()

from agent import Agent, Swarm
from langchain_community.tools import DuckDuckGoSearchResults


# Initialize Swarm with telemetry
client = Swarm()

# Initialize Rivalz Client for RAG operations
CURRENT_DIR = Path(__file__).parent
rivalz_client = RivalzClientSdk(os.getenv("RIVALZ_SECRET_TOKEN"))

# Global variables to store RAG context
KNOWLEDGE_BASE_ID = None
RAG_DOCUMENTS = []

def setup_rag_pipeline():
    
    global KNOWLEDGE_BASE_ID, RAG_DOCUMENTS
    
    # Initialize the client
    print("🚀 Initializing Rivalz client...")
    client = RivalzClientSdk(os.getenv("RIVALZ_SECRET_TOKEN"))

    try:
        # Upload files
        print("📁 Uploading files...")
        upload_results = []
        
        # Dynamically find and upload PDF files from a documents directory
        documents_dir = CURRENT_DIR / "../documents"
        if documents_dir.exists():
            pdf_files = list(documents_dir.glob("*.pdf"))
            for pdf_file in pdf_files:
                upload_result = client.upload_file(pdf_file)
                upload_results.append(upload_result)
                print(f"✅ File uploaded successfully: {pdf_file.name}")
        
        # Upload other file types if needed (e.g., passport)
        passport_path = documents_dir / "passport.jpg"
        if passport_path.exists():
            passport_result = client.upload_passport(passport_path)
            print("✅ Passport uploaded successfully")

        # Create knowledge base (use the first PDF found)
        if pdf_files:
            print("\n📚 Creating knowledge base...")
            knowledge_base = client.create_rag_knowledge_base(
                pdf_files[0],
                "Multi-Agent RAG Knowledge Base"
            )
            KNOWLEDGE_BASE_ID = knowledge_base["id"]
            print("✅ Knowledge base created:", KNOWLEDGE_BASE_ID)

            # Add additional documents to knowledge base
            for doc in pdf_files[1:]:
                document = client.add_document_to_knowledge_base(
                    doc,
                    KNOWLEDGE_BASE_ID
                )
                RAG_DOCUMENTS.append(document["id"])
                print(f"✅ Document added: {document['id']}")

            # Wait for knowledge base to be ready with a timeout
            timeout_duration = 60  # 1 minute timeout
            start_time = time.time()

            response = client.get_knowledge_bases()
            while response[0]["status"] != "ready":
                if time.time() - start_time > timeout_duration:
                    print("⚠️ Timeout reached: Knowledge base not ready after 60 seconds. Proceeding...")
                    break
                response = client.get_knowledge_bases()
                time.sleep(1)

            print("✅ RAG Pipeline Setup Complete (with or without timeout)")
            return KNOWLEDGE_BASE_ID

    except Exception as error:
        print("❌ RAG Setup Error:", str(error))
        return None





def create_rag_knowledge_base(document_path, knowledge_base_name):
    """
    Create a RAG knowledge base using Rivalz SDK.
    
    Args:
        document_path (str): Path to the document for the knowledge base
        knowledge_base_name (str): Name of the knowledge base
    
    Returns:
        dict: Knowledge base creation result
    """
    try:
        knowledge_base = rivalz_client.create_rag_knowledge_base(
            document_path, 
            knowledge_base_name
        )
        return {
            "status": "success", 
            "knowledge_base_id": knowledge_base.get("id"),
            "message": "Knowledge base created successfully"
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Failed to create knowledge base: {str(e)}"
        }

# Enhanced RAG-aware functions for agents
def query_rag_knowledge_base(query):
    """
    Query the RAG knowledge base with a specific query.
    
    Args:
        query (str): User's query
    
    Returns:
        dict: Contextual response from the knowledge base
    """
    if not KNOWLEDGE_BASE_ID:
        return {"error": "Knowledge base not initialized"}
    
    try:
        client = RivalzClientSdk(os.getenv("RIVALZ_SECRET_TOKEN"))
        chat_response = client.create_chat_session(
            KNOWLEDGE_BASE_ID, 
            query
        )
        return {
            "status": "success",
            "response": chat_response.get("response", "No response"),
            "context": chat_response.get("context", [])
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": f"RAG query failed: {str(e)}"
        }




from langchain_community.tools import DuckDuckGoSearchResults

import json
from langchain_community.tools import DuckDuckGoSearchResults

def rivalz_network_info(query: str) -> dict:
    """
    Perform a search to retrieve information about Rivalz AI and return structured, relevant results.

    Parameters:
    - query (str): The specific query about Rivalz AI.

    Returns:
    - dict: A dictionary containing relevant search results or an error message.
    """
    try:
        # Initialize DuckDuckGo Search Results tool
        search_tool = DuckDuckGoSearchResults()
        
        # Add specific context for Rivalz AI to the query
        full_query = f"Rivalz AI {query}"
        
        # Perform the search and retrieve the results
        raw_results = search_tool.run(full_query)
        
        # Ensure results are valid JSON if applicable
        try:
            results = json.loads(raw_results) if isinstance(raw_results, str) else raw_results
        except json.JSONDecodeError:
            return {
                "error": "Invalid Response Format",
                "message": "Could not parse search results into JSON.",
                "raw_results": raw_results,
            }

        # Validate that results is iterable and contains dictionaries
        if not isinstance(results, list):
            return {
                "error": "Unexpected Response Structure",
                "message": "Results are not in the expected list format.",
                "raw_results": results,
            }

        # Filter and structure the output for clarity
        relevant_results = []
        for result in results:
            if isinstance(result, dict):  # Ensure each result is a dictionary
                title = result.get("title", "No Title")
                url = result.get("link", "No URL")
                snippet = result.get("snippet", "No Snippet")
                
                if "Rivalz AI" in title or "Rivalz AI" in snippet:
                    relevant_results.append({"title": title, "url": url, "snippet": snippet})
        
        # If no relevant results, return a fallback message
        if not relevant_results:
            return {"message": f"No relevant results found for Rivalz AI query: '{query}'."}
        
        return {"results": relevant_results[:3]}  # Return up to 5 relevant results

    except Exception as e:
        return {"error": "Search Tool Error", "message": str(e)}





def monitor_tvl_changes(retries: int = 3):
    """
    Fetch the Total Value Locked (TVL) for all chains using DeFiLlama's /v2/chains endpoint.
    Includes retries for handling failures.
    """
    url = "https://api.llama.fi/v2/chains"  # Endpoint for TVL of all chains

    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise error for non-2xx status codes
            data = response.json()

            # Print or process the TVL data for all chains
            for chain in data:
                print(f"Chain: {chain['name']}, TVL: {chain['tvl']}")
            
            return data  # Return the list of TVLs for further processing if needed

        except requests.RequestException as e:
            logging.error(f"Attempt {attempt + 1} failed: {e}")
        except ValueError as ve:
            logging.error(f"Data error: {ve}")
            raise

    raise RuntimeError("Failed to fetch TVL for all chains after multiple attempts")

COIN_SYMBOL_TO_ID = {
    "BTC" : "bitcoin",
    "ETH" : "ethereum",
    "DOGE" : "dogecoin",
    "BNB" : "binancecoin",
    "ADA" : "cardano",
    "SOL" : "solana",
    "XRP" : "ripple",
    "LTC" : "litecoin",
    "DOT" : "polkadot",
    "MATIC" : "polygon",
    "SHIB" : "shiba-inu",
}

def crypto_price(query: str) -> dict:
    """
    Fetch current cryptocurrency prices.

    Parameters:
    - query (str): The cryptocurrency name or symbol (e.g., BTC, ETH, Bitcoin).

    Returns:
    - dict: A dictionary containing the current price in USD or an error message.
    """
    url = "https://api.coingecko.com/api/v3/simple/price"
    coin_id = COIN_SYMBOL_TO_ID.get(query.upper(), query.lower())
    
    params = {"ids": coin_id, "vs_currencies": "usd"}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

         # Check if valid price data exists
        if coin_id in data:
            price = data[coin_id]["usd"]
            return {"message": f"The current price of {query.upper()} is ${price:.2f} USD."}
        else:
            return {"message": f"Unable to retrieve the price for '{query}'. Check the cryptocurrency name or symbol."}
    except requests.RequestException as e:
        return {"error": "Network Error", "message": str(e)}
    except KeyError:
        return {"error": "Data Error", "message": f"Invalid response for query: {query}"}



def process_onchain_request(request_id, request_type="NOT SPECIFIED"):
    """Process on-chain requests (e.g., token transfers, staking operations). Ask for user confirmation before proceeding."""
    print(f"[mock] Processing on-chain request {request_id} of type {request_type}...")
    return "Request processed!"

def notify_rivalz_agents():
    """Notify relevant Rivalz agents about network updates or user actions."""
    print("[mock] Notifying Rivalz agents about updates...")
    return "Agents notified!"

# Create the agents
triage_agent = Agent(
    name="Rivalz Triage Agent",
    instructions="""Handle general queries about  RIVALZ, also you direct the user to which agent is best suited to handle the user's request and transfer the conversation to that agent.
    - For token transfers, staking and on-chain operations -> On-Chain Operations Agent
    - For TVL monitoring, crypto price and financial analysis -> Financial Analyst Agent
    In specific cases - always transfer to the appropriate specialist.""",
    functions=[rivalz_network_info, create_rag_knowledge_base,query_rag_knowledge_base]
)

onchain_operations_agent = Agent(
    name="On-Chain Operations Agent",
    instructions="Handle token transfers, staking, and on-chain operations for users.",
    functions=[process_onchain_request, query_rag_knowledge_base]
)

financial_analyst_agent = Agent(
    name="Financial Analyst Agent",
    instructions="Analyze and monitor financial data, crypto price including TVL changes and network activity in the blockchain ecosystem.",
    functions=[monitor_tvl_changes, crypto_price, query_rag_knowledge_base]
)

# Define transfer functions
def transfer_back_to_triage():
    """Call this function if the user request needs to be handled by the triage agent."""
    return triage_agent

def transfer_to_onchain_operations():
    """Transfer the conversation to the On-Chain Operations Agent."""
    return onchain_operations_agent

def transfer_to_financial_analyst():
    """Transfer the conversation to the Financial Analyst Agent."""
    return financial_analyst_agent

# Assign functions to the agents
triage_agent.functions = [transfer_to_onchain_operations, transfer_to_financial_analyst, rivalz_network_info]
onchain_operations_agent.functions.append(transfer_back_to_triage)
financial_analyst_agent.functions.append(transfer_back_to_triage)

print("Starting Rivalz AI Agents - Triage, On-Chain Operations, and Financial Analyst Agents")

def main():
    # First, set up the RAG pipeline
    setup_rag_pipeline()
    
    print("\n🤖 Starting Multi-Agent System with RAG")
    
    messages = []
    agent = triage_agent

    while True:
        user_input = input("\033[90mUser\033[0m: ")
        messages.append({"role": "user", "content": user_input})

        response = client.run(agent=agent, messages=messages)
        
        for message in response.messages:
            if message["role"] == "assistant" and message.get("content"):
                print(f"\033[94m{message['sender']}\033[0m: {message['content']}")
            elif message["role"] == "tool":
                tool_name = message.get("tool_name", "")
                print(f"\033[93mSystem\033[0m: {message['content']}")
        
        messages.extend(response.messages)
        agent = response.agent

if __name__ == "__main__":
    main()