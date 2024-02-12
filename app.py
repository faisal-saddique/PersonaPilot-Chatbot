import streamlit as st
from openai import OpenAI
from langchain.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import fitz  # PyMuPDF
from random import randint
import os
# Load environment variables
load_dotenv()

# OpenAI initialization
client = OpenAI()

# Set page configuration with an icon
st.set_page_config(page_title="PersonaPilot-Chat", page_icon="🚀")

@st.cache_resource
def get_vectorstore():
    VECTORSTORE_NAME = os.getenv('VECTORSTORE_NAME')
    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(VECTORSTORE_NAME, embeddings=embeddings)
    return vectorstore

# Streamlit UI
st.title("PersonaPilot-Chat: Document Complexity Analyzer")

if "options" not in st.session_state:
    st.session_state['options'] = None

if "pdf_content" not in st.session_state:
    st.session_state['pdf_content'] = None

if "should_proceed" not in st.session_state:
    st.session_state.should_proceed = False

if "should_proceed_again" not in st.session_state:
    st.session_state.should_proceed_again = False

if "selected_option" not in st.session_state:
    st.session_state.selected_option = None

if "vectorstore" not in st.session_state:
    st.session_state["vectorstore"] = get_vectorstore()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "Assistant", "content": "Please enter your requirements."})

def get_response_from_chatgpt(persona: str, document: str = st.session_state["pdf_content"]) -> str:
    SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")
    # Chatbot interaction with OpenAI
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"{SYSTEM_PROMPT}"},
            {"role": "user", "content": f"PERSONA: ```{persona}```\n\nDOCUMENT:```{document}```"}
        ],
        max_tokens=500
    )
    return chat_completion.choices[0].message.content
    # import time
    # time.sleep(2)
    # return f"lol{randint(0,230)}"

def get_matching_personas(requirements):
    similar_response = st.session_state["vectorstore"].similarity_search(requirements, k=3)
    matcing_personas = [doc.page_content for doc in similar_response]
    return matcing_personas

def enable_flow():
    st.session_state.should_proceed_again = True

# Create a sidebar
with st.sidebar:
    if "pdf_content" not in st.session_state:
        st.session_state["pdf_content"] = ""
    # User input for document and testing requirements
    document_type = st.radio("Select Document Type:", ["Text", "PDF"])
    if document_type == "Text":
        st.session_state["pdf_content"] = st.text_area("Paste your document here:")
    else:
        pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])
        if document_type == "PDF" and pdf_file is not None:
            pdf_content = {}
            pdf_data = pdf_file.read()
            pdf_doc = fitz.open(stream=pdf_data, filetype="pdf")
            for page_num in range(pdf_doc.page_count):
                page = pdf_doc[page_num]
                text = page.get_text("text")
                pdf_content[f"Page {page_num + 1}"] = text.encode("utf-8")
            st.session_state["pdf_content"] = ""
            for key, value in pdf_content.items():

                st.session_state["pdf_content"] += str(value)

    # st.info(st.session_state.messages)
    # st.warning(st.session_state.selected_option)

if st.session_state['pdf_content']:
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    # React to user input
    if prompt := st.chat_input("Enter requirements here."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.should_proceed = True

    if st.session_state.should_proceed:
        if not st.session_state['options']:
            st.session_state['options'] = get_matching_personas(prompt)
        with st.chat_message("assistant"):
            st.session_state['selected_option'] = st.radio("Select an option:", st.session_state['options'], index=None, on_change=enable_flow)
            # st.info(st.session_state.selected_option)

    if st.session_state.should_proceed_again:
        # Display assistant message with selected option and options as bullet points
        assistant_message = f"You were presented with these options:\n"
        for option in st.session_state['options']:
            assistant_message += f"- {option}\n"

        assistant_message += f"\n\nAnd you selected: **{st.session_state.selected_option}**"

        st.chat_message("assistant").markdown(assistant_message)

        # Bot responds to user's choice
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})

        # Bot generates response using GPT-3
        response = get_response_from_chatgpt(persona=st.session_state.selected_option)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
            st.session_state.should_proceed = False
            st.session_state.should_proceed_again = False
            st.session_state.selected_option = None
            st.session_state.options = None
else:
    st.info("Please add a document/content to be analyzed first.")