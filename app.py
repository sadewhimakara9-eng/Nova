import streamlit as st
from groq import Groq
from PIL import Image
from mcstatus import JavaServer
from streamlit_mic_recorder import mic_recorder
import datetime
import yfinance as yf

# 1. Page Config
st.set_page_config(page_title="Nova Pro Max", page_icon="🛡️", layout="wide")

# 2. Groq API Key
client = Groq(api_key="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")

# 3. CSS - Pro UI
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    h1, h2, h3, p, span, div, label, .stMarkdown { color: #ffffff !important; }
    .stTextInput input, .stSelectbox div, .stNumberInput input, .stTextArea textarea {
        color: #000000 !important; background-color: #ffffff !important; font-weight: bold !important;
    }
    .stMetric { background-color: #0a0a0a; border: 1px solid #00ff00; padding: 15px; border-radius: 10px; }
    section[data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #444; }
    .stButton>button { background-color: #00ff00 !important; color: #000000 !important; font-weight: bold !important; border-radius: 8px; }
    code { color: #ff00ff !important; background-color: #1a1a1a !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR
with st.sidebar:
    st.title("🛡️ Nova Pro Control")
    mode = st.radio("Tool එක තෝරන්න:", [
        "💬 Voice & Smart Chat", 
        "🎮 MC Admin Dashboard", 
        "📄 File Analyzer",
        "🛡️ Cyber Security Lab",
        "💳 BOC/iPay Guide",
        "💰 Finance & Crypto"
    ])
    st.markdown("---")
    st.write("Current Server: **Better MC 1.21.11**")

# 5. MAIN LOGIC

if mode == "💬 Voice & Smart Chat":
    st.title("🎤 Nova Voice & Chat")
    st.write("ලියන්න කම්මැලි නම් මයික් එක ඔබලා කතා කරන්න!")
    
    # Voice Recorder
    audio = mic_recorder(start_prompt="කතා කරන්න (Start)", stop_prompt="නැවතීමට (Stop)", key='recorder')
    
    if audio:
        st.audio(audio['bytes'])
        st.info("හඬ හඳුනාගැනීම සඳහා සූදානම් වෙමින් පවතියි... (මෙම පහසුකම භාවිතා කිරීමට API එකට යැවිය යුතුය)")

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "මම Nova. අද මොනවද වෙන්න ඕනේ මචං?"}]
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    
    if prompt := st.chat_input("Nova ගෙන් අහන්න..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            comp = client.chat.completions.create(
                messages=[{"role": "system", "content": "You are Nova, an expert in Minecraft, Sri Lankan Banking, and Cybersecurity."}, *st.session_state.messages],
                model="llama-3.3-70b-versatile",
            )
            res = comp.choices[0].message.content
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

elif mode == "🎮 MC Admin Dashboard":
    st.title("🎮 Minecraft Admin Dashboard")
    server_address = "185.207.166.145:19008"
    
    if st.button("Refresh Server Status"):
        try:
            server = JavaServer.lookup(server_address)
            status = server.status()
            st.success("Server Online! 🟢")
            st.metric("Ping", f"{int(status.latency)} ms")
            st.metric("Players", f"{status.players.online} / {status.players.max}")
        except:
            st.error("Server Offline! 🔴")

    st.markdown("### Quick Commands")
    p_name = st.text_input("Player Name:", value="DeathnatorMC")
    if st.button("Give Oak Logs Bundle"):
        st.code(f"/give {p_name} oak_log 64")

elif mode == "🛡️ Cyber Security Lab":
    st.title("🛡️ Cyber Security Lab")
    st.write("අධ්‍යාපනික කටයුතු සඳහා පමණක් භාවිතා කරන්න.")
    tool = st.selectbox("Tool එක තෝරන්න:", ["Aircrack-ng (Wi-Fi)", "Nmap (Scanning)", "Metasploit"])
    if tool == "Aircrack-ng (Wi-Fi)":
        st.code("airmon-ng start wlan0")
        st.code("airodump-ng wlan0mon")
        st.info("Wi-Fi network එකේ security පරීක්ෂා කිරීමට ඉහත පියවර අනුගමනය කරන්න.")

elif mode == "💳 BOC/iPay Guide":
    st.title("💳 Sri Lankan Banking Helper")
    bank_task = st.selectbox("කරන්න අවශ්‍ය දේ:", ["BOC Card Link to iPay", "Dialog Genie Transaction Fail Fix", "Money Transfer Guide"])
    if bank_task == "BOC Card Link to iPay":
        st.write("1. iPay App එක Open කරන්න.")
        st.write("2. 'Add Bank Account/Card' තෝරන්න.")
        st.write("3. BOC Debit Card එකේ තොරතුරු සහ OTP එක ඇතුළත් කරන්න.")

elif mode == "💰 Finance & Crypto":
    st.title("💰 Finance Tracker")
    try:
        btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
        lkr = yf.Ticker("LKR=X").history(period="1d")['Close'].iloc[-1]
        st.metric("Bitcoin (USD)", f"${btc:,.2f}")
        st.metric("USD to LKR", f"Rs. {lkr:,.2f}")
    except:
        st.warning("Data loading...")

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
