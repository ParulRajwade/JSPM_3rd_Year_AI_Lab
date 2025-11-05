# import os
# import streamlit as st
# from dotenv import load_dotenv
# load_dotenv()  # This loads variables from .env into os.environ


# # LangChain imports
# from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint, ChatHuggingFace
# from langchain.chains import RetrievalQA
# from langchain_community.vectorstores import FAISS
# from langchain_core.prompts import PromptTemplate

# # Page Configuration and Custom CSS
# # Use the custom design from the previous response
# st.set_page_config(
#     page_title="Medical Chatbot",
#     page_icon="⚕️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )


# css = """
# <style>
# /* General App and Font Styling */
# body {
#     background-color: #f8f9fa;
#     color: #333333;
#     font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
# }

# h1 {
#     color: #004080;
#     text-align: center;
#     font-size: 2.5em;
#     font-weight: 600;
# }

# /* Main Chat Container */
# .main .block-container {
#     padding-top: 2rem;
#     padding-bottom: 2rem;
#     max-width: 900px;
# }

# /* Custom Chat Bubbles */
# .chat-bubble {
#     padding: 12px 18px;
#     border-radius: 20px;
#     max-width: 75%;
#     word-wrap: break-word;
#     font-size: 1em;
#     line-height: 1.5;
#     position: relative;
#     border: 1px solid #e0e0e0;
# }

# .user-bubble {
#     background-color: #f0f0f0;
#     align-self: flex-end;
#     border-bottom-right-radius: 5px;
# }

# .bot-bubble {
#     background-color: #e6f2ff;
#     align-self: flex-start;
#     border-bottom-left-radius: 5px;
# }

# /* Avatars */
# .avatar {
#     width: 40px;
#     height: 40px;
#     border-radius: 50%;
#     margin-right: 10px;
#     display: flex;
#     align-items: center;
#     justify-content: center;
#     font-size: 1.2em;
#     background-color: #c4e6c9; /* Soft green for bot */
#     color: #ffffff;
# }

# .user-avatar {
#     margin-left: 10px;
#     background-color: #dcdcdc; /* Light gray for user */
#     color: #555555;
# }

# /* Chat Message Row (including avatar) */
# .chat-message-row {
#     display: flex;
#     align-items: flex-start;
#     gap: 10px;
# }

# .user-message-row {
#     justify-content: flex-end;
# }

# /* Input box styling */
# .stTextInput > div > div > input {
#     border-radius: 25px;
#     padding: 10px 15px;
#     border: 1px solid #ccc;
#     box-shadow: none;
#     transition: all 0.3s ease;
# }

# .stTextInput > div > div > input:focus {
#     border-color: #007bff;
#     box-shadow: 0 0 5px rgba(0, 123, 255, 0.2);
# }

# /* Sidebar Styling */
# .sidebar .sidebar-content {
#     background-color: #ffffff;
#     box-shadow: 2px 0 5px rgba(0,0,0,0.05);
# }

# .sidebar .stButton button {
#     border-radius: 25px;
#     border: 1px solid #004080;
#     color: #004080;
#     background-color: #ffffff;
#     transition: all 0.3s ease;
# }

# .sidebar .stButton button:hover {
#     background-color: #004080;
#     color: #ffffff;
# }
# </style>
# """
# st.markdown(css, unsafe_allow_html=True)

# HF_TOKEN = os.environ.get("HF_TOKEN")

# # Model 
# HUGGINGFACE_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.2"

# # Vector Store 
# DB_FAISS_PATH = "vectorstore/db_faiss"

# # RAG Functions
# @st.cache_resource
# def get_vectorstore():
#     """Loads and caches the FAISS vector store."""
#     try:
#         embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
#         db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
#         return db
#     except FileNotFoundError:
#         st.error(f"Error: The FAISS database was not found at {DB_FAISS_PATH}.")
#         st.stop()
#     except Exception as e:
#         st.error(f"An unexpected error occurred while loading the vector store: {e}")
#         st.stop()


# def set_custom_prompt(custom_prompt_template):
#     """Creates a PromptTemplate object."""
#     prompt = PromptTemplate(template=custom_prompt_template, input_variables=["context", "question"])
#     return prompt


