import streamlit as st
from groq import Groq
from PIL import Image
from mcstatus import JavaServer
from streamlit_mic_recorder import mic_recorder

# 1. PAGE CONFIG (අයිකනය සහ නම මෙතනින්)
st.set_page_config(page_title="Nova Pro Max", page_icon="🤖", layout="wide")

# 2. API & STYLING
client = Groq(api_key="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")
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    h1, h2, h3, p, span, label { color: #ffffff !important; }
    .stTextInput input, .stChatInput input { color: #000000 !important; background-color: #ffffff !important; font-weight: bold; }
    .stButton>button { background-color: #00ff00 !important; color: #000000 !important; font-weight: bold; width: 100%; }
    code { color: #00ff00 !important; background-color: #1a1a1a !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR
with st.sidebar:
    st.title("🚀 Nova Pro")
    mode = st.radio("Tools:", ["💬 Chat", "🎮 MC Monitor", "⚔️ Commands", "🛡️ Network", "💳 BOC Guide"])
    st.write("---")
    st.write("Server: Better MC 1.21.11")

# 4. TOOLS LOGIC
if mode == "💬 Chat":
    st.title("🎤 Nova Voice & Chat")
    mic_recorder(start_prompt="Speak", stop_prompt="Stop", key='recorder')
    if prompt := st.chat_input("Ask Nova..."):
        with st.chat_message("assistant"):
            res = client.chat.completions.create(messages=[{"role":"user","content":prompt}], model="llama-3.3-70b-versatile")
            st.write(res.choices[0].message.content)

elif mode == "🎮 MC Monitor":
    st.title("🎮 Server Status")
    if st.button("Check 185.207.166.145:19008"):
        try:
            status = JavaServer.lookup("185.207.166.145:19008").status()
            st.success(f"Online: {status.players.online}/{status.players.max}")
        except: st.error("Offline")

elif mode == "⚔️ Commands":
    st.title("⚔️ Command Gen")
    p = st.text_input("Player:", value="DeathnatorMC")
    i = st.text_input("Item:", value="oak_log")
    st.code(f"/give {p} {i} 64")

elif mode == "🛡️ Network":
    st.title("📶 Network Optimizer")
    st.info("ZLT S50: Band 40 is recommended for Anuradhapura.")

elif mode == "💳 BOC Guide":
    st.title("💳 Banking Help")
    st.write("BOC Debit Card එක iPay/Genie වලට Link කරන හැටි මෙතනින් බලන්න.")
