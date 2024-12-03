import { RivalzClientSdk } from "./RivalzClient";
import path from "path";
import fs from "fs/promises";
import * as dotenv from "dotenv";

dotenv.config();

async function main() {
  // Initialize the client
  console.log("🚀 Initializing Rivalz client...");
  const client = new RivalzClientSdk(process.env.RIVALZ_SECRET_TOKEN);

  try {
    // Example 1: Upload a file
    console.log("📁 Uploading file...");
    const uploadResult = await client.uploadFile(
      path.join(__dirname, "../documents/sample.pdf"),
      "sample.pdf"
    );
    console.log("✅ File uploaded successfully:", uploadResult);

    // Example 2: Upload a passport image
    console.log("\n📷 Uploading passport...");
    const passportResult = await client.uploadPassport(
      path.join(__dirname, "../documents/passport.jpg"),
      "passport.jpg"
    );
    console.log("✅ Passport uploaded successfully:", passportResult);

    // Example 3: Create a knowledge base
    console.log("\n📚 Creating knowledge base...");
    const knowledgeBase = await client.createRagKnowledgeBase(
      path.join(__dirname, "../documents/knowledge.pdf"),
      "My Knowledge Base"
    );
    console.log("✅ Knowledge base created:", knowledgeBase.id);

    // Example 4: Add document to knowledge base
    console.log("\n📄 Adding document to knowledge base...");
    const document = await client.addDocumentToKnowledgeBase(
      path.join(__dirname, "../documents/additional.pdf"),
      knowledgeBase.id
    );
    console.log("✅ Document added:", document.id);

    let response = await client.getKnowledgeBases();
    console.log("✅ Knowledge bases:", response);

    // Example 5: Create a chat session
    while (response[0].status !== "ready") {
      response = await client.getKnowledgeBases();
    }
    const knowledgeBaseId = response[0].id;
    console.log("\n💬 Starting chat session...");
    const chatResponse = await client.createChatSession(
      knowledgeBaseId,
      "What is the main topic of the document?"
    );
    console.log("✅ Chat response:", chatResponse);

    // Example 6: Get uploaded documents
    const documents = await client.getUploadedDocuments();
    console.log("✅ Documents:", documents);

    // Example 7: Get uploaded history
    const uploadedHistory = await client.getUploadedHistory(0, 20);
    console.log("✅ Uploaded history:", uploadedHistory);

    // Example 8: Download a file
    console.log("\n⬇️ Downloading file...");
    const downloadPath = await client.downloadFile(
      uploadedHistory.uploadHistories[0].uploadHash,
      path.join(__dirname, "../downloads")
    );
    console.log("✅ File downloaded to:", downloadPath);

    // Example 9: Delete all files
    await client.deleteFile(uploadedHistory.uploadHistories[0].uploadHash);
    console.log("✅ File deleted successfully");
  } catch (error) {
    console.error("❌ Error:", error instanceof Error ? error.message : error);
  }
}

// Run the example
if (require.main === module) {
  main().catch((error) => {
    console.error("❌ Fatal error:", error);
    process.exit(1);
  });
}