# @st.cache_resource
# def load_llm(huggingface_repo_id, hf_token):
#     """Initializes the HuggingFace LLM Endpoint and wraps it in a ChatHuggingFace adapter."""
#     try:
#         llm_endpoint = HuggingFaceEndpoint(
#             repo_id=huggingface_repo_id,
#             temperature=0.5,
#             huggingfacehub_api_token=hf_token,
#             max_new_tokens=512,
#         )
#         chat_model = ChatHuggingFace(llm=llm_endpoint)
#         return chat_model
#     except Exception as e:
#         st.error(f"Failed to load Hugging Face model: {e}")
#         st.error("Possible reasons: Invalid token, model access requires an explicit grant, or an issue with the Hugging Face API.")
#         return None

# # Main Streamlit App 

# def main():
#     st.title("MediChat AI")
#     st.write("Your personal health assistant. Ask me anything about medical conditions, symptoms, and general health advice.")

#     #  chat history
#     if 'messages' not in st.session_state:
#         st.session_state.messages = []

#     # Display chat messages from history on app rerun
#     for message in st.session_state.messages:
#         if message["role"] == "user":
#             with st.container():
#                 st.markdown(
#                     f"""
#                     <div class="chat-message-row user-message-row">
#                         <div class="chat-bubble user-bubble">{message["content"]}</div>
#                         <div class="avatar user-avatar">👤</div>
#                     </div>
#                     """, unsafe_allow_html=True
#                 )
#         else:
#             with st.container():
#                 st.markdown(
#                     f"""
#                     <div class="chat-message-row">
#                         <div class="avatar">⚕️</div>
#                         <div class="chat-bubble bot-bubble">{message["content"]}</div>
#                     </div>
#                     """, unsafe_allow_html=True
#                 )

#     #  user input
#     user_prompt = st.chat_input("Ask me about a symptom or health concern...")

#     if user_prompt:
#         st.chat_message('user').markdown(user_prompt)
#         st.session_state.messages.append({'role': 'user', 'content': user_prompt})

#         # Check API key
#         if not HF_TOKEN:
#             st.error("HF_TOKEN not found. Please set it as an environment variable.")
#             st.stop()

#         # custom prompt 
#         CUSTOM_PROMPT_TEMPLATE = """
#         Use the pieces of information provided in the context to answer user's question.
#         If you dont know the answer, just say that you dont know, dont try to make up an answer.
#         Dont provide anything out of the given context

#         Context: {context}
#         Question: {question}

#         Start the answer directly. No small talk please.
#         """

#         # RAG Chain Initialization
#         try:
#             with st.spinner("Generating response..."):
#                 # Load vector store from disk
#                 vectorstore = get_vectorstore()

#                 # Initialize the LLM using Hugging Face
#                 llm = load_llm(HUGGINGFACE_REPO_ID, HF_TOKEN)
#                 if llm is None:
#                     st.stop()

#                 # Create the RetrievalQA chain
#                 # Setting return_source_documents=False to avoid unnecessary data retrieval
#                 qa_chain = RetrievalQA.from_chain_type(
#                     llm=llm,
#                     chain_type="stuff",
#                     retriever=vectorstore.as_retriever(search_kwargs={'k': 3}),
#                     return_source_documents=False, 
#                     chain_type_kwargs={'prompt': set_custom_prompt(CUSTOM_PROMPT_TEMPLATE)}
#                 )

#                 # Invoke the chain with the user's query
#                 response = qa_chain.invoke({'query': user_prompt})
#                 result = response["result"]

#                 # Format the final response for display
#                 result_to_show = result

#                 st.chat_message('assistant').markdown(result_to_show)
#                 st.session_state.messages.append({'role': 'assistant', 'content': result_to_show})

#         except Exception as e:
#             st.error(f"An unexpected error occurred during model invocation: {str(e)}")
#             st.warning("Please check your internet connection, API token, and model permissions.")


# #Sidebar 
# with st.sidebar:
#     st.header("MediChat Options")
#     st.markdown("---")
#     if st.button("Start New Chat", use_container_width=True):
#         st.session_state.messages = []
#         st.rerun()
#     st.markdown("---")
#     st.markdown("##### **Disclaimer**")
#     st.markdown("MediChat is an AI assistant and should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified health provider with any questions you may have regarding a medical condition.")


# if __name__ == "__main__":
#     main()


import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv() # This loads variables from .env into os.environ

# LangChain imports
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint, ChatHuggingFace
from langchain.chains import RetrievalQA
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

