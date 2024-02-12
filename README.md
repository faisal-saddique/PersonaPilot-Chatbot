# PersonaPilot-Chat: Document Complexity Analyzer

Welcome to PersonaPilot-Chat, a Streamlit-based application that utilizes OpenAI's GPT-3.5-turbo model to analyze document complexity based on user requirements and document content. This document provides essential information on setting up, running, and understanding the PersonaPilot-Chat application.

## Overview

PersonaPilot-Chat is designed to assist users in analyzing document complexity by interacting with OpenAI's GPT-3.5-turbo model. Users can provide specific requirements and document content, and the application will generate a response tailored to the user's input.

## Getting Started

### Prerequisites

Before running the PersonaPilot-Chat application, make sure you have the following:

- Python (3.6 or higher)
- Streamlit
- OpenAI Python SDK
- PyMuPDF (for handling PDF files)
- LangChain (specifically, vectorstores.faiss and langchain_openai)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/faisal-saddique/PersonaPilot-Chatbot.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:

   - Create a `.env` file in the project root.
   - Define the following variables in the `.env` file:
     - `OPENAI_API_KEY`: Your OpenAI API key.
     - `VECTORSTORE_NAME`: Name of the vector store for document matching.
     - `SYSTEM_PROMPT`: System prompt for GPT-3.5-turbo.

### Running the Application

Run the following command to start the PersonaPilot-Chat application:

```bash
streamlit run app.py
```

Visit the provided URL in your web browser to access the application.

## Usage

1. **Select Document Type:**
   - Choose between "Text" or "PDF" for document input.

2. **Input Document Content:**
   - Paste text or upload a PDF file.

3. **Enter Requirements:**
   - Enter specific requirements in the chat input.

4. **Select Matching Persona:**
   - The application identifies matching personas based on requirements and displays them.

5. **Choose an Option:**
   - Select an option from the displayed personas.

6. **View Analysis:**
   - The application provides an analysis of the selected persona and generates responses using GPT-3.5-turbo.

## Additional Information

- The application uses a vector store for document matching, which can be configured by modifying the `VECTORSTORE_NAME` environment variable.

## Contributing

Feel free to contribute to PersonaPilot-Chat by submitting issues, feature requests, or pull requests. Your contributions are highly appreciated!