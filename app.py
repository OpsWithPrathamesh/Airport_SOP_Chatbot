import streamlit as st
import os
from src.data_loader import load_all_documents
from src.vectorstore import CloudVectorDB
from src.search import RAGSearch

# 1. Title and Setup
st.set_page_config(page_title="Airport SOP Assistant", layout="wide")
st.title("✈️ Airport Operations AI Assistant")

# 2. Sidebar (The control panel)
with st.sidebar:
    st.header("Admin Controls")
    if st.button("🔄 Build/Update Database"):
        with st.spinner("Processing PDFs & Uploading to Pinecone..."):
            docs = load_all_documents("data")
            if docs:
                store = CloudVectorDB() # <-- Changed
                store.build_from_documents(docs)
                st.success(f"Success! Uploaded {len(docs)} chunks to the Cloud.")

# 3. Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Handle User Input
if prompt := st.chat_input("Ask about Airport SOPs..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI Response
    with st.chat_message("assistant"):
        try:
            bot = RAGSearch()
            response, sources = bot.search_and_answer(prompt)
            
            st.markdown(response)
            
            # Show the sources (Evidence)
            with st.expander("View Source Documents"):
                for doc in sources:
                    st.caption(f"📄 Source: {doc.metadata.get('source', 'Unknown')} | Page: {doc.metadata.get('page', 0)}")
                    st.text(doc.page_content[:300] + "...")
            
            st.session_state.messages.append({"role": "assistant", "content": response})
        # New code
        except Exception as e:
            import traceback
            st.error(f"❌ An error occurred: {e}")
            st.text(traceback.format_exc()) # This prints the full error trace on screen