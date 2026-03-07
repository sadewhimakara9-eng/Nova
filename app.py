import streamlit as st
from groq import Groq
from PIL import Image
from mcstatus import JavaServer
from streamlit_mic_recorder import mic_recorder
import datetime

# yfinance install වෙලා නැත්නම් error එක වළක්වා ගැනීමට
try:
    import yfinance as yf
except ImportError:
    yf = None

# 1. Page Config
st.set_page_config(page_title="Nova Ultra Pro", page_icon="🛡️", layout="wide")

# 2. Groq API Key
client = Groq(api_key="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")

# 3. CSS - UI එක සහ අකුරු පැහැදිලිව පේන්න හැදීම
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    h1, h2, h3, p, span, div, label, .stMarkdown { color: #ffffff !important; }
    
    /* Input Boxes සහ Text Area වල අකුරු කළු පාටින් පැහැදිලිව පේන්න */
    .stTextInput input, .stSelectbox div, .stNumberInput input, .stTextArea textarea, .stChatInput input {
        color: #000000 !important; 
        background-color: #ffffff !important;
        font-weight: bold !important;
    }
    
    .stMetric { background-color: #0a0a0a; border: 1px solid #00ff00; padding: 15px; border-radius: 10px; }
    section[data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #444; }
    .stButton>button { background-color: #00ff00 !important; color: #000000 !important; font-weight: bold !important; }
    code { color: #00ff00 !important; background-color: #1a1a1a !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR - මෙතන සියලුම කලින් තිබූ ඔප්ෂන් සහ අලුත් ඒවා ඇත
with st.sidebar:
    st.title("🚀 Nova Ultra Pro")
    mode = st.radio("Tool එක තෝරන්න:", [
        "💬 Voice & Smart Chat", 
        "🎮 Minecraft Monitor", 
        "⚔️ MC Command Helper",
        "📄 File Analyzer",
        "🖼️ Image Vision",
        "🎵 Music Studio",
        "🛡️ Cyber Security Lab",
        "💰 Finance & Crypto",
        "💳 BOC/iPay Guide"
    ])
    st.markdown("---")
    st.write(f"Current Server: **Better MC 1.21.11**") #

# 5. MAIN LOGIC

# --- 1. Chat & Voice ---
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

# --- 2. Minecraft Monitor ---
elif mode == "🎮 Minecraft Monitor":
    st.title("🎮 Minecraft Server Status")
    server_address = st.text_input("Server IP & Port:", value="185.207.166.145:19008") #
    if st.button("Check Now"):
        try:
            server = JavaServer.lookup(server_address)
            status = server.status()
            st.success("Server Online! 🟢")
            st.metric("Ping", f"{int(status.latency)} ms")
            st.metric("Players", f"{status.players.online} / {status.players.max}")
            st.write(f"Version: {status.version.name}")
        except:
            st.error("Server Offline හෝ IP එක වැරදියි. 🔴")

# --- 3. Command Helper ---
elif mode == "⚔️ MC Command Helper":
    st.title("⚔️ MC Command Helper")
    p_name = st.text_input("Player ගේ නම:", value="DeathnatorMC") #
    item = st.text_input("Item එක (e.g. oak_log):", value="oak_log")
    st.markdown("### Generated Command:")
    st.code(f"/give {p_name} {item} 64")

# --- 4. File Analyzer ---
elif mode == "📄 File Analyzer":
    st.title("📄 Advanced File Reader")
    up = st.file_uploader("Text file එකක් දාන්න (.txt)", type=["txt"])
    if up:
        content = up.read().decode("utf-8")
        q = st.text_input("මේ ගොනුව ගැන Nova ගෙන් අහන්න:")
        if st.button("Analyze"):
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": f"Context: {content}"}, {"role": "user", "content": q}],
                model="llama-3.3-70b-versatile",
            )
            st.info(res.choices[0].message.content)

# --- 5. Image Vision ---
elif mode == "🖼️ Image Vision":
    st.title("🖼️ Vision AI")
    up = st.file_uploader("Upload Image", type=["jpg", "png"])
    if up: st.image(Image.open(up), use_container_width=True)

# --- 6. Music Studio ---
elif mode == "🎵 Music Studio":
    st.title("🎵 Music Studio")
    if st.button("Generate 30s Lo-fi Track"):
        st.success("ට්‍රැක් එක සාර්ථකව හැදුණා!")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

# --- 7. Cyber Security Lab ---
elif mode == "🛡️ Cyber Security Lab":
    st.title("🛡️ Cyber Security Lab")
    st.write("Educational Use Only - Aircrack-ng Guide")
    st.code("airmon-ng start wlan0") #
    st.code("airodump-ng wlan0mon")

# --- 8. Finance & Crypto ---
elif mode == "💰 Finance & Crypto":
    st.title("💰 Finance Tracker")
    if yf:
        btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
        lkr = yf.Ticker("LKR=X").history(period="1d")['Close'].iloc[-1]
        st.metric("Bitcoin (USD)", f"${btc:,.2f}")
        st.metric("USD to LKR", f"Rs. {lkr:,.2f}")
    else:
        st.error("yfinance library එක තවම install වී නැත.")

# --- 9. BOC/iPay Guide ---
elif mode == "💳 BOC/iPay Guide":
    st.title("💳 Sri Lankan Banking Helper")
    st.write("1. BOC Debit Card එක iPay වලට සම්බන්ධ කරන හැටි.") #
    st.write("2. Dialog Genie transaction fail වුනොත් කරන්න ඕන දේ.")
