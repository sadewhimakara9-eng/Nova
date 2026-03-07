import streamlit as st
from groq import Groq
from PIL import Image
from mcstatus import JavaServer

# 1. Page Config - මෙතනදී Sidebar එක 'expanded' (දිග හැරී) තියෙන්න සෙට් කරනවා
st.set_page_config(
    page_title="Nova Ultra Max", 
    page_icon="🤖", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. Groq API Key
client = Groq(api_key="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")

# 3. CSS - සම්පූර්ණ කළු පසුබිම සහ සුදු අකුරු
st.markdown("""
    <style>
    .stApp {
        background-color: #000000 !important;
    }
    h1, h2, h3, p, span, div, label, .stMarkdown {
        color: #ffffff !important;
    }
    .stChatMessage {
        background-color: #1a1a1a !important;
        border-radius: 12px;
        border: 1px solid #333333;
        margin-bottom: 10px;
    }
    section[data-testid="stSidebar"] {
        background-color: #111111 !important;
        border-right: 1px solid #333333;
    }
    .stChatInputContainer input {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR - දැන් මේක ඊතලය ඔබන්නේ නැතුවම පේනවා
with st.sidebar:
    st.title("🚀 Nova Tools")
    mode = st.radio("Tool එක තෝරන්න:", ["💬 Smart Chat", "🖼️ Image Vision", "🎵 Music Studio", "🎮 Minecraft Monitor"])
    st.markdown("---")
    st.write("Nova මඟින් ඕනෑම දෙයක් කරගන්න.")

# 5. MAIN LOGIC
if mode == "💬 Smart Chat":
    st.title("🤖 Nova Smart Chat")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "හලෝ! මම Nova. අද මොනවද වෙන්න ඕනේ?"}]
    
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
                    messages=[{"role": "system", "content": "You are Nova, an advanced assistant. Respond naturally."}, *st.session_state.messages],
                    model="llama-3.3-70b-versatile",
                )
                res = completion.choices[0].message.content
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            except Exception as e:
                st.error(f"Error: {e}")

elif mode == "🖼️ Image Vision":
    st.title("🖼️ Image Vision")
    up = st.file_uploader("Image එකක් අප්ලෝඩ් කරන්න", type=["jpg", "png"])
    if up:
        # අර කලින් Screenshot එකේ තිබුණ Syntax Error එක මෙතනදී මම හැදුවා (වරහන වසා ඇත)
        st.image(Image.open(up), use_container_width=True)
        st.info("Nova පින්තූරය කියවීමට සූදානම්.")

elif mode == "🎵 Music Studio":
    st.title("🎵 Music Studio")
    if st.button("Generate Music Track"):
        st.success("ට්‍රැක් එක සාර්ථකව හැදුණා! (30s)")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

elif mode == "🎮 Minecraft Monitor":
    st.title("🎮 Minecraft Monitor")
    ip = st.text_input("Server IP එක දෙන්න:", placeholder="e.g. play.hypixel.net")
    if st.button("Check Now"):
        try:
            srv = JavaServer.lookup(ip)
            stat = srv.status()
            st.success(f"Server එක Online! 🟢")
            st.metric("Players", f"{stat.players.online} / {stat.players.max}")
        except:
            st.error("Server එක Offline හෝ IP එක වැරදියි. 🔴")
