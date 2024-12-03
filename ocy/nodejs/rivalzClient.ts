import RivalzClient from "rivalz-client";
import {
  KnowledgeBase,
  Document,
  ChatSession,
  ChatResponse,
  UploadHistoryItem,
} from "./types";
import fs from "fs/promises";

export class RivalzClientSdk {
  private MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
  private sdk: RivalzClient;

  constructor(secretToken: string) {
    if (!secretToken) {
      throw new Error("SECRET_TOKEN is required");
    }
    this.sdk = new RivalzClient(secretToken);
  }

  private async validateFileSize(filePath: string): Promise<number> {
    const stats = await fs.stat(filePath);
    if (stats.size > this.MAX_FILE_SIZE) {
      throw new Error(
        `File size exceeds maximum limit of ${
          this.MAX_FILE_SIZE / (1024 * 1024)
        }MB`
      );
    }
    return stats.size;
  }

  // File Management Methods
  async uploadFile(
    filePath: string,
    fileName: string
  ): Promise<{ ipfs_hash: string }> {
    await this.validateFileSize(filePath);
    const fileBuffer = await fs.readFile(filePath);
    const result = await this.sdk.uploadFile(fileBuffer, fileName);
    return result;
  }

  async uploadPassport(
    passportImagePath: string,
    fileName: string
  ): Promise<{ ipfs_hash: string }> {
    await this.validateFileSize(passportImagePath);
    const fileBuffer = await fs.readFile(passportImagePath);
    const result = await this.sdk.uploadPassport(fileBuffer, fileName);
    return result;
  }

  async downloadFile(ipfsHash: string, saveDirectory: string): Promise<string> {
    return await this.sdk.downloadFile(ipfsHash, saveDirectory);
  }

  async download(ipfsHash: string): Promise<string> {
    return await this.sdk.download(ipfsHash);
  }

  async deleteFile(ipfsHash: string): Promise<string> {
    const result = await this.sdk.deleteFile(ipfsHash);
    return result;
  }

  // Knowledge Base Methods
  async createRagKnowledgeBase(
    documentPath: string,
    knowledgeBaseName: string
  ): Promise<KnowledgeBase> {
    const result = await this.sdk.createRagKnowledgeBase(
      documentPath,
      knowledgeBaseName
    );
    return result;
  }

  async addDocumentToKnowledgeBase(
    documentPath: string,
    knowledgeBaseId: string
  ): Promise<Document> {
    const result = await this.sdk.addDocumentToKnowledgeBase(
      documentPath,
      knowledgeBaseId
    );
    return result;
  }

  async deleteDocumentFromKnowledgeBase(
    documentId: string,
    knowledgeBaseId: string
  ): Promise<string> {
    const result = await this.sdk.deleteDocumentFromKnowledgeBase(
      documentId,
      knowledgeBaseId
    );
    return result;
  }

  async getKnowledgeBases(): Promise<KnowledgeBase[]> {
    return await this.sdk.getKnowledgeBases();
  }

  async getKnowledgeBase(knowledgeBaseId: string): Promise<KnowledgeBase> {
    return await this.sdk.getKnowledgeBase(knowledgeBaseId);
  }

  // Chat Session Methods
  async createChatSession(
    knowledgeBaseId: string,
    message: string,
    chatSessionId?: string | null
  ): Promise<ChatResponse> {
    return await this.sdk.createChatSession(
      knowledgeBaseId,
      message,
      chatSessionId
    );
  }

  async getChatSessions(): Promise<ChatSession[]> {
    return await this.sdk.getChatSessions();
  }

  async getChatSession(chatSessionId: string): Promise<ChatSession> {
    return await this.sdk.getChatSession(chatSessionId);
  }

  async getUploadedDocuments(): Promise<Document[]> {
    return await this.sdk.getUploadedDocuments();
  }

  async getUploadedHistory(
    page: number,
    pageSize: number
  ): Promise<{
    totalFilesUploaded: number;
    uploadHistories: any;
  }> {
    const response = await this.sdk.getUploadedHistory(page, pageSize);
    console.log("💬 Response:", response);
    return response;
  }
}