# Custom CSS for the creative, light-colored UI
css = """
<style>
/* General App and Font Styling */
body {
    background-color: #f8f9fa;
    color: #333333;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

h1 {
    color: #004080;
    text-align: center;
    font-size: 2.5em;
    font-weight: 600;
}

/* Main Chat Container */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 900px;
}

/* Custom Chat Bubbles */
.chat-bubble {
    padding: 12px 18px;
    border-radius: 20px;
    max-width: 75%;
    word-wrap: break-word;
    font-size: 1em;
    line-height: 1.5;
    position: relative;
    border: 1px solid #e0e0e0;
}

.user-bubble {
    background-color: #f0f0f0;
    align-self: flex-end;
    border-bottom-right-radius: 5px;
}

.bot-bubble {
    background-color: #e6f2ff;
    align-self: flex-start;
    border-bottom-left-radius: 5px;
}

/* Avatars */
.avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-right: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2em;
    background-color: #c4e6c9; /* Soft green for bot */
    color: #ffffff;
}

.user-avatar {
    margin-left: 10px;
    background-color: #dcdcdc; /* Light gray for user */
    color: #555555;
}

/* Chat Message Row (including avatar) */
.chat-message-row {
    display: flex;
    align-items: flex-start;
    gap: 10px;
}

.user-message-row {
    justify-content: flex-end;
}

/* Input box styling */
.stTextInput > div > div > input {
    border-radius: 25px;
    padding: 10px 15px;
    border: 1px solid #ccc;
    box-shadow: none;
    transition: all 0.3s ease;
}

.stTextInput > div > div > input:focus {
    border-color: #007bff;
    box-shadow: 0 0 5px rgba(0, 123, 255, 0.2);
}

/* Sidebar Styling */
.sidebar .sidebar-content {
    background-color: #ffffff;
    box-shadow: 2px 0 5px rgba(0,0,0,0.05);
}

.sidebar .stButton button {
    border-radius: 25px;
    border: 1px solid #004080;
    color: #004080;
    background-color: #ffffff;
    transition: all 0.3s ease;
}

.sidebar .stButton button:hover {
    background-color: #004080;
    color: #ffffff;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

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
    st.title("MediChat AI 🎙️")
    st.write("Your personal health assistant. You can speak your question or type it.")

    # 1. VOICE INPUT AREA (Speech-to-Text)
    st.markdown("<h3 style='font-size: 1.2em;'>🎤 Speak Your Question:</h3>", unsafe_allow_html=True)
    voice_transcript = speech_to_text(
        language='en', 
        start_prompt="Click to Start Recording",
        stop_prompt="Stop Recording",
        key='stt_recorder', 
        use_container_width=True
    )
    st.markdown("---") # Visual separator

    # 2. CHAT HISTORY MANAGEMENT
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Combine voice input (if present) with text input
    text_prompt = st.chat_input("...or type your question here")
    
    # Prioritize voice input if a transcription was just completed
    user_prompt = voice_transcript if voice_transcript else text_prompt
    
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.container():
                st.markdown(
                    f"""
                    <div class="chat-message-row user-message-row">
                        <div class="chat-bubble user-bubble">{message["content"]}</div>
                        <div class="avatar user-avatar">👤</div>
                    </div>
                    """, unsafe_allow_html=True
                )
        else:
            with st.container():
                st.markdown(
                    f"""
                    <div class="chat-message-row">
                        <div class="avatar">⚕️</div>
                        <div class="chat-bubble bot-bubble">{message["content"]}</div>
                    </div>
                    """, unsafe_allow_html=True
                )

    # 3. RAG PIPELINE EXECUTION
    if user_prompt:
        # A. Display user prompt (whether typed or spoken)
        st.chat_message('user').markdown(user_prompt)
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
                st.chat_message('assistant').markdown(result)
                
                # --- VOICE OUTPUT INTEGRATION ---
                speak_text(result) 
                
                st.session_state.messages.append({'role': 'assistant', 'content': result})

        except Exception as e:
            st.error(f"An unexpected error occurred during model invocation: {str(e)}")
            st.warning("Please check your internet connection, API token, and model permissions.")


# Sidebar (Unchanged)
with st.sidebar:
    st.header("MediChat Options")
    st.markdown("---")
    if st.button("Start New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.markdown("##### **Disclaimer**")
    st.markdown("MediChat is an AI assistant and should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified health provider with any questions you may have regarding a medical condition.")


if __name__ == "__main__":
    main()