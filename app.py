import streamlit as st
from src.helper import get_pdf_text, get_text_chunk, get_vector_store, get_conversational_chain

def user_input(user_question):
    if st.session_state.conversation is None:
        st.error("Please upload and process a PDF document first.")
        return

    response = st.session_state.conversation({'question': user_question})
    st.session_state.chatHistory = response['chat_history']
    for i, message in enumerate(st.session_state.chatHistory):
        if i % 2 == 0:
            st.write("User: ", message.content)
        else:
            st.write("DocuChat: ", message.content)

def main():
    st.set_page_config("Information Retrieval System")
    st.header("DocuChat: :blue[Chat with Your Documents] 💁")  
    st.subheader(':blue-background[:green[_Turn static PDFs into interactive knowledge_]]')
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chatHistory" not in st.session_state:
        st.session_state.chatHistory = None
    
    with st.sidebar:
        st.title("Menu")
        pdf_docs = st.file_uploader(":orange[Upload your PDF files and click the Submit and Process button.]",
                                    accept_multiple_files=True) 
        if st.button("Submit & Process"):
            with st.spinner("Processing...."):
                raw_data = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunk(raw_data)
                vector_store = get_vector_store(text_chunks)
                st.session_state.conversation = get_conversational_chain(vector_store)
                st.success("Done")

    user_question = st.text_input(":red[Ask questions about your PDF files:] :blue[Start Now!]")
    
    if user_question:
        if st.session_state.conversation is None:
            st.warning("Please upload and process a PDF document before asking questions.")
        else:
            user_input(user_question)

if __name__ == "__main__":
    main()