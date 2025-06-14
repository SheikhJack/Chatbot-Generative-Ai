from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from pinecone import Pinecone as Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

load_dotenv()

PINECONE_API_KEY=os.environ.get("PINECONE_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY



extracted_data=load_pdf_file(data="Data/")
text_chunks=text_split(extracted_data)
embeddings = download_hugging_face_embeddings()


docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name="medibot",
    embedding=embeddings
)