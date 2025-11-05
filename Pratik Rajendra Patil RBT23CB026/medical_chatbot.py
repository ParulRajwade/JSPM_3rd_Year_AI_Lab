import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv() # This loads variables from .env into os.environ

# LangChain imports
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint, ChatHuggingFace
# Use classic chains compatibility where necessary
from langchain_classic.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate

# Voice Imports
from streamlit_mic_recorder import speech_to_text
from gtts import gTTS
import io

# --- Page Configuration and Custom CSS ---
st.set_page_config(
    page_title="Medical Chatbot",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple and minimal CSS styling
st.markdown("""
    <style>
        /* Base styles */
        .stApp {
            max-width: 1000px;
            margin: 0 auto;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Header */
        h1 {
            color: #2c5282;
            text-align: center;
            padding: 1rem 0;
            font-size: 2rem;
            border-bottom: 2px solid #e2e8f0;
            margin-bottom: 2rem;
        }
        
        /* Chat messages */
        .chat-message {
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            display: flex;
            gap: 1rem;
            align-items: flex-start;
        }
        
        .user-message {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            margin-left: 2rem;
        }
        
        .bot-message {
            background: #f0f9ff;
            border: 1px solid #bfdbfe;
            margin-right: 2rem;
        }
        
        /* Message content */
        .message-content {
            flex: 1;
        }
        
        /* Avatars */
        .avatar {
            width: 2.5rem;
            height: 2.5rem;
            border-radius: 0.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            flex-shrink: 0;
        }
        
        /* Input area */
        .stTextInput input {
            border: 1px solid #e2e8f0;
            padding: 0.75rem;
            border-radius: 0.5rem;
            width: 100%;
            margin-bottom: 1rem;
        }
        
        /* Voice input button */
        .streamlit-recorder button {
            background: #2c5282;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            cursor: pointer;
        }
        
        /* Sidebar */
        .sidebar .sidebar-content {
            background: #f8fafc;
            padding: 1rem;
        }
        
        /* New chat button */
        .sidebar .stButton button {
            width: 100%;
            background: #2c5282;
            color: white;
            border: none;
            padding: 0.5rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
        }
        
        /* Disclaimer */
        .disclaimer {
            margin-top: 2rem;
            padding: 1rem;
            background: #fff;
            border: 1px solid #e2e8f0;
            border-radius: 0.5rem;
            font-size: 0.875rem;
            color: #4a5568;
        }
    </style>
""", unsafe_allow_html=True)
# --- Configuration ---
HF_TOKEN = os.environ.get("HF_TOKEN")
HUGGINGFACE_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.2"
DB_FAISS_PATH = "vectorstore/db_faiss"

# --- Voice Function ---
def speak_text(text):
    """Converts text to speech and plays it automatically."""
    try:
        # 1. Generate speech using gTTS
        tts = gTTS(text=text, lang='en')
        
        # 2. Save the audio to a BytesIO object (in memory)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        
        # 3. Play the audio automatically
        st.audio(audio_fp, format='audio/mp3', autoplay=True)
    except Exception as e:
        # Fails silently if no internet or gTTS issue, but logs to terminal
        st.error("Text-to-Speech failed. Check internet connection.")
        print(f"TTS Error: {e}")

# --- RAG Functions (Unchanged) ---
@st.cache_resource
def get_vectorstore():
    """Loads and caches the FAISS vector store."""
    try:
        embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
        return db
    except FileNotFoundError:
        st.error(f"Error: The FAISS database was not found at {DB_FAISS_PATH}.")
        st.stop()
    except Exception as e:
        st.error(f"An unexpected error occurred while loading the vector store: {e}")
        st.stop()


def set_custom_prompt(custom_prompt_template):
    """Creates a PromptTemplate object."""
    prompt = PromptTemplate(template=custom_prompt_template, input_variables=["context", "question"])
    return prompt


@st.cache_resource
def load_llm(huggingface_repo_id, hf_token):
    """Initializes the HuggingFace LLM Endpoint and wraps it in a ChatHuggingFace adapter."""
    try:
        llm_endpoint = HuggingFaceEndpoint(
            repo_id=huggingface_repo_id,
            temperature=0.5,
            huggingfacehub_api_token=hf_token,
            max_new_tokens=512,
        )
        chat_model = ChatHuggingFace(llm=llm_endpoint)
        return chat_model
    except Exception as e:
        st.error(f"Failed to load Hugging Face model: {e}")
        st.error("Possible reasons: Invalid token, model access requires an explicit grant, or an issue with the Hugging Face API.")
        return None

# --- Main Streamlit App --- 
def main():
    # Simple header with minimal styling
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="color: #2c5282; margin-bottom: 0.5rem;">
                ⚕️ MediChat AI
            </h1>
            <p style="color: #4a5568;">Your Healthcare Assistant</p>
        </div>
    """, unsafe_allow_html=True)

    # Voice Input Section using native Streamlit components
    with st.container():
        col1, col2 = st.columns([0.1, 0.9])
        with col1:
            st.markdown("🎤")
        with col2:
            st.markdown("#### Voice Input Enabled")
            st.caption("Speak naturally to interact with MediChat")
    
    voice_transcript = speech_to_text(
        language='en',
        start_prompt="Start Recording",
        stop_prompt="Stop Recording",
        key='stt_recorder',
        use_container_width=True
    )
    
    # Subtle Separator
    st.markdown("""
        <div style='
            width: 100%;
            height: 1px;
            background: linear-gradient(to right, transparent, #e2e8f0, transparent);
            margin: 2rem 0;
        '>
        </div>
    """, unsafe_allow_html=True)

    # 2. CHAT HISTORY MANAGEMENT
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Combine voice input (if present) with text input
    text_prompt = st.chat_input("...or type your question here")
    
    # Prioritize voice input if a transcription was just completed
    user_prompt = voice_transcript if voice_transcript else text_prompt
    
    # Simple Message Display
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "⚕️"):
            st.write(message["content"])

    # 3. RAG PIPELINE EXECUTION
    if user_prompt:
    # Display user prompt (whether typed or spoken)
        with st.chat_message("user", avatar="👤"):
            st.write(user_prompt)
        st.session_state.messages.append({'role': 'user', 'content': user_prompt})

        # B. Check API key
        if not HF_TOKEN:
            st.error("HF_TOKEN not found. Please set it as an environment variable.")
            st.stop()

        # C. Custom prompt setup
        CUSTOM_PROMPT_TEMPLATE = """
        Use the pieces of information provided in the context to answer user's question.
        If you dont know the answer, just say that you dont know, dont try to make up an answer.
        Dont provide anything out of the given context

        Context: {context}
        Question: {question}

        Start the answer directly. No small talk please.
        """

        # D. RAG Chain Initialization
        try:
            with st.spinner("Generating response..."):
                vectorstore = get_vectorstore()
                llm = load_llm(HUGGINGFACE_REPO_ID, HF_TOKEN)
                if llm is None: st.stop()

                qa_chain = RetrievalQA.from_chain_type(
                    llm=llm,
                    chain_type="stuff",
                    retriever=vectorstore.as_retriever(search_kwargs={'k': 3}),
                    return_source_documents=False, 
                    chain_type_kwargs={'prompt': set_custom_prompt(CUSTOM_PROMPT_TEMPLATE)}
                )

                response = qa_chain.invoke({'query': user_prompt})
                result = response["result"]

                # E. Display and Speak the Answer
                with st.chat_message("assistant", avatar="⚕️"):
                    st.write(result)
                
                # --- VOICE OUTPUT INTEGRATION ---
                speak_text(result) 
                
                st.session_state.messages.append({'role': 'assistant', 'content': result})

        except Exception as e:
            st.error(f"An unexpected error occurred during model invocation: {str(e)}")
            st.warning("Please check your internet connection, API token, and model permissions.")


# Sidebar Content
with st.sidebar:
    st.title("⚕️ MediChat Controls")
    st.divider()
    
    # New Chat Button
    if st.button("+ New chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    # Capabilities Section
    st.subheader("Capabilities")
    st.markdown("✓ Medical knowledge & diagnosis assistance")
    st.markdown("✓ Voice input & response")
    st.markdown("✓ Evidence-based information")
    
    st.divider()
    
    # Disclaimer Section
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        st.markdown("⚠️")
    with col2:
        st.markdown("### Important Medical Notice")
    
    st.warning("""
    MediChat provides general medical information for educational purposes only. 
    This AI assistant is not a substitute for:
    
    • Professional medical advice
    • Clinical diagnosis
    • Treatment recommendations
    
    Always consult qualified healthcare providers for medical decisions.
    """)
    
    # Footer
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("⚕️ © 2025 MediChat AI")
    with col2:
        st.markdown("v2.0", help="Medical Information System")


if __name__ == "__main__":
    main()