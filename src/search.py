import os
from langchain_openai import ChatOpenAI
from langchain_classic.chains import RetrievalQA
from src.vectorstore import CloudVectorDB  # <-- Changed Import
from dotenv import load_dotenv

load_dotenv()

class RAGSearch:
    def __init__(self):
        # 1. Connect to Cloud Database
        self.vector_store = CloudVectorDB()
        self.db = self.vector_store.load()
        
        # 2. Get API Key
        api_key = os.getenv("OPENROUTER_API_KEY")

        # 3. Setup OpenRouter
        self.llm = ChatOpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            model="meta-llama/llama-3.3-70b-instruct:free",
            temperature=0
        )

    def search_and_answer(self, query):
        # 4. Create Chain
        # We increase k to 5 since cloud search is fast and we want more context
        retriever = self.db.as_retriever(search_kwargs={"k": 5})
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm, 
            chain_type="stuff", 
            retriever=retriever,
            return_source_documents=True
        )
        
        result = qa_chain.invoke({"query": query})
        return result["result"], result["source_documents"]