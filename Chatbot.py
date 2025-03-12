from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
import os

def get_openai_api_key():
    load_dotenv()  # Carrega as variáveis do arquivo .env
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return openai_api_key
openai_api_key = get_openai_api_key()

st.title("🔧 Chat GPT - Suporte OC")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Como posso ajudar?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
