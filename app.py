import streamlit as st
from groq import Groq
from PIL import Image
from mcstatus import JavaServer
import datetime

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
    .stButton>button { background-color: #ffffff; color: #000000; width: 100%; font-weight: bold; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR
with st.sidebar:
    st.title("🚀 Nova Multi-Tools")
    mode = st.radio("Tool එක තෝරන්න:", [
        "💬 Smart Chat", 
        "🎮 Minecraft Monitor", 
        "⚔️ MC Command Helper",
        "🖼️ Image Vision", 
        "🎵 Music Studio",
        "📊 System Info"
    ])
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
                messages=[{"role": "system", "content": "You are Nova, an advanced assistant."}, *st.session_state.messages],
                model="llama-3.3-70b-versatile",
            )
            res = comp.choices[0].message.content
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

elif mode == "🎮 Minecraft Monitor":
    st.title("🎮 Server Status")
    server_address = st.text_input("Server IP & Port:", value="185.207.166.145:19008")
    if st.button("Check Now"):
        try:
            server = JavaServer.lookup(server_address)
            status = server.status()
            st.success("Server Online! 🟢")
            st.metric("Players", f"{status.players.online} / {status.players.max}")
            st.metric("Ping", f"{int(status.latency)} ms")
        except:
            st.error("Server Offline! 🔴")

elif mode == "⚔️ MC Command Helper":
    st.title("⚔️ MC Command Helper")
    st.write("සර්වර් එකේ වැඩ වලට ඕන කමාන්ඩ් ඉක්මනින් හදාගන්න.")
    cmd_type = st.selectbox("Command වර්ගය:", ["Give Item", "Teleport", "GameMode", "Clear Inventory"])
    player_name = st.text_input("Player ගේ නම:", value="DeathnatorMC")
    
    if cmd_type == "Give Item":
        item = st.text_input("Item එක (e.g. diamond_sword):", value="oak_log")
        amount = st.number_input("ප්‍රමාණය:", min_value=1, value=64)
        st.code(f"/give {player_name} {item} {amount}")
    elif cmd_type == "Teleport":
        coords = st.text_input("Coordinates (x y z):", value="0 64 0")
        st.code(f"/tp {player_name} {coords}")

elif mode == "🖼️ Image Vision":
    st.title("🖼️ Image Vision")
    up = st.file_uploader("පින්තූරයක් අප්ලෝඩ් කරන්න", type=["jpg", "png"])
    if up:
        st.image(Image.open(up), use_container_width=True)
        st.info("Nova පින්තූරය කියවීමට සූදානම්.")

elif mode == "🎵 Music Studio":
    st.title("🎵 Music Studio")
    if st.button("Create Track"):
        st.success("ට්‍රැක් එක සාර්ථකව නිර්මාණය විය! (30s)")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

elif mode == "📊 System Info":
    st.title("📊 Nova System Info")
    st.write(f"**අද දිනය:** {datetime.date.today()}")
    st.write(f"**වේලාව:** {datetime.datetime.now().strftime('%H:%M:%S')}")
    st.write("**Model:** Llama 3.3 (Groq API)")
    st.write("**Region:** Colombo, Sri Lanka")
