# Medical Chatbot

This is a Retrieval-Augmented Generation (RAG) based medical chatbot. It uses a local vector store created from PDF documents to answer user queries about medical topics. The application features a user-friendly web interface built with Streamlit and includes voice input and output capabilities.

## Features

- **RAG Pipeline:** Answers questions based on a provided knowledge base (PDF documents).
- **Hugging Face Integration:** Uses the Mistral-7B model via the Hugging Face Inference API.
- **Local Vector Store:** Creates and uses a local FAISS vector store for efficient document retrieval.
- **Interactive UI:** A clean and modern user interface built with Streamlit.
- **Voice-to-Text:** Allows users to ask questions using their microphone.
- **Text-to-Speech:** Reads the AI's response aloud to the user.

## Project Structure

```
Pratik Rajendra Patil RBT23CB026/
├── data/
│   └── (Your PDF files for the knowledge base go here)
├── Report/
│   └── Mini Project Report.pdf
├── create_memory.py        # Script to create the vector store from PDFs
├── connect_llm.py          # Script for command-line interaction with the RAG chain
├── medical_chatbot.py      # The main Streamlit web application
├── requirements.txt        # A list of all necessary Python packages
├── README.md               # You are here!
└── .env                    # (You must create this) Environment variables file
```

## Setup and Installation

Follow these steps to set up and run the project locally.

### 1. Prerequisites

- Python 3.10 or higher
- Git installed on your system

### 2. Clone the Repository

Clone this repository to your local machine.

```bash
git clone <repository-url>
cd <repository-folder>
```

### 3. Create a Virtual Environment

It is highly recommended to use a virtual environment to manage dependencies.

```bash
# Create the virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 4. Install Dependencies

Install all the required Python packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 5. Set Up Environment Variables

This project requires a Hugging Face API token to access the language model.

1.  **Create a `.env` file** in the root of the `Pratik Rajendra Patil RBT23CB026` directory.
2.  **Get your Hugging Face Token:**
    - Go to [Hugging Face](https://huggingface.co/).
    - Sign up or log in.
    - Go to your Profile -> Settings -> Access Tokens.
    - Create a new token with "read" permissions.
3.  **Add the token to your `.env` file** in the following format:

    ```
    HF_TOKEN="your_hugging_face_api_token_here"
    ```

### 6. Add Your Data

Place all the PDF documents that will serve as the knowledge base inside the `data/` folder.

## Usage

The project has two main steps: creating the knowledge base and running the chatbot.

### Step 1: Create the Vector Store

You must run this script **first**. It will read all the PDFs in the `data/` folder, convert them into numerical embeddings, and save them into a local FAISS vector store in the `vectorstore/` directory.

```bash
python create_memory.py
```

This process only needs to be done once, or whenever you add or change the documents in the `data/` folder.

### Step 2: Run the Medical Chatbot

To start the interactive web application, run the following command:

```bash
streamlit run medical_chatbot.py
```

This will open the application in your default web browser, where you can interact with the chatbot using text or your voice.
