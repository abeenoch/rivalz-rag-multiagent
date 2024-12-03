# Rivalz SDK Node.js Wrapper

Simple TypeScript wrapper for the Rivalz SDK with file size validation and type safety.

## Setup

1. Install dependencies:

```bash
npm install rivalz-client dotenv
```

2. Create a `.env` file:

```env
RIVALZ_SECRET_TOKEN=your_secret_token_here
```

## Usage

```typescript
import { RivalzClientSdk } from "./RivalzClient";
import * as dotenv from "dotenv";

dotenv.config();

async function example() {
  const client = new RivalzClientSdk(process.env.RIVALZ_SECRET_TOKEN);

  // Upload a file
  const result = await client.uploadFile("path/to/file.pdf", "document.pdf");
  console.log(result.ipfs_hash);

  // Create a knowledge base
  const kb = await client.createRagKnowledgeBase("path/to/doc.pdf", "My KB");

  // Chat with the knowledge base
  const response = await client.createChatSession(kb.id, "What is this about?");
  console.log(response);
}

example().catch(console.error);
```

## Available Methods

### File Management

- `uploadFile(filePath: string, fileName: string): Promise<{ ipfs_hash: string }>`
- `uploadPassport(passportPath: string, fileName: string): Promise<{ ipfs_hash: string }>`
- `downloadFile(ipfsHash: string, saveDirectory: string): Promise<string>`
- `download(ipfsHash: string): Promise<string>`
- `deleteFile(ipfsHash: string): Promise<string>`

### Knowledge Base

- `createRagKnowledgeBase(documentPath: string, knowledgeBaseName: string): Promise<KnowledgeBase>`
- `addDocumentToKnowledgeBase(documentPath: string, knowledgeBaseId: string): Promise<Document>`
- `deleteDocumentFromKnowledgeBase(documentId: string, knowledgeBaseId: string): Promise<string>`
- `getKnowledgeBases(): Promise<KnowledgeBase[]>`
- `getKnowledgeBase(knowledgeBaseId: string): Promise<KnowledgeBase>`

### Chat

- `createChatSession(knowledgeBaseId: string, message: string, chatSessionId?: string): Promise<ChatResponse>`
- `getChatSessions(): Promise<ChatSession[]>`
- `getChatSession(chatSessionId: string): Promise<ChatSession>`

### Document History

- `getUploadedDocuments(): Promise<Document[]>`
- `getUploadedHistory(page: number, pageSize: number): Promise<{ totalFilesUploaded: number; uploadHistories: UploadHistory[] }>`

## Features

- TypeScript support
- File size validation (10MB limit)
- Async/await support
- Error handling
- Environment variable configuration

## Error Handling

```typescript
try {
  await client.uploadFile("large-file.pdf", "large.pdf");
} catch (error) {
  if (error instanceof Error) {
    console.error("Upload failed:", error.message); // File size or SDK error
  }
}
```
