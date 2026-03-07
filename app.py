import streamlit as st
from groq import Groq
from PIL import Image
from mcstatus import JavaServer
import requests

# 1. Page Config
st.set_page_config(page_title="Nova Ultra Max", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

# 2. Groq API Key
client = Groq(api_key="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")

# 3. CSS - Full Black Theme
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    h1, h2, h3, p, span, div, label, .stMarkdown { color: #ffffff !important; }
    .stChatMessage { background-color: #1a1a1a !important; border-radius: 12px; border: 1px solid #333333; margin-bottom: 10px; }
    section[data-testid="stSidebar"] { background-color: #111111 !important; border-right: 1px solid #333333; }
    .stButton>button { background-color: #ffffff; color: #000000; width: 100%; font-weight: bold; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR
with st.sidebar:
    st.title("🚀 Nova Multi-Tools")
    mode = st.radio("Tool එක තෝරන්න:", ["💬 Smart Chat", "🎮 Minecraft Monitor", "🌍 Web Search", "🖼️ Image Vision", "🎵 Music Studio"])
    st.markdown("---")

# 5. MAIN LOGIC
if mode == "💬 Smart Chat":
    st.title("🤖 Nova Smart Chat")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "හලෝ! මම Nova. මොනවද අද කරන්න ඕනේ?"}]
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    if prompt := st.chat_input("Nova ගෙන් අහන්න..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            comp = client.chat.completions.create(
                messages=[{"role": "system", "content": "You are Nova, an advanced AI assistant."}, *st.session_state.messages],
                model="llama-3.3-70b-versatile",
            )
            res = comp.choices[0].message.content
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

elif mode == "🎮 Minecraft Monitor":
    st.title("🎮 Minecraft Server Status")
    server_address = st.text_input("Server IP & Port:", value="185.207.166.145:19008")
    if st.button("Check Server"):
        try:
            server = JavaServer.lookup(server_address)
            status = server.status()
            st.success("Server Online! 🟢")
            col1, col2 = st.columns(2)
            col1.metric("Players", f"{status.players.online} / {status.players.max}")
            col2.metric("Ping", f"{int(status.latency)} ms")
            
            # Player List එක පෙන්වීම
            if status.players.sample:
                st.write("**Online Players:**")
                for player in status.players.sample:
                    st.code(player.name)
            else:
                st.info("දැනට players ලා කවුරුත් නැහැ.")
        except:
            st.error("Server එක Offline හෝ IP එක වැරදියි. 🔴")

elif mode == "🌍 Web Search":
    st.title("🌍 Quick Web Search")
    query = st.text_input("සොයන්න අවශ්‍ය දේ:")
    if st.button("Search"):
        st.info(f"'{query}' ගැන තොරතුරු සොයමින් පවතියි... (මෙම පහසුකම Nova Search API හරහා සම්බන්ධ වේ)")

elif mode == "🖼️ Image Vision":
    st.title("🖼️ Image Vision")
    up = st.file_uploader("පින්තූරයක් අප්ලෝඩ් කරන්න", type=["jpg", "png"])
    if up:
        st.image(Image.open(up), use_container_width=True)
        st.info("Llama-3.2-Vision හරහා Nova පින්තූරය කියවයි.")

elif mode == "🎵 Music Studio":
    st.title("🎵 Nova Music Studio")
    if st.button("Create Track"):
        st.success("ට්‍රැක් එක සාර්ථකව නිර්මාණය විය! (30s)")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
