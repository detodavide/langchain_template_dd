from fastapi import APIRouter, HTTPException, Depends, status
from models.tables.User import User
from datasource.pg_session import db_dependency
from langfuse.callback.langchain import LangchainCallbackHandler
from utils.auth.user_auth import get_current_user
from utils.langfuse_handler import get_trace_handler
from models.validators.chat import ChatResponse
from langchain_core.runnables.base import RunnableSerializable
from typing import Any
from utils.llm_handler import get_llm_dependancy, LLMDependancy

router = APIRouter()


@router.post("/send-message", response_model=ChatResponse)
async def send_message(
    question: str,
    user: User = Depends(get_current_user),
    handler: LangchainCallbackHandler = Depends(get_trace_handler),
    llmhandler: LLMDependancy = Depends(get_llm_dependancy),
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
        )
    query = {"question": question, "name": user.username}
    chain: RunnableSerializable[Any, str] = llmhandler.get_chain()
    result = await chain.ainvoke(query, config={"callbacks": [handler]})
    return {"message": result}
