import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

# Configuración Visual
st.set_page_config(page_title="AI Orchestrator", layout="wide")
st.title("🕹️ Mi Centro de Control IA")

# 1. Conexión segura con la llave que guardaste (luego te digo dónde ponerla)
mi_llave = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=mi_llave)

# 2. Definición de tus Apps de AI Studio
APPS = {
    "EchoWise": "Eres EchoWise. Tu especialidad es analizar audio y transcribir con inteligencia emocional.",
    "Vocesia Studio": "Eres Vocesia Studio. Creas guiones narrativos y estructuras de voz profesionales.",
    "Infolibro GenAI": "Eres Infolibro GenAI. Resumes libros y extraes sabiduría de documentos de forma estructurada."
}

# Selector de App
seleccion = st.pills("Selecciona la App que quieres usar:", list(APPS.keys()), default="EchoWise")
st.markdown(f"### Estás controlando: **{seleccion}**")

# Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- CONTROLES: VOZ Y TEXTO ---
col1, col2 = st.columns([1, 4])
with col1:
    audio_data = mic_recorder(start_prompt="🎙️ Hablar", stop_prompt="🛑 Parar", key='recorder')

if prompt := st.chat_input("Escribe tu orden aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    # Respuesta de la IA
    with st.chat_message("assistant"):
        model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=APPS[seleccion])
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

# Si usaste la voz
if audio_data:
    with st.chat_message("assistant"):
        model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=APPS[seleccion])
        response = model.generate_content([
            "Ejecuta esta orden de voz según tu especialidad:",
            {"mime_type": "audio/wav", "data": audio_data['bytes']}
        ])
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
