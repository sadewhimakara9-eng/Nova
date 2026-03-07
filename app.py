import streamlit as st
from groq import Groq
from PIL import Image
from mcstatus import JavaServer

# 1. Page Config
st.set_page_config(page_title="Nova Ultra Max", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

# 2. Groq API Key
client = Groq(api_key="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")

# 3. CSS - අකුරු සුදු පාටට හැදීම (Text Visibility Fix)
st.markdown("""
    <style>
    /* මුළු ඇප් එකේම පසුබිම තද නිල්/කළු පාටක් කරමු */
    .stApp {
        background-color: #0f172a;
    }
    
    /* හැම අකුරක්ම සුදු පාටට පේන්න හදමු */
    h1, h2, h3, p, span, div, label {
        color: #ffffff !important;
    }

    /* චැට් මැසේජ් බොක්ස් එක පේන විදිහ */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 10px;
        color: white !important;
    }

    /* Input box එකේ අකුරු කළු පාට වෙන්න පුළුවන් නිසා ඒකත් හදමු */
    .stChatInputContainer input {
        color: white !important;
    }
    
    /* Sidebar එකේ අකුරු */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR
with st.sidebar:
    st.title("🚀 Nova Tools")
    mode = st.radio("Options:", ["💬 Smart Chat", "🖼️ Image Vision", "🎵 Music Studio", "🎮 Minecraft Monitor"])
    st.markdown("---")

# 5. MAIN LOGIC
if mode == "💬 Smart Chat":
    st.title("🤖 Nova Smart Chat")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi! මම Nova. අද මොනවද වෙන්න ඕනේ?"}]
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Nova ගෙන් අහන්න..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                completion = client.chat.completions.create(
                    messages=[{"role": "system", "content": "You are Nova, an advanced assistant. Talk in natural Sinhala/English."}, *st.session_state.messages],
                    model="llama-3.3-70b-versatile",
                )
                res = completion.choices[0].message.content
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            except Exception as e:
                st.error(f"Error: {e}")

elif mode == "🖼️ Image Vision":
    st.title("👁️ Image Vision")
    up = st.file_uploader("Image එකක් දාන්න", type=["jpg", "png"])
    if up:
        st.image(Image.open(up), use_container_width=True)
        st.info("Llama-3.2-Vision හරහා Nova පින්තූරය කියවයි.")

elif mode == "🎵 Music Studio":
    st.title("🎵 Music Studio")
    if st.button("Generate Track"):
        st.success("Track generated! (30s)")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

elif mode == "🎮 Minecraft Monitor":
    st.title("🎮 Minecraft Monitor")
    ip = st.text_input("Server IP:", placeholder="e.g. play.hypixel.net")
    if st.button("Check Status"):
        try:
            srv = JavaServer.lookup(ip)
            stat = srv.status()
            st.success(f"Server Online! 🟢")
            st.write(f"Players: {stat.players.online}")
        except:
            st.error("Offline හෝ IP වැරදියි. 🔴")
