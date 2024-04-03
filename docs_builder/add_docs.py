from fastapi import FastAPI, HTTPException
from langchain.schema import Document
from langchain_community.vectorstores.pgvector import PGVector
from langchain.indexes import SQLRecordManager

from datasource.pg_vector_store import AsnyPgVector
from datasource.store_factory import get_vector_store


async def add_documents(
    docs, record_manager: SQLRecordManager, pgvector_store: PGVector, digest=True
):

    try:
        if digest:
            documents = [
                Document(
                    page_content=doc.page_content,
                    metadata=(
                        {**doc.metadata, "digest": doc.generate_digest()}
                        if doc.metadata
                        else {"digest": doc.generate_digest()}
                    ),
                )
                for doc in docs
            ]
        else:
            documents = docs

        if record_manager:
            ids = await record_manager.add_documents(documents)
        else:
            ids = (
                await pgvector_store.aadd_documents(documents)
                if isinstance(pgvector_store, AsnyPgVector)
                else pgvector_store.add_documents(documents)
            )
        return {"message": "Documents added successfully", "ids": ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
