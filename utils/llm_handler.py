from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.runnables.base import RunnableSerializable
from typing import Any
from langchain.indexes import SQLRecordManager, index
from langchain_core.vectorstores import VectorStore
from routes.user_route import get_one_user
from models.tables import User
from .env_variables import load_db_variables
from llm.db_embedding_manager import DBEmbeddingManager
from llm.chain import ModelChain
from utils.auth.user_auth import get_current_user
from fastapi import HTTPException, Depends, status


class LLMDependancy:
    def __init__(self, user: User):
        self.user = user
        self.db_embedding_manager = self._init_db_embedding_manager()
        self.model_chain = self._init_model_chain()

    def get_chain(self) -> RunnableSerializable[Any, str]:
        return self.model_chain.chain

    def get_retriever(self) -> VectorStoreRetriever:
        return self.db_embedding_manager.retriever

    def get_vectorstore(self) -> VectorStore:
        return self.db_embedding_manager.vector_store

    def get_record_manager(self) -> SQLRecordManager:
        return self.db_embedding_manager.record_manager

    def _init_db_embedding_manager(
        self,
        connection_string: str = load_db_variables(),
        collection_name: str = "mamba_linear-time-sequence",
    ):
        return DBEmbeddingManager(connection_string, collection_name)

    def _init_model_chain(self):
        model_chain: ModelChain = ModelChain(self.db_embedding_manager)
        model_chain.setup_chain()
        return model_chain


def get_llm_dependancy(user: User = Depends(get_current_user)) -> LLMDependancy:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
        )
    return LLMDependancy(user)
