from fastapi import APIRouter, HTTPException
from .schemas import QueryRequest, QueryResponse
from .services import KNOWLEDGE_BASE_ID, query_rag_knowledge_base

router = APIRouter()

@router.post("/query/", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    # if not KNOWLEDGE_BASE_ID:
    #     raise HTTPException(status_code=500, detail="Knowledge Base is not initialized.")
    
    result = query_rag_knowledge_base(request.query)
    # result = query_rag_knowledge_base(request.query, request.knowledge_base_id or KNOWLEDGE_BASE_ID)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["message"])

    return {
        "query": request.query,
        "response": result,
        "context": result.get("context", [])
    }

