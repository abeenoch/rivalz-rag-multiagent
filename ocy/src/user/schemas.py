from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    query: str
    knowledge_base_id: Optional[str] = None

class QueryResponse(BaseModel):
    query: str
    response: str
    context: List[str] = []
