from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from .user.router import router as query_router
# from .user.services import initialize_rag_pipeline

from ocy.services.multi_agent import setup_rag_pipeline, call_multi_agent



app = FastAPI(
    title="Rivalz RAG Multi-Agent API",
    description="API for Rivalz RAG Multi-Agent",
    version="1.0.0"
)

# <!-- Change python to src -->

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# app.include_router(query_router)


# Initialize RAG pipeline on startup
@app.on_event("startup")
async def startup_event():
    await setup_rag_pipeline()


@app.post("/chat")
async def chat(message: str):

    # Call the multi-agent to generate a response
    response = await call_multi_agent(message)
    return {"response": response}
