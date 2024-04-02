import os

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, Query, Body
from langchain.schema import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader, PyPDFium2Loader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from sqlalchemy.orm import Session
from io import BytesIO
from typing import Annotated, Optional

from models.validators.document_model import DocumentModel
from models.validators.user import UserModel
from models.validators.document_response import DocumentResponse
from datasource.pg_vector_store import AsnyPgVector
from datasource.store_factory import get_vector_store
from docs_builder.add_docs import add_documents
from docs_builder.formats.from_pdf import docs_from_pdf
from PyPDF2 import PdfReader
from utils.env_variables import get_env_variable, load_db_variables
from datasource.pg_session import SessionLocal, engine, Base
from models.tables import *
from routes import router as main_router


load_dotenv(find_dotenv())

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(main_router)


try:
    USE_ASYNC = os.getenv("USE_ASYNC", "False").lower() == "true"
    if USE_ASYNC:
        print("Async project used")

    CONNECTION_STRING = load_db_variables()
    OPENAI_API_KEY = get_env_variable("OPENAI_API_KEY")
    embeddings = OpenAIEmbeddings()

    mode = "async" if USE_ASYNC else "sync"
    pgvector_store = get_vector_store(
        connection_string=CONNECTION_STRING,
        embeddings=embeddings,
        collection_name="test_collection",
        mode=mode,
    )
    retriever = pgvector_store.as_retriever()
    template = """Answer the question based only on the following context:
    {context}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    model = ChatOpenAI(model_name="gpt-3.5-turbo")
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )


except ValueError as e:
    raise HTTPException(status_code=500, detail=str(e))
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


# @app.post("/user-create")
# async def create_user(user: UserModel, db: db_dependency):
#     try:
#         db_user = User(username=user.username, name=user.name)
#         db.add(db_user)
#         db.commit()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     return user


@app.post("/add-documents/")
async def add_documents_endpoint(documents: list[DocumentModel]):
    return await add_documents(documents, pgvector_store)


@app.post("/upload-pdf-file/")
async def add_documents_from_file(
    file: UploadFile = File(...),
    collection_name: Optional[str] = Body(None, description="Optional collection name"),
):
    """
    Upload a pdf file and store data to the vector_db
    """
    try:
        if file.filename.endswith(".pdf"):
            pdf_content = await file.read()
            pdf_stream = BytesIO(pdf_content)
            pdf_reader = PdfReader(pdf_stream)
            documents = docs_from_pdf(pdf_reader=pdf_reader, pdf_name=file.filename)
            new_pgvector_store = get_vector_store(
                embeddings=embeddings,
                collection_name=(
                    collection_name if collection_name else file.filename.split(".")[0]
                ),
                connection_string=CONNECTION_STRING,
                mode=mode,
            )

        return await add_documents(documents, new_pgvector_store, digest=False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get-all-ids/")
async def get_all_ids():
    try:
        if isinstance(pgvector_store, AsnyPgVector):
            ids = await pgvector_store.get_all_ids()
        else:
            ids = pgvector_store.get_all_ids()

        return ids
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get-documents-by-ids/", response_model=list[DocumentResponse])
async def get_documents_by_ids(ids: list[str]):
    try:
        if isinstance(pgvector_store, AsnyPgVector):
            existing_ids = await pgvector_store.get_all_ids()
            documents = await pgvector_store.get_documents_by_ids(ids)
        else:
            existing_ids = pgvector_store.get_all_ids()
            documents = pgvector_store.get_documents_by_ids(ids)

        if not all(id in existing_ids for id in ids):
            raise HTTPException(status_code=404, detail="One or more IDs not found")

        return documents
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/delete-documents/")
async def delete_documents(ids: list[str]):
    try:
        if isinstance(pgvector_store, AsnyPgVector):
            existing_ids = await pgvector_store.get_all_ids()
            await pgvector_store.delete(ids=ids)
        else:
            existing_ids = pgvector_store.get_all_ids()
            pgvector_store.delete(ids=ids)

        if not all(id in existing_ids for id in ids):
            raise HTTPException(status_code=404, detail="One or more IDs not found")

        return {"message": f"{len(ids)} documents deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/")
async def quick_response(msg: str):
    result = chain.invoke(msg)
    return result
