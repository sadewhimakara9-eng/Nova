import streamlit as st
from groq import Groq
from PIL import Image
from mcstatus import JavaServer
from streamlit_mic_recorder import mic_recorder

# 1. PAGE CONFIG - මෙතනින් තමයි Desktop Icon එක සහ App Name එක පාලනය වෙන්නේ
st.set_page_config(
    page_title="Nova Pro Max", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. GROQ API KEY
client = Groq(api_key="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")

# 3. CUSTOM UI (CSS) - Dark Theme එක සහ අකුරු පැහැදිලිව පේන්න හැදීම
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    h1, h2, h3, p, span, div, label, .stMarkdown { color: #ffffff !important; }
    
    /* Input Boxes වල ලියන අකුරු කළු පාටින් පැහැදිලිව පේන්න හැදීම */
    .stTextInput input, .stSelectbox div, .stNumberInput input, .stTextArea textarea, .stChatInput input {
        color: #000000 !important; 
        background-color: #ffffff !important;
        font-weight: bold !important;
    }
    
    .stMetric { background-color: #0a0a0a; border: 1px solid #00ff00; padding: 15px; border-radius: 10px; }
    section[data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #444; }
    .stButton>button { background-color: #00ff00 !important; color: #000000 !important; font-weight: bold !important; width: 100%; border-radius: 8px; }
    code { color: #00ff00 !important; background-color: #1a1a1a !important; padding: 5px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR MENU - සියලුම පරණ සහ අලුත් Tools මෙතන ඇත
with st.sidebar:
    st.title("🚀 Nova Ultra Pro")
    mode = st.radio("Tool එක තෝරන්න:", [
        "💬 Voice & Smart Chat", 
        "🎮 Minecraft Monitor", 
        "⚔️ MC Command Helper",
        "📄 File Analyzer",
        "🖼️ Image Vision",
        "🎵 Music Studio",
        "🛡️ Network Optimizer",
        "🛡️ Cyber Security Lab",
        "💳 BOC/iPay Guide"
    ])
    st.markdown("---")
    st.write("Current Server: **Better MC 1.21.11**")

# 5. MAIN LOGIC

# --- Chat & Voice ---
if mode == "💬 Voice & Smart Chat":
    st.title("🎤 Nova Voice & Chat")
    audio = mic_recorder(start_prompt="කතා කරන්න (Start)", stop_prompt="නැවතීමට (Stop)", key='recorder')
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "හලෝ මචං! මම Nova. අද මොනවද වෙන්න ඕනේ?"}]
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

# --- Minecraft Monitor ---
elif mode == "🎮 Minecraft Monitor":
    st.title("🎮 Server Live Status")
    server_addr = st.text_input("Server IP & Port:", value="185.207.166.145:19008")
    if st.button("Check Now"):
        try:
            server = JavaServer.lookup(server_addr)
            status = server.status()
            st.success("Server Online! 🟢")
            st.metric("Ping", f"{int(status.latency)} ms")
            st.metric("Players", f"{status.players.online} / {status.players.max}")
        except:
            st.error("Server Offline! 🔴")

# --- Command Helper ---
elif mode == "⚔️ MC Command Helper":
    st.title("⚔️ Command Generator")
    p_name = st.text_input("Player Name:", value="DeathnatorMC")
    item = st.text_input("Item:", value="oak_log")
    st.markdown("### Generated Command:")
    st.code(f"/give {p_name} {item} 64")

# --- Network Optimizer ---
elif mode == "🛡️ Network Optimizer":
    st.title("📶 Network Booster")
    st.write("Anuradhapura ප්‍රදේශය සඳහා නිර්දේශ:")
    st.info("ZLT S50 රවුටරය සඳහා Band 40 වඩාත් ස්ථාවරයි.")
    st.code("Cell ID Locking & Band Locking enabled for Dialog 4G")

# --- Image Vision ---
elif mode == "🖼️ Image Vision":
    st.title("🖼️ Vision AI")
    up = st.file_uploader("Upload Image", type=["jpg", "png"])
    if up: 
        st.image(Image.open(up), use_container_width=True)

# --- Music Studio ---
elif mode == "🎵 Music Studio":
    st.title("🎵 Nova Music Studio")
    if st.button("Generate 30s Lo-fi Track"):
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

# --- Banking Guide ---
elif mode == "💳 BOC/iPay Guide":
    st.title("💳 Banking Helper")
    st.write("BOC Debit Card එක iPay හෝ Genie වලට සම්බන්ධ කිරීමට උදව්.")

# --- File Analyzer ---
elif mode == "📄 File Analyzer":
    st.title("📄 File Analyzer")
    up = st.file_uploader("Text file එකක් දාන්න", type=["txt"])
    if up:
        content = up.read().decode("utf-8")
        q = st.text_input("ගොනුව ගැන අහන්න:")
        if st.button("Analyze"):
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": f"Context: {content}"}, {"role": "user", "content": q}],
                model="llama-3.3-70b-versatile",
            )
            st.info(res.choices[0].message.content)

# --- Cyber Security ---
elif mode == "🛡️ Cyber Security Lab":
    st.title("🛡️ Cyber Security Lab")
    st.code("airodump-ng wlan0mon")
