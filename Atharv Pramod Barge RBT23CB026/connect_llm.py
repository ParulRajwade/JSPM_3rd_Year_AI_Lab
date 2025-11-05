import os
from langchain_huggingface import HuggingFaceEndpoint, HuggingFaceEmbeddings, ChatHuggingFace
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS

# Authentication
HF_TOKEN = os.environ.get("HF_TOKEN")

# Model Selection(mistralai/Mistral-7B-Instruct-v0.2)

HUGGINGFACE_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.2" 

# Vector Store Setup
DB_FAISS_PATH = "vectorstore/db_faiss"
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def load_llm(huggingface_repo_id):
    """
    Initializes the HuggingFace LLM Endpoint and wraps it in a ChatHuggingFace adapter.
    This bypasses the 'text-generation' error by forcing the use of the 'conversational' task.
    """
    # HuggingFaceEndpoint
    llm_endpoint = HuggingFaceEndpoint(
        repo_id=huggingface_repo_id,
        task="conversational", 
        temperature=0.5,
        huggingfacehub_api_token=HF_TOKEN,
        max_new_tokens=512, 
    )
    
    # Wrap the endpoint in ChatHuggingFace This allows the LLM (which is a chat model) to be used seamlessly by the RetrievalQA chain which normally expects a generic LLM.
    chat_model = ChatHuggingFace(llm=llm_endpoint)
    return chat_model

# Define Prompt and Chain setup

CUSTOM_PROMPT_TEMPLATE = """
Use the pieces of information provided in the context to answer user's question.
If you dont know the answer, just say that you dont know, dont try to make up an answer. 
Dont provide anything out of the given context

Context: {context}
Question: {question}

Start the answer directly. No small talk please.
"""

def set_custom_prompt(custom_prompt_template):
    """Creates a PromptTemplate object."""
    # We keep PromptTemplate, and the RetrievalQA chain handles converting this to a chat format (System + Human message) for the ChatHuggingFace model.
    prompt = PromptTemplate(template=custom_prompt_template, input_variables=["context", "question"])
    return prompt

# Main Execution

if not HF_TOKEN:
    print("Error: HF_TOKEN environment variable is not set. Please set it in your environment.")
else:
    print(f"HF_TOKEN is set. Attempting to load model {HUGGINGFACE_REPO_ID} with conversational task...")
    
    try:
        # Load Database (Assumes 'vectorstore/db_faiss' exists)

        db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
        print("FAISS database loaded successfully.")

        # Create QA chain
        qa_chain = RetrievalQA.from_chain_type(
            # Pass the ChatHuggingFace object returned by load_llm
            llm=load_llm(HUGGINGFACE_REPO_ID),
            chain_type="stuff",
            retriever=db.as_retriever(search_kwargs={'k': 3}),
            return_source_documents=True,
            chain_type_kwargs={'prompt': set_custom_prompt(CUSTOM_PROMPT_TEMPLATE)}
        )

        print("RAG Chain initialized successfully.")

        # Now invoke with a single query
        user_query = input("Write Query Here: ")
        
        # Invoke the chain
        response = qa_chain.invoke({'query': user_query})
        
        print("\n--- RESULT ---")
        print("MODEL RESPONSE:", response["result"])
        print("\n--- SOURCE DOCUMENTS ---")
        print("SOURCE DOCUMENTS:", response["source_documents"])
        
    except FileNotFoundError:
        print(f"\nFATAL ERROR: The FAISS database was not found at {DB_FAISS_PATH}.")
        print("Please ensure your vector database files exist.")
    except Exception as e:
        # network or model incompatibility errors
        print(f"\nAN ERROR OCCURRED during model invocation: {e}")
        print("\nPossible solutions:")
        print("1. Ensure you have accepted the model's terms on the Hugging Face Hub page.")
        print(f"2. Check if the model {HUGGINGFACE_REPO_ID} is still hosted by the free Inference API.")
        print("3. Check your network connection and token permissions.")
