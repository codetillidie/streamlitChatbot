import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

# App title and configuration
st.set_page_config(page_title="🤗💬 streamlitChatbot")

# Sidebar for Hugging Face credentials
with st.sidebar:
    st.title('🤗💬 streamlitChatbot')
    
    hf_email = st.text_input('Enter E-mail:', type='password')
    hf_pass = st.text_input('Enter password:', type='password')
    if not (hf_email and hf_pass):
        st.warning('Please enter your credentials!', icon='⚠️')
    else:
        st.success('Proceed to entering your prompt message!', icon='👉')
    
    st.markdown('📖 Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/)!')
    
# Initialize session state for storing chat messages
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Display chat messages from the session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function to generate a response from the Hugging Face model
def generate_response(prompt_input, email, passwd):
    try:
        sign = Login(email, passwd)
        cookies = sign.login()
        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
        return chatbot.chat(prompt_input)
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return "There was an error processing your request."

# Get user prompt and display it in the chat
if prompt := st.chat_input(disabled=not (hf_email and hf_pass)):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate and display a response if the last message is from the user
if st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt, hf_email, hf_pass)
            st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
