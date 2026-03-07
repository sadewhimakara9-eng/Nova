import streamlit as st
from groq import Groq
from PIL import Image
from mcstatus import JavaServer

# 1. Page Config
st.set_page_config(page_title="Nova Ultra Max", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

# 2. Groq API Key
client = Groq(api_key="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")

# 3. CSS - Black Theme
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    h1, h2, h3, p, span, div, label, .stMarkdown { color: #ffffff !important; }
    .stChatMessage { background-color: #1a1a1a !important; border-radius: 12px; border: 1px solid #333333; margin-bottom: 10px; }
    section[data-testid="stSidebar"] { background-color: #111111 !important; border-right: 1px solid #333333; }
    .stChatInputContainer input { color: white !important; }
    /* Button එක පේන විදිහ හදමු */
    .stButton>button { background-color: #ffffff; color: #000000; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR
with st.sidebar:
    st.title("🚀 Nova Tools")
    mode = st.radio("Tool එක තෝරන්න:", ["💬 Smart Chat", "🖼️ Image Vision", "🎵 Music Studio", "🎮 Minecraft Monitor"])

# 5. MAIN LOGIC
if mode == "💬 Smart Chat":
    st.title("🤖 Nova Smart Chat")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "හලෝ! මම Nova. මොනවද වෙන්න ඕනේ?"}]
    for message in st.session_state.messages:
        with st.chat_message(message["role"]): st.markdown(message["content"])
    if prompt := st.chat_input("Nova ගෙන් අහන්න..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                comp = client.chat.completions.create(
                    messages=[{"role": "system", "content": "You are Nova, an advanced assistant."}, *st.session_state.messages],
                    model="llama-3.3-70b-versatile",
                )
                res = comp.choices[0].message.content
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            except Exception as e: st.error(f"Error: {e}")

elif mode == "🖼️ Image Vision":
    st.title("🖼️ Image Vision")
    up = st.file_uploader("Image එකක් අප්ලෝඩ් කරන්න", type=["jpg", "png"])
    if up:
        st.image(Image.open(up), use_container_width=True)
        st.info("Nova පින්තූරය කියවීමට සූදානම්.")

elif mode == "🎵 Music Studio":
    st.title("🎵 Music Studio")
    if st.button("Generate Music Track"):
        st.success("ට්‍රැක් එක සාර්ථකව හැදුණා!")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

elif mode == "🎮 Minecraft Monitor":
    st.title("🎮 Minecraft Monitor")
    # මෙතනදී IP එකයි Port එකයි දෙකම ගහන්න පුළුවන් (e.g. 185.207.166.145:19008)
    server_address = st.text_input("Server IP & Port එක දෙන්න:", value="185.207.166.145:19008")
    
    if st.button("Check Now"):
        with st.spinner("සර්වර් එක පරීක්ෂා කරයි..."):
            try:
                # IP එකයි Port එකයි වෙන් කරලා ගන්නවා
                server = JavaServer.lookup(server_address)
                status = server.status()
                st.success(f"Server Online! 🟢")
                st.metric("Players Online", f"{status.players.online} / {status.players.max}")
                st.metric("Ping (Latency)", f"{int(status.latency)} ms")
                st.write(f"**Version:** {status.version.name}")
            except Exception as e:
                st.error("Server එක Offline හෝ IP/Port එක වැරදියි. 🔴")
                st.info("සර්වර් එක Java ද කියලා ෂුවර් කරගන්න. Bedrock සර්වර් නම් මේ ලයිබ්‍රරි එක වෙනස් වෙන්න ඕනේ.")
