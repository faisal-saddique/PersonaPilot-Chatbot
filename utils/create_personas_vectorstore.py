from langchain.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Constants
OVERWRITE_EXISTING = False
VECTORSTORE_NAME = os.getenv('VECTORSTORE_NAME')

def convert_personas_to_docs(personas_list: list):
    docs = []
    for persona in personas_list:
        # Print persona information
        print(f"Processing persona: {persona['name']}")
        
        # Append Document to docs
        docs.append(Document(page_content=str(persona['description']),
                             metadata={key: value for key, value in persona.items() if key != 'description'}))
    
    return docs

with open("personas.json", "r") as file:
    personas = json.load(file)['personas']

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings()

# Convert personas to Document objects
final_docs = convert_personas_to_docs(personas_list=personas)

# Print the number of personas processed
print(f"Number of personas processed: {len(final_docs)}")

# Try to load existing vectorstore; create a new one if it doesn't exist
try:
    existing_vectorstore = FAISS.load_local(VECTORSTORE_NAME, embeddings=embeddings)
    vectorstore = existing_vectorstore
    print("Loaded existing vectorstore.")
except RuntimeError:
    # Vectorstore does not exist, create a new one from documents and embeddings
    vectorstore = FAISS.from_documents(documents=final_docs, embedding=embeddings)
    print("Created a new vectorstore.")

# Optionally overwrite existing vectorstore by merging with a new one
if OVERWRITE_EXISTING:
    new_vectorstore = FAISS.from_documents(documents=final_docs, embedding=embeddings)
    vectorstore.merge_from(new_vectorstore)
    print("Merged with a new vectorstore.")

# Save the resulting vectorstore locally
vectorstore.save_local(VECTORSTORE_NAME)
print(f"Vectorstore saved locally as {VECTORSTORE_NAME}.")
