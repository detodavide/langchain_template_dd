from llm.db_embedding_manager import DBEmbeddingManager
from llm.chain import ModelChain
from fastapi import Depends, Request
from .env_variables import load_db_variables, load_dotenv
from langchain_core.runnables.base import RunnableSerializable
from typing import Any


async def init_db_embedding_manager(
    app,
    connection_string: str = load_db_variables(),
    collection_name: str = "mamba_linear-time-sequence",
):
    app.state.db_embedding_manager = DBEmbeddingManager(
        connection_string, collection_name
    )


async def init_model_chain(app):
    db_embedding_manager = app.state.db_embedding_manager
    app.state.model_chain = ModelChain(db_embedding_manager)
    app.state.model_chain.setup_chain()
