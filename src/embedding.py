from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

class EmbeddingPipeline:
    def __init__(self):
        # AI model to convert text to vectors
        self.model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    def chunk_documents(self, documents):
        # Split big pages into smaller chunks (1000 characters)
        # This helps the AI be more precise.
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        return splitter.split_documents(documents)