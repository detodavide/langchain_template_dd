from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import VectorStoreRetriever
from llm.db_embedding_manager import DBEmbeddingManager
from langchain_core.runnables.base import RunnableSerializable
from typing import Any

from llm.template import DEFAULT_TEMPLATE
from fastapi import Depends, Request
from langchain_core.vectorstores import VectorStore


class LLMDependancy:
    def __init__(self, request: Request):
        self.request = request

    def get_chain(self) -> RunnableSerializable[Any, str]:
        return self.request.app.state.model_chain.chain

    def get_retriever(self) -> VectorStoreRetriever:
        return self.request.app.state.db_embedding_manager.retriever


def get_llm_dependancy(request: Request) -> LLMDependancy:
    return LLMDependancy(request)
