from pathlib import Path
from typing import List
from langchain_community.document_loaders import PyPDFLoader

def load_all_documents(data_dir: str) -> List:
    # 1. Find the folder
    data_path = Path(data_dir).resolve()
    documents = []
    
    # 2. Look for all .pdf files
    pdf_files = list(data_path.glob('**/*.pdf'))
    print(f"[INFO] Found {len(pdf_files)} PDF files.")
    
    # 3. Loop through each file and load it
    for pdf_file in pdf_files:
        try:
            loader = PyPDFLoader(str(pdf_file))
            docs = loader.load()
            print(f"[INFO] Loaded {len(docs)} pages from {pdf_file.name}")
            documents.extend(docs)
        except Exception as e:
            print(f"[ERROR] Could not load {pdf_file}: {e}")
            
    return documents