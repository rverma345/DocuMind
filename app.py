import streamlit as st
from ingestion import ingest_documents
from route import query_router
from search import searching_and_produce_output

st.set_page_config(page_title="🧠 DocuMind: Universal Document Intelligence Chatbot", layout='wide')
st.title("🧠 DocuMind: Universal Document Intelligence Chatbot")


if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None

# sidebar to upload documents
with st.sidebar:
    st.header('Upload Your Documents')
    pdf_docs = st.file_uploader(
        "Upload your PDFs here and click on 'Process'",
        accept_multiple_files=True
    )
    
    # The button to trigger the document ingestion process
    if st.button('Process'):
        if pdf_docs:
            with st.spinner('Processing Documents... This may take a moment.'):
                import os

                # Create folder for uploaded files
                os.makedirs("uploaded_pdfs", exist_ok=True)

                file_paths = []
                for pdf in pdf_docs:
                    file_path = os.path.join("uploaded_pdfs", pdf.name)
                    with open(file_path, "wb") as f:
                        f.write(pdf.read())  # Save file to disk
                    file_paths.append(file_path)

                # Now ingest using saved file paths
                st.session_state.vector_store = ingest_documents(file_paths)
                st.success("Documents processed successfully!")
        else:
            st.warning("Please upload at least one PDF file.")

# --- Chat History Display ---
# This loop iterates through the messages stored in the session state and displays them.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#User Input and Chat Logic 
if prompt := st.chat_input("Ask a question about your documents or the web..."):
    # Append the user's message to the session state and display it.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # This is the main logic block that generates the assistant's response.
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = ""
            
            # Checking if documents have been processed and a vector store exists.
            if st.session_state.vector_store is not None:
                response = searching_and_produce_output(prompt, st.session_state.vector_store)
            else:
                st.info("No documents uploaded. Performing a web search.")
                response = searching_and_produce_output(prompt, None)

            # Display the final response from the assistant.
            st.markdown(response)
            
            # Append the assistant's response to the session state for history.
            st.session_state.messages.append({"role": "assistant", "content": response})