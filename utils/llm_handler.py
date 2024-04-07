from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import VectorStoreRetriever
from llm.db_embedding_manager import DBEmbeddingManager
from langchain_core.runnables.base import RunnableSerializable
from typing import Any

from utils.env_variables import load_db_variables, get_env_variable
from llm.template import DEFAULT_TEMPLATE
from fastapi import Depends, Request


def get_chain(request: Request) -> RunnableSerializable[Any, str]:
    return request.app.state.model_chain.chain


def get_retriever():
    return
