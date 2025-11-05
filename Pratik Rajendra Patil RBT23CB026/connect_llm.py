import os
from langchain_huggingface import HuggingFaceEndpoint, HuggingFaceEmbeddings, ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate
# Use the compatibility package that exposes classic chain helpers
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import FAISS

# --- Environment and Model Configuration (Unchanged) ---
HF_TOKEN = os.environ.get("HF_TOKEN")
HUGGINGFACE_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.2"
DB_FAISS_PATH = "vectorstore/db_faiss"

# --- Embedding Model (Unchanged) ---
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def load_llm(huggingface_repo_id):
    """Initializes the HuggingFace LLM Endpoint and wraps it in a ChatHuggingFace adapter."""
    llm_endpoint = HuggingFaceEndpoint(
        repo_id=huggingface_repo_id,
        task="conversational",
        temperature=0.5,
        huggingfacehub_api_token=HF_TOKEN,
        max_new_tokens=512,
    )
    chat_model = ChatHuggingFace(llm=llm_endpoint)
    return chat_model

# --- Modern Prompt and Chain Setup ---

# Use ChatPromptTemplate for chat models for better clarity
CUSTOM_PROMPT_TEMPLATE = """Use the following pieces of context to answer the user's question.
If you don't know the answer, just say that you don't know. Don't try to make up an answer.
Keep the answer concise and based ONLY on the provided context.

Context: {context}

Question: {input}

Start the answer directly. No small talk please."""

def create_rag_chain(llm, retriever, custom_prompt_template):
    """Creates a modern retrieval chain using LCEL."""
    
    prompt = ChatPromptTemplate.from_template(custom_prompt_template)
    
    # This chain takes a question and retrieved documents and formats them into a prompt
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    
    # This chain takes a user question, retrieves relevant documents, and passes them to the question_answer_chain
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    return rag_chain

# --- Main Execution ---

if not HF_TOKEN:
    print("Error: HF_TOKEN environment variable is not set. Please set it in your environment.")
else:
    print(f"HF_TOKEN is set. Attempting to load model {HUGGINGFACE_REPO_ID} with conversational task...")

    try:
        # Load the local FAISS database
        db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
        print("FAISS database loaded successfully.")

        # Create a retriever from the database
        retriever = db.as_retriever(search_kwargs={'k': 3})

        # Load the language model
        llm = load_llm(HUGGINGFACE_REPO_ID)

        # Create the modern RAG chain
        rag_chain = create_rag_chain(llm, retriever, CUSTOM_PROMPT_TEMPLATE)
        print("Modern RAG Chain initialized successfully.")

        # Get user input
        user_query = input("Write Query Here: ")

        # Invoke the chain with the user's query
        # Note: The input key is 'input' by default in create_retrieval_chain
        response = rag_chain.invoke({'input': user_query})

        # Print the results
        print("\n--- RESULT ---")
        print("MODEL RESPONSE:", response["answer"])
        print("\n--- SOURCE DOCUMENTS ---")
        # The source documents are now nested in the 'context' key
        for i, doc in enumerate(response["context"]):
            print(f"\n--- Document {i+1} ---\n")
            print(doc.page_content)

    except FileNotFoundError:
        print(f"\nFATAL ERROR: The FAISS database was not found at {DB_FAISS_PATH}.")
        print("Please ensure your vector database files exist.")
    except Exception as e:
        print(f"\nAN ERROR OCCURRED during model invocation: {e}")
        print("\nPossible solutions:")
        print("1. Ensure you have accepted the model's terms on the Hugging Face Hub page.")
        print(f"2. Check if the model {HUGGINGFACE_REPO_ID} is still hosted by the free Inference API.")
        print("3. Check your network connection and token permissions.")