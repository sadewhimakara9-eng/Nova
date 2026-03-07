import streamlit as st
from groq import Groq
from PIL import Image
from mcstatus import JavaServer
import datetime

# yfinance එක install වෙලා නැත්නම් error එකක් එන එක වැළැක්වීමට
try:
    import yfinance as yf
except ImportError:
    yf = None

# 1. Page Config
st.set_page_config(page_title="Nova Ultra Max V2", page_icon="🚀", layout="wide")

# 2. Groq API Key
client = Groq(api_key="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")

# 3. CSS - UI & Text Visibility Fix
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
    
    /* Command Generator එකේ Code එක කොළ පාටින් පේන්න */
    code { color: #00ff00 !important; background-color: #1a1a1a !important; padding: 5px; border-radius: 5px; }
    
    .stMetric { background-color: #111111; border: 1px solid #333333; padding: 15px; border-radius: 10px; }
    section[data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #444; }
    .stButton>button { background-color: #ffffff !important; color: #000000 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR
with st.sidebar:
    st.title("🚀 Nova Next-Gen")
    mode = st.radio("පහසුකම තෝරන්න:", [
        "💬 Smart Chat", 
        "📄 File Analyzer",
        "🎮 Minecraft Monitor", 
        "⚔️ MC Command Helper",
        "💰 Finance & Crypto",
        "🖼️ Image Vision"
    ])

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

elif mode == "📄 File Analyzer":
    st.title("📄 Advanced File Reader")
    uploaded_file = st.file_uploader("Text file එකක් දාන්න (.txt)", type=["txt"])
    if uploaded_file:
        content = uploaded_file.read().decode("utf-8")
        st.success("File එක කියවන ලදී!")
        q = st.text_input("මේ ගොනුව ගැන Nova ගෙන් අහන්න:")
        if st.button("Analyze"):
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": f"Context: {content}"}, {"role": "user", "content": q}],
                model="llama-3.3-70b-versatile",
            )
            st.info(res.choices[0].message.content)

elif mode == "🎮 Minecraft Monitor":
    st.title("🎮 Server Live Status")
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
    st.title("⚔️ Command Generator")
    player = st.text_input("Player Name:", value="DeathnatorMC")
    item = st.text_input("Item:", value="oak_log")
    st.markdown("### Generated Command (Copy this):")
    st.code(f"/give {player} {item} 64")

elif mode == "💰 Finance & Crypto":
    st.title("💰 Finance Tracker")
    if yf:
        try:
            btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
            lkr = yf.Ticker("LKR=X").history(period="1d")['Close'].iloc[-1]
            c1, c2 = st.columns(2)
            c1.metric("Bitcoin (USD)", f"${btc:,.2f}")
            c2.metric("USD to LKR", f"Rs. {lkr:,.2f}")
        except:
            st.warning("මිල ගණන් ලබා ගැනීමට නොහැකි විය.")
    else:
        st.error("yfinance library එක තවම install වෙලා නැහැ. කරුණාකර requirements.txt පරීක්ෂා කරන්න.")

elif mode == "🖼️ Image Vision":
    st.title("🖼️ Vision AI")
    up = st.file_uploader("Upload Image", type=["jpg", "png"])
    if up: st.image(Image.open(up), use_container_width=True)
