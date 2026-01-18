import os
import time
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from src.embedding import EmbeddingPipeline
from dotenv import load_dotenv

load_dotenv()

class CloudVectorDB:
    def __init__(self):
        self.index_name = os.getenv("PINECONE_INDEX_NAME")
        self.api_key = os.getenv("PINECONE_API_KEY")
        self.pipeline = EmbeddingPipeline()
        
        # Initialize Pinecone Client
        self.pc = Pinecone(api_key=self.api_key)

    def build_from_documents(self, documents):
        print("[INFO] Chunking documents...")
        chunks = self.pipeline.chunk_documents(documents)
        
        print(f"[INFO] Connecting to Pinecone index '{self.index_name}'...")
        
        # Check if index exists, if not create it (Serverless)
        existing_indexes = [i.name for i in self.pc.list_indexes()]
        if self.index_name not in existing_indexes:
            print(f"[INFO] Creating new index: {self.index_name}")
            self.pc.create_index(
                name=self.index_name,
                dimension=384, # Must match all-MiniLM-L6-v2
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
            # Wait a moment for index to initialize
            time.sleep(2)

        print(f"[INFO] Uploading {len(chunks)} vectors to Cloud (this may take a while)...")
        # This uploads the vectors to Pinecone
        self.db = PineconeVectorStore.from_documents(
            documents=chunks, 
            embedding=self.pipeline.model, 
            index_name=self.index_name
        )
        print("[INFO] Upload complete!")

    def load(self):
        # Connect to the existing cloud index
        self.db = PineconeVectorStore.from_existing_index(
            index_name=self.index_name,
            embedding=self.pipeline.model
        )
        return self.db