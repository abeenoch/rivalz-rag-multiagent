import os
import time
from pathlib import Path
from dotenv import load_dotenv
from rivalz_client_sdk import RivalzClientSdk

# Load environment variables
load_dotenv()

# Get current directory
CURRENT_DIR = Path(__file__).parent

def main():
    # Initialize the client
    print("🚀 Initializing Rivalz client...")
    client = RivalzClientSdk(os.getenv("RIVALZ_SECRET_TOKEN"))

    try:
        # Example 1: Upload a file
        print("📁 Uploading file...")
        upload_result = client.upload_file(
            CURRENT_DIR / "../documents/sample.pdf"
        )
        print("✅ File uploaded successfully:", upload_result)

        # Example 2: Upload a passport image
        print("\n📷 Uploading passport...")
        passport_result = client.upload_passport(
            CURRENT_DIR / "../documents/passport.jpg"
        )
        print("✅ Passport uploaded successfully:", passport_result)

        # Example 3: Create a knowledge base
        print("\n📚 Creating knowledge base...")
        knowledge_base = client.create_rag_knowledge_base(
            CURRENT_DIR / "../documents/knowledge.pdf",
            "My Knowledge Base"
        )
        print("✅ Knowledge base created:", knowledge_base["id"])

        # Example 4: Add document to knowledge base
        print("\n📄 Adding document to knowledge base...")
        document = client.add_document_to_knowledge_base(
            CURRENT_DIR / "../documents/additional.pdf",
            knowledge_base["id"]
        )
        print("✅ Document added:", document["id"])

        # Example 5: Get knowledge bases and wait for ready status
        response = client.get_knowledge_bases()
        print("✅ Knowledge bases:", response)

        while response[0]["status"] != "ready":
            response = client.get_knowledge_bases()
            time.sleep(1)  # Wait 1 second before checking again

        # Example 6: Create a chat session
        print("\n💬 Starting chat session...")
        chat_response = client.create_chat_session(
            response[0]["id"],
            "What is the main topic of the document?"
        )
        print("✅ Chat response:", chat_response)

        # Example 7: Get uploaded documents
        documents = client.get_uploaded_documents()
        print("✅ Documents:", documents)

        # Example 8: Get uploaded history
        uploaded_history = client.get_upload_history(1, 10)
        print("✅ Uploaded history:", uploaded_history)

        # Example 9: Download a file
        print("\n⬇️ Downloading file...")
        upload_hash = uploaded_history[1][0]['uploadHash']
        file_name = uploaded_history[1][0]['fileName']
        print("✅ Upload hash:", upload_hash)
        download_path = client.download(
            upload_hash,
            CURRENT_DIR / f"../downloads/{file_name}"
        )
        print("✅ File downloaded to:", download_path)

        # Example 10: Delete a file
        print("\n🗑️ Deleting file...")
        client.delete_file(upload_hash)
        print("✅ File deleted successfully")

    except Exception as error:
        print("❌ Error:", str(error))

if __name__ == "__main__":
    main() 
