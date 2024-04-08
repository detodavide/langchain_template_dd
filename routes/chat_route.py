from collections.abc import Iterator
import json
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
from fastapi.responses import StreamingResponse
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

router = APIRouter()


@router.post("/send-message", response_model=ChatResponse)
async def send_message(
    question: str,
    user: User = Depends(get_current_user),
    handler: LangchainCallbackHandler = Depends(get_trace_handler),
    llmhandler: LLMDependancy = Depends(get_llm_dependancy),
):
    chain, query = await build_chain_and_query(question, user, llmhandler)
    result = await chain.ainvoke(query, config={"callbacks": [handler]})
    return {"message": result}


@router.post("/message-streaming")
async def chat_message_streaming(
    question: str,
    user: User | None = Depends(get_current_user),
    handler: LangchainCallbackHandler = Depends(get_trace_handler),
    llmhandler: LLMDependancy = Depends(get_llm_dependancy),
) -> StreamingResponse:
    chain, query = await build_chain_and_query(question, user, llmhandler)
    return StreamingResponse(
        stream_result(chain, query, handler),
        media_type="application/json",
    )


# UTILS
async def build_chain_and_query(
    question: str,
    user: User = Depends(get_current_user),
    llmhandler: LLMDependancy = Depends(get_llm_dependancy),
) -> RunnableSerializable[Any, str]:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
        )
    query = {"question": question, "name": user.username}
    return llmhandler.get_chain(), query


async def stream_result(
    chain: RunnableSerializable[Any, str],
    query: str,
    handler: LangchainCallbackHandler,
):
    buffer = ""
    text_gen = chain.astream(query, config={"callbacks": [handler]})
    async for text in text_gen:
        buffer += text
        if len(buffer) > 1024 or text.endswith("\\n"):
            json_obj = {"content": buffer}
            yield json.dumps(json_obj) + "\n"
            buffer = ""
    if buffer:
        json_obj = {"content": buffer}
        yield json.dumps(json_obj) + "\n"
