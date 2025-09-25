import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings


# ----------------------------
# 1. Load API Key
# ----------------------------
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")

# ----------------------------
# 2. Load documents
# ----------------------------
docs = []

# Example: Load a PDF
base_dir = os.path.dirname(__file__) 
file_path = os.path.join(base_dir, "sample_rag.pdf")
pdf_loader = PyPDFLoader(file_path)
docs.extend(pdf_loader.load())

# Example: Load a Word file
#docx_loader = Docx2txtLoader("sample.docx")
#docs.extend(docx_loader.load())

# ----------------------------
# 3. Split documents into chunks
# ----------------------------
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
documents = text_splitter.split_documents(docs)

# ----------------------------
# 4. Create embeddings + vectorstore
# ----------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="hkunlp/instructor-large",
    model_kwargs={"device": "cpu"}
)
vectorstore = FAISS.from_documents(documents, embeddings)

# ----------------------------
# 5. Retriever + Gemini
# ----------------------------
retriever = vectorstore.as_retriever()
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3, google_api_key=google_api_key)

# ----------------------------
# 6. Conversational RAG Chain
# ----------------------------
memory = ConversationBufferMemory(memory_key="chat_history",
                                   return_messages=True, 
                                   output_key="answer")

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=True,
    verbose=True,
    output_key="answer"
)

# ----------------------------
# 7. Chat loop
# ----------------------------
if __name__ == "__main__":
    print("🤖 Gemini RAG Chatbot ready with PDF/Word support! Type 'exit' to quit.")
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit"]:
            break

        result = qa_chain({"question": query})
        answer = result["answer"]
        sources = [doc.page_content[:200] + "..." for doc in result["source_documents"]]  # show preview

        print("Bot:", answer)
        print("📚 Sources:", sources)