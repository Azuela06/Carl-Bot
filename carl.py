#imports to use llama and streamlit since it's not a built in function in python
import streamlit as st
import ollama

st.title("Carl Bot")  #Name of the bot

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi! How can I help you?"}]

# write the chat history

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message(msg["role"], avatar="🐻‍❄️").write(msg["content"])
    else:
        st.chat_message(msg["role"], avatar="🤖").write(msg["content"]) 

# Creating bot's response using llama

#defining a function that will we call later

def generateResponse():
    response = ollama.chat(model='llama2:latest', stream = True, messages=st.session_state.messages) #history of the convo
    for partialResponse in response:
        token = partialResponse["message"]["content"]
        st.session_state["full_message"] += token       #session state (when chatting)
        yield token  #yield instead of return so chat will be continuous

#what you will see in the UI or user-end interface
if prompt := st.chat_input():
    st.session_state.messages.append({"role" : "user", "content" : prompt})
    st.chat_message("user", avatar="🐻‍❄️").write(prompt)
    st.session_state["full_message"] = ""
    st.chat_message("assistant", avatar="🤖").write_stream(generateResponse)   #calling the function that will generate the bot's response
    st.session_state.messages.append({"role": "assistant", "content" : st.session_state["full_message"]})