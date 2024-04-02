from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, PyPDFium2Loader
from langchain.schema import Document
import os
from io import BytesIO
from PyPDF2 import PdfReader


def get_path():
    """
    This was just for educational purpose. Loading data from filesystem
    """
    parent_path = os.getcwd()
    docs_path = "/docs_builder/formats/"
    filename = "mamba_linear-time-sequence.pdf"
    return parent_path + docs_path + filename, filename.split(".")[0]


def docs_from_pdf(pdf_reader: PdfReader | None = None, pdf_name: str = ""):
    documents = []

    if pdf_reader:
        for page in pdf_reader.pages:
            raw_text = page.extract_text()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
            )
            chunks = text_splitter.split_text(raw_text)

            for chunk in chunks:
                documents.append(
                    Document(
                        page_content=chunk.replace("\n", " "),
                        metadata={"source": pdf_name},
                    )
                )
    else:
        pdf_content, filename = get_path()
        loader = PyPDFLoader(pdf_content)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=20,
        )
        docs = text_splitter.split_documents(docs)

        for doc in docs:
            documents.append(
                Document(
                    page_content=doc.page_content.replace("\n", " "),
                    metadata={"source": filename},
                )
            )

    return documents
