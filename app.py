import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import fitz  # PyMuPDF

# Load environment variables
load_dotenv()

# OpenAI initialization
client = OpenAI()

# Set page configuration with an icon
st.set_page_config(page_title="PersonaPilot-Chat", page_icon="🚀")

# Streamlit UI
st.title("PersonaPilot-Chat: Document Complexity Analyzer")

# User input for document and testing requirements
document_type = st.radio("Select Document Type:", ["Text", "PDF"])
if document_type == "Text":
    document = st.text_area("Paste your document here:")
else:
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

testing_requirements = st.text_input("Enter testing requirements:")

# Button to trigger analysis
if st.button("Analyze Document"):
    # Extract text from the uploaded PDF
    if document_type == "PDF" and pdf_file is not None:
        pdf_content = {}
        pdf_data = pdf_file.read()
        pdf_doc = fitz.open(stream=pdf_data, filetype="pdf")
        for page_num in range(pdf_doc.page_count):
            page = pdf_doc[page_num]
            text = page.get_text("text")
            pdf_content[f"Page {page_num + 1}"] = text.encode("utf-8")

        # Now pdf_content is a dictionary with page numbers as keys and text as values
        # for page_num, text in pdf_content.items():
        #     st.write(f"Page {page_num}:\n{text.decode('utf-8')}")



    # Chatbot interaction with OpenAI
    # chat_completion = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant."},
    #         {"role": "user", "content": f"How are you?"}
    #     ]
    # )

    # Display results
    st.subheader("Analysis Results:")
    st.write(pdf_content)
    # st.write(chat_completion["choices"][0]["message"]["content"])
