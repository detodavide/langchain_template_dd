from fastapi import FastAPI, HTTPException
from langchain.schema import Document
from langchain_community.vectorstores.pgvector import PGVector
from langchain.indexes import SQLRecordManager, index


async def add_documents(
    documents, record_manager: SQLRecordManager, pgvector_store: PGVector, cleanup
):

    try:
        result = index(
            documents,
            record_manager,
            pgvector_store,
            cleanup=cleanup.value,
            source_id_key="source",
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
