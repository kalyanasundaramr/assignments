import os
import shutil
import tempfile
import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables from .env file
load_dotenv()

# Page Configuration
st.set_page_config(page_title="Multi-PDF RAG Assistant", page_icon="📚", layout="centered")

st.title("📚 Multi-PDF RAG Assistant with Local Storage")
st.markdown("Upload multiple PDF documents, index them into a local vector database, and ask questions with precise source citations.")

# Verify API Key is available
if not os.environ.get("OPENAI_API_KEY"):
    st.error("⚠️ OpenAI API key not found! Please check your `.env` file and make sure it contains your `OPENAI_API_KEY`.")
    st.stop()

DB_FAISS_PATH = "faiss_index"

# Automatically load the vector database from local storage on startup if it exists
if "store" not in st.session_state:
    if os.path.exists(DB_FAISS_PATH):
        with st.spinner("Loading existing vector database from local storage..."):
            try:
                st.session_state.store = FAISS.load_local(
                    DB_FAISS_PATH, 
                    OpenAIEmbeddings(), 
                    allow_dangerous_deserialization=True
                )
                st.success("Loaded existing vector index from disk!")
            except Exception as e:
                st.error(f"Error loading local index: {e}")

# Sidebar controls for file upload and index clearing
st.sidebar.header("Document Management")
files = st.sidebar.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)

if os.path.exists(DB_FAISS_PATH):
    if st.sidebar.button("🗑️ Clear Local Index & Reset"):
        if os.path.exists(DB_FAISS_PATH):
            shutil.rmtree(DB_FAISS_PATH)
        if "store" in st.session_state:
            del st.session_state.store
        st.success("Local vector index cleared!")
        st.rerun()

# Process new file uploads if no store is currently active in session
if files and "store" not in st.session_state:
    with st.spinner("Processing and indexing documents..."):
        chunks = []
        for f in files:
            # Save uploaded file temporarily so PyPDFLoader can access its path
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(f.getvalue())
                tmp_path = tmp_file.name
            
            try:
                loader = PyPDFLoader(tmp_path)
                docs = loader.load()
                
                # Update metadata source to display original uploaded file name
                for doc in docs:
                    doc.metadata["source"] = f.name
                
                # Split documents into chunks
                splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                file_chunks = splitter.split_documents(docs)
                chunks.extend(file_chunks)
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
        
        if chunks:
            # Create FAISS vector store, save it locally, and keep in session state
            store = FAISS.from_documents(chunks, OpenAIEmbeddings())
            store.save_local(DB_FAISS_PATH)
            st.session_state.store = store
            st.success(f"Indexed {len(chunks)} chunks and saved locally to `{DB_FAISS_PATH}`!")
        else:
            st.error("No valid text could be extracted from the uploaded PDFs.")

# Question Answering Section
if "store" in st.session_state:
    st.divider()
    st.subheader("Ask a Question")
    question = st.text_input("Type your question here...")
    
    if question:
        with st.spinner("Retrieving answers and sources..."):
            # Retrieve relevant chunks
            retriever = st.session_state.store.as_retriever(search_kwargs={"k": 4})
            docs = retriever.invoke(question)
            
            # Generate response using ChatOpenAI
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a helpful assistant. Answer the question using ONLY the provided context below. If the answer is not in the context, state that you cannot find the answer.\n\nContext:\n{context}"),
                ("human", "{input}")
            ])
            
            context_text = "\n\n".join([d.page_content for d in docs])
            response = llm.invoke(prompt.format(context=context_text, input=question))
            
            # Display Answer
            st.markdown("### Answer")
            st.write(response.content)
            
            # Display Sources (Filename & 1-indexed page number)
            st.markdown("### Sources")
            seen_sources = set()
            sources_list = []
            for d in docs:
                source_name = os.path.basename(d.metadata.get('source', 'Unknown'))
                page_num = d.metadata.get('page', 0) + 1  # PyPDFLoader pages are 0-indexed
                source_key = (source_name, page_num)
                if source_key not in seen_sources:
                    seen_sources.add(source_key)
                    sources_list.append(f"{source_name} - page {page_num}")
            
            st.caption(" | ".join(sources_list))
else:
    st.info("👈 Please upload one or more PDF files via the sidebar to begin indexing.")