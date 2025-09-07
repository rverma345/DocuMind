import streamlit as st

st.set_page_config(page_title= "🧠 DocuMind: Universal Document Intelligence Chatbot",layout='wide')
st.title("🧠 DocuMind: Universal Document Intelligence Chatbot")

#initializing session state variables
if 'messages' not in st.session_state:
    st.session_state.messages=[]
if 'vector_store' not in st.session_state:
    st.session_state.vector_store= None

with st.sidebar:
    st.header('Upload Your Documents here')
    pdf_docs=st.file_uploader(
        "Upload your Pdfs here  and click on 'Process'",
        accept_multiple_files=True
    )
    if st.button('Process'):
        with st.spinner('Processing Documents'):
            # placeholder for document ingestion process
            st.success("Documents processed successfully!")

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask a question about your documents or the web..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # This is where you'll call the main logic function (Step 5)
    # response = generate_response(prompt)
    with st.chat_message("assistant"):
        # Display assistant response
        # st.markdown(response)
        pass # Placeholder for now
    