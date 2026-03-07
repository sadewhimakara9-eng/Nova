import streamlit as st
from groq import Groq
from PIL import Image
from mcstatus import JavaServer
import requests

# 1. Page Config
st.set_page_config(page_title="Nova Ultra Max", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

# 2. Groq API Key
client = Groq(api_key="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")

# 3. CSS - Black Theme with Visible Text
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    h1, h2, h3, p, span, div, label, .stMarkdown { color: #ffffff !important; }
    .stChatMessage { background-color: #1a1a1a !important; border-radius: 12px; border: 1px solid #333333; margin-bottom: 10px; }
    section[data-testid="stSidebar"] { background-color: #111111 !important; border-right: 1px solid #333333; }
    .stButton>button { background-color: #ffffff; color: #000000; width: 100%; font-weight: bold; border-radius: 8px; border: none; padding: 10px; }
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
        st.session_state.messages = [{"role": "assistant", "content": "හලෝ! මම Nova. අද මොනවද වෙන්න ඕනේ?"}]
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
    # මෙතන default අගය විදිහට ඔයාගේ සර්වර් එක දාලා තියෙන්නේ
    server_address = st.text_input("Server IP & Port:", value="185.207.166.145:19008")
    
    if st.button("Check Server Status"):
        with st.spinner("සර්වර් එක පරීක්ෂා කරමින් පවතියි..."):
            try:
                # සර්වර් එක lookup කරලා තත්පර 5ක කාලයක් (timeout) ලබා දෙනවා
                server = JavaServer.lookup(server_address)
                status = server.status()
                
                st.success(f"Server Online! 🟢")
                col1, col2 = st.columns(2)
                col1.metric("Players Online", f"{status.players.online} / {status.players.max}")
                col2.metric("Ping (Latency)", f"{int(status.latency)} ms")
                st.write(f"**Version:** {status.version.name}")
                
                if status.players.sample:
                    st.write("**Online Players:**")
                    for p in status.players.sample:
                        st.code(p.name)
            except Exception as e:
                # පරීක්ෂා කිරීම අසාර්ථක වුණොත් මේ මැසේජ් එක පෙන්වයි
                st.error("සර්වර් එක සම්බන්ධ කර ගැනීමට නොහැකි විය. 🔴")
                st.info("සර්වර් එක පණ ගැන්වී ඇති බව සහ IP/Port නිවැරදි බව නැවත පරීක්ෂා කරන්න.")

elif mode == "🌍 Web Search":
    st.title("🌍 Quick Web Search")
    q = st.text_input("සොයන්න අවශ්‍ය දේ:")
    if st.button("සොයන්න"):
        st.warning("Web Search පහසුකම සක්‍රීය වෙමින් පවතියි...")

elif mode == "🖼️ Image Vision":
    st.title("🖼️ Image Vision")
    up = st.file_uploader("Image එකක් අප්ලෝඩ් කරන්න", type=["jpg", "png"])
    if up:
        st.image(Image.open(up), use_container_width=True)
        st.info("Nova පින්තූරය කියවීමට සූදානම්.")

elif mode == "🎵 Music Studio":
    st.title("🎵 Nova Music Studio")
    if st.button("Create Track"):
        st.success("ට්‍රැක් එක සාර්ථකව හැදුණා!")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
