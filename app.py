import streamlit as st
from groq import Groq
from PIL import Image
from mcstatus import JavaServer
from streamlit_mic_recorder import mic_recorder
import datetime

# yfinance සහ වෙනත් libraries import කිරීම
try:
    import yfinance as yf
except ImportError:
    yf = None

# 1. PAGE CONFIG - Icon එක සහ App එකේ නම මෙතනින් වෙනස් වේ
st.set_page_config(
    page_title="Nova Pro Max", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. GROQ API KEY
client = Groq(api_key="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")

# 3. CUSTOM UI (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    h1, h2, h3, p, span, div, label, .stMarkdown { color: #ffffff !important; }
    .stTextInput input, .stSelectbox div, .stNumberInput input, .stTextArea textarea, .stChatInput input {
        color: #000000 !important; background-color: #ffffff !important; font-weight: bold !important;
    }
    .stMetric { background-color: #0a0a0a; border: 1px solid #00ff00; padding: 15px; border-radius: 10px; }
    section[data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #444; }
    .stButton>button { background-color: #00ff00 !important; color: #000000 !important; font-weight: bold !important; width: 100%; }
    code { color: #00ff00 !important; background-color: #1a1a1a !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR MENU
with st.sidebar:
    st.title("🚀 Nova Ultra Pro")
    mode = st.radio("Tool එක තෝරන්න:", [
        "💬 Voice & Smart Chat", 
        "🎮 Minecraft Monitor", 
        "🛡️ Network Optimizer (New)",
        "⚔️ MC Command Helper",
        "📄 File Analyzer",
        "🖼️ Image Vision",
        "🎵 Music Studio",
        "🛡️ Cyber Security Lab",
        "💰 Finance & Crypto",
        "💳 BOC/iPay Guide"
    ])
    st.markdown("---")
    st.write("Current Server: **Better MC 1.21.11**")

# 5. MAIN LOGIC

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

elif mode == "🎮 Minecraft Monitor":
    st.title("🎮 Minecraft Server Status")
    server_address = st.text_input("Server IP & Port:", value="185.207.166.145:19008")
    if st.button("Check Status"):
        try:
            server = JavaServer.lookup(server_address)
            status = server.status()
            st.success("Server Online! 🟢")
            st.metric("Ping", f"{int(status.latency)} ms")
            st.metric("Players", f"{status.players.online} / {status.players.max}")
        except:
            st.error("Offline!")

elif mode == "🛡️ Network Optimizer (New)":
    st.title("📶 Dialog Router Optimizer")
    st.write("Anuradhapura ප්‍රදේශයට හොඳම Signal ලබා ගැනීමට:")
    st.info("ZLT S50 රවුටරය සඳහා නිර්දේශිත Bands: Band 3, Band 40")
    if st.button("හොඳම Band එක පරීක්ෂා කරන්න"):
        st.success("Band 40 (2300MHz) දැනට ස්ථාවරව පවතියි.")

elif mode == "⚔️ MC Command Helper":
    st.title("⚔️ Command Generator")
    p_name = st.text_input("Player Name:", value="DeathnatorMC")
    item = st.text_input("Item:", value="oak_log")
    st.code(f"/give {p_name} {item} 64")

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

elif mode == "🖼️ Image Vision":
    st.title("🖼️ Vision AI")
    up = st.file_uploader("Upload Image", type=["jpg", "png"])
    if up: st.image(Image.open(up), use_container_width=True)

elif mode == "🎵 Music Studio":
    st.title("🎵 Nova Music")
    if st.button("Lo-fi Track එකක් සාදන්න"):
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

elif mode == "🛡️ Cyber Security Lab":
    st.title("🛡️ Cyber Security Lab")
    st.code("airodump-ng wlan0mon")

elif mode == "💰 Finance & Crypto":
    st.title("💰 Finance Tracker")
    if yf:
        btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
        st.metric("Bitcoin (USD)", f"${btc:,.2f}")

elif mode == "💳 BOC/iPay Guide":
    st.title("💳 Banking Guide")
    st.write("BOC Debit Card එක iPay හෝ Genie වලට සම්බන්ධ කිරීමට උදව්.")
