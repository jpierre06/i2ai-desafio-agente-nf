import os
import streamlit as st
from core.question import run_csv_question_chain
from core.data_loader import load_dataframes_from_folders
from core.logger import save_chat_log
import core.zip_processor as zp

# Configurações do Streamlit
with st.sidebar:  
    api_key = st.text_input("Gemini API Key", key="chatbot_api_key", type="password")
    "[Get an Gemini API key](https://aistudio.google.com/app/apikey)"
    save_history = st.checkbox("Salvar log do histórico da conversa", value=False)
    

st.title("💬 Chatbot")
st.caption("🚀 Dados de Notas Fiscais - Disponibilizado pelo TCU")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Faça sua pergunta?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Digite sua pergunta sobre os dados..."):
    if not api_key:
        st.info("Por favor adicione sua Gemini API key pra continuar.")
        st.stop()
    
    os.environ["GOOGLE_API_KEY"] = api_key

    # Verifica a existência de novos arquivos ZIP para processar
    zp.process_zip_files()
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    with st.spinner("🔍 Analisando sua pergunta e consultando os dados..."):

        data = load_dataframes_from_folders()

        if isinstance(data, str):  # erro ao carregar
            st.session_state.messages.append({"role": "assistant", "content": f"❌ {data}"})
            st.chat_message("assistant").write(f"❌ {data}")
            st.stop()

        code = ""

        try:
            msg, code = run_csv_question_chain(
                prompt, 
                {"heads": data["heads"], "items": data["items"]}, 
                api_key=api_key
            )
        except Exception as e:
            msg = f"⚠️ Ocorreu um erro ao processar sua pergunta: {str(e)}"
            code = "Error."

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

    if save_history:
        save_chat_log(prompt, msg, code)