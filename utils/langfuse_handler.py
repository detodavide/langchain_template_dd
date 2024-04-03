from langfuse import Langfuse
from langfuse.callback.langchain import LangchainCallbackHandler
from fastapi import Depends, status, HTTPException
from utils.auth.user_auth import get_current_user
from models.tables import User


def get_langfuse():
    return Langfuse()


def get_trace_handler(
    langfuse: Langfuse = Depends(get_langfuse), user: User = Depends(get_current_user)
) -> LangchainCallbackHandler:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated"
        )
    trace = langfuse.trace(user_id=user.username)
    return trace.get_langchain_handler()
