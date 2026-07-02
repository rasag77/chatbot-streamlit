import streamlit as st
from openai import OpenAI

st.set_page_config(layout="wide")

modelo = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

st.write("### ChatBot com IA")

if not "lista_mensagens" in st.session_state:
    st.session_state["lista_mensagens"] = []

# contêiner com altura fixa e scroll automático
chat_container = st.container(height=500)

with chat_container:
    for mensagem in st.session_state["lista_mensagens"]:
        role = mensagem["role"]
        content = mensagem["content"]
        st.chat_message(role).write(content)

mensagem_usuario = st.chat_input("Escreva sua mensagem aqui")

if mensagem_usuario:
    with chat_container:
        st.chat_message("user").write(mensagem_usuario)
    mensagem = {"role": "user", "content": mensagem_usuario}
    st.session_state["lista_mensagens"].append(mensagem)

    with st.spinner("Pensando..."):
        resposta_modelo = modelo.chat.completions.create(
            messages=st.session_state["lista_mensagens"],
            model="llama-3.3-70b-versatile"
        )
    resposta_ia = resposta_modelo.choices[0].message.content

    with chat_container:
        st.chat_message("assistant").write(resposta_ia)
    mensagem_ia = {"role": "assistant", "content": resposta_ia}
    st.session_state["lista_mensagens"].append(mensagem_ia)
    st.rerun()
