import os
from operator import itemgetter

from dotenv import find_dotenv, load_dotenv
from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
    File,
    Depends,
    Body,
    status,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from io import BytesIO
from typing import Optional
from langchain.indexes import SQLRecordManager, index
from langchain.indexes.base import RecordManager
from langchain.vectorstores import VectorStore
from langfuse.callback.langchain import LangchainCallbackHandler
from fastapi.middleware.cors import CORSMiddleware

from models.validators.document_model import DocumentModel
from models.validators.document_response import DocumentResponse
from docs_builder.add_docs import add_documents
from docs_builder.formats.from_pdf import docs_from_pdf
from PyPDF2 import PdfReader
from utils.env_variables import get_env_variable, load_db_variables
from datasource.pg_session import engine, Base
from models.tables import *
from routes import router as main_router
from contextlib import asynccontextmanager
from utils.auth.user_auth import get_current_user
from utils.langfuse_handler import get_trace_handler
from models.validators.record_manager_model import CleanupMethod
from models.validators.chat import ChatResponse
from starlette.responses import JSONResponse
from utils.app_startup import *
from utils.llm_handler import get_llm_dependancy, LLMDependancy


load_dotenv(find_dotenv())


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(main_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/add-documents/")
async def add_documents_endpoint(
    documents: list[DocumentModel],
    llm_dependancy: LLMDependancy = Depends(get_llm_dependancy),
):
    retriever: VectorStore = llm_dependancy.get_retriever()
    return await add_documents(documents, retriever)


@app.post("/upload-pdf-file/")
async def add_documents_from_file(
    file: UploadFile = File(...),
    collection_name: Optional[str] = Body(None, description="Optional collection name"),
    cleanup: CleanupMethod = Body(CleanupMethod.incremental),
    llm_dependancy: LLMDependancy = Depends(get_llm_dependancy),
):
    """
    Upload a pdf file and store data to the vector_db
    """
    if file.filename.endswith(".pdf"):
        pdf_content = await file.read()
        pdf_stream = BytesIO(pdf_content)
        pdf_reader = PdfReader(pdf_stream)
        documents = docs_from_pdf(pdf_reader=pdf_reader, pdf_name=file.filename)
    return await add_documents(
        documents,
        llm_dependancy.get_record_manager(),
        llm_dependancy.get_vectorstore(),
        cleanup,
    )
