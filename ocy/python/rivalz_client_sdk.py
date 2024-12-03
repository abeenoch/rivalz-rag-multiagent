from rivalz_client.client import RivalzClient
import os
from typing import Dict, List, Optional, Union
from pathlib import Path

class RivalzClientSdk:
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    def __init__(self, secret_token: str):
        if not secret_token:
            raise ValueError("SECRET_TOKEN is required")
        self.sdk = RivalzClient(secret_token)

    def _validate_file_size(self, file_path: str) -> int:
        file_size = os.path.getsize(file_path)
        if file_size > self.MAX_FILE_SIZE:
            raise ValueError(
                f"File size exceeds maximum limit of {self.MAX_FILE_SIZE / (1024 * 1024)}MB"
            )
        return file_size

    # File Management Methods
    def upload_file(self, file_path: str) -> Dict[str, str]:
        self._validate_file_size(file_path)
        result = self.sdk.upload_file(file_path)
        return result

    def upload_passport(self, passport_path: str) -> Dict[str, str]:
        self._validate_file_size(passport_path)
        result = self.sdk.upload_passport(passport_path)
        return result

    def download(self, ipfs_hash: str, save_directory: str) -> str:
        return self.sdk.download(ipfs_hash, save_directory)

    def delete_file(self, ipfs_hash: str) -> str:
        result = self.sdk.delete_file(ipfs_hash)
        return result

    # Knowledge Base Methods
    def create_rag_knowledge_base(
        self, document_path: str, knowledge_base_name: str
    ) -> Dict:
        result = self.sdk.create_rag_knowledge_base(
            document_path, knowledge_base_name
        )
        return result

    def add_document_to_knowledge_base(
        self, document_path: str, knowledge_base_id: str
    ) -> Dict:
        result = self.sdk.add_document_to_knowledge_base(
            document_path, knowledge_base_id
        )
        return result

    def delete_document_from_knowledge_base(
        self, document_id: str, knowledge_base_id: str
    ) -> str:
        result = self.sdk.delete_document_from_knowledge_base(
            document_id, knowledge_base_id
        )
        return result

    def get_knowledge_bases(self) -> List[Dict]:
        return self.sdk.get_knowledge_bases()

    def get_knowledge_base(self, knowledge_base_id: str) -> Dict:
        return self.sdk.get_knowledge_base(knowledge_base_id)

    # Chat Session Methods
    def create_chat_session(
        self,
        knowledge_base_id: str,
        message: str,
        chat_session_id: Optional[str] = None,
    ) -> Dict:
        return self.sdk.create_chat_session(
            knowledge_base_id, message, chat_session_id
        )

    def get_chat_sessions(self) -> List[Dict]:
        return self.sdk.get_chat_sessions()

    def get_chat_session(self, chat_session_id: str) -> Dict:
        return self.sdk.get_chat_session(chat_session_id)

    def get_uploaded_documents(self) -> List[Dict]:
        return self.sdk.get_uploaded_documents()

    def get_upload_history(
        self, page: int, page_size: int
    ) -> Dict[str, Union[int, List[Dict]]]:
        response = self.sdk.get_upload_history(page, page_size)
        return response 