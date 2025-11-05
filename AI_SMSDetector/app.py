# -------------------------------
# 📘 app.py — Streamlit Interface
# -------------------------------

import streamlit as st
import joblib
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

nltk.download('stopwords')

# Load Model
model, vectorizer = joblib.load("sms_spam_model.pkl")

stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

# Simple keyword helper
spam_keywords = ["lottery", "congratulations", "offer", "free", "win", "prize", "click", "money"]

def clean_text(text):
    text = text.lower()
    text = ''.join([ch for ch in text if ch not in string.punctuation])
    words = [stemmer.stem(w) for w in text.split() if w not in stop_words]
    return ' '.join(words)

def predict_message(message):
    msg = clean_text(message)
    if any(word in msg for word in spam_keywords):
        return "Spam"
    pred = model.predict(vectorizer.transform([msg]))[0]
    return pred

# Custom CSS for styling
st.markdown("""
<style>
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Title styling */
    .main-title {
        text-align: center;
        color: white;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        animation: fadeInDown 0.8s ease-out;
    }
    
    .subtitle {
        text-align: center;
        color: #f0f0f0;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        animation: fadeInUp 0.8s ease-out;
    }
    
    /* Card container */
    .card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
        animation: slideUp 0.6s ease-out;
    }
    
    /* Result boxes */
    .result-box {
        padding: 1.5rem;
        border-radius: 15px;
        margin-top: 1.5rem;
        text-align: center;
        font-size: 1.3rem;
        font-weight: 600;
        animation: scaleIn 0.5s ease-out;
    }
    
    .spam-result {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
        border: 3px solid #ff5252;
    }
    
    .safe-result {
        background: linear-gradient(135deg, #51cf66 0%, #37b24d 100%);
        color: white;
        border: 3px solid #2f9e44;
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes scaleIn {
        from {
            opacity: 0;
            transform: scale(0.9);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        border: none;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Text area styling */
    .stTextArea > div > div > textarea {
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
    }
    
    /* Feature boxes */
    .feature-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Streamlit UI
st.set_page_config(page_title="Spam Detector", page_icon="📧", layout="wide")

# Header
st.markdown('<h1 class="main-title">📧 SMS Spam Detector</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Powered by Machine Learning • Bagging Ensemble Model</p>', unsafe_allow_html=True)

# Main content area
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    st.markdown("### 💬 Enter Your Message")
    input_msg = st.text_area(
        "",
        placeholder="Type or paste your SMS/Email message here...",
        height=150,
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    predict_button = st.button("🔍 Analyze Message", use_container_width=True)
    
    if predict_button:
        if input_msg.strip() == "":
            st.warning("⚠️ Please enter a message first!")
        else:
            with st.spinner("🔄 Analyzing message..."):
                import time
                time.sleep(0.5)  # Brief delay for effect
                result = predict_message(input_msg)
                
                if result.lower() == "spam":
                    st.markdown("""
                    <div class="result-box spam-result">
                        🚨 SPAM DETECTED<br>
                        <small style="font-size: 0.9rem; font-weight: 400;">
                        This message appears to be spam. Be cautious!
                        </small>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="result-box safe-result">
                        ✅ SAFE MESSAGE<br>
                        <small style="font-size: 0.9rem; font-weight: 400;">
                        This message appears to be legitimate.
                        </small>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer with features
st.markdown("<br><br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">⚡</div>
        <strong>Fast Detection</strong><br>
        <small>Instant results</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">🎯</div>
        <strong>High Accuracy</strong><br>
        <small>ML-powered classification</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">🔒</div>
        <strong>Privacy First</strong><br>
        <small>Local processing</small>
    </div>
    """, unsafe_allow_html=True)