
import os
from pathlib import Path
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

# Load environment variables
project_root = Path(__file__).resolve().parent.parent
load_dotenv(project_root / ".env")

# Connect to Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Load the SAME embedding model used during ingestion
embeddings = HuggingFaceEmbeddings(
    model_name=os.getenv("Local_Embedding_Model", "BAAI/bge-m3"),
    model_kwargs={"device": "cpu"}
)

# Connect to existing vector store
vector_store = PineconeVectorStore(
    index_name="fde-sop-index-local",
    embedding=embeddings
)

# Ask a question
question = "What should be done when cargo temperature exceeds the permitted limit?"

# Retrieve relevant document chunks
results = vector_store.similarity_search_with_score(
    question,
    k=3
)

print("\nQuestion:", question)
print("\nRetrieved SOP content:\n")

for doc, score in results:
    print("Source:", doc.metadata.get("source_file"))
    print("Page:", doc.metadata.get("page_number", "N/A"))
    print("Similarity score:", round(score, 4))
    print("Content:", doc.page_content)
    print("-" * 60)
