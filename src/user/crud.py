from dotenv import load_dotenv
import os
import time

from pathlib2 import Path
from ..rivalz_client_sdk import RivalzClientSdk
# Initialize Rivalz Client for RAG operations
CURRENT_DIR = Path(__file__).parent

load_dotenv()
rivalz_client = RivalzClientSdk(os.getenv("RIVALZ_SECRET_TOKEN"))

def setup_rag_pipeline(client, RAG_DOCUMENTS):
    
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

