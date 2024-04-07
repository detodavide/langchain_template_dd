from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import VectorStoreRetriever
from llm.db_embedding_manager import DBEmbeddingManager
from langchain_core.runnables.base import RunnableSerializable
from typing import Any
from .template import DEFAULT_TEMPLATE


class ModelChain:
    def __init__(
        self,
        db_embedding_manager: DBEmbeddingManager,
        model=ChatOpenAI(model_name="gpt-3.5-turbo"),
    ):
        self.db_embedding_manager: DBEmbeddingManager = db_embedding_manager
        self.prompt: ChatPromptTemplate = self._default_prompt()
        self.model = model
        self.chain = None

    def setup_chain(self):
        self.chain = (
            {
                "context": itemgetter("question") | self.db_embedding_manager.retriever,
                "question": itemgetter("question"),
                "name": itemgetter("name"),
            }
            | self.prompt
            | self.model
            | StrOutputParser()
        )

    def _default_prompt(self, template: str = DEFAULT_TEMPLATE):
        return ChatPromptTemplate.from_template(template)
