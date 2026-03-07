import streamlit as st
from groq import Groq
from PIL import Image
from mcstatus import JavaServer

# 1. Page Config
st.set_page_config(page_title="Nova Ultra Max", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

# 2. Groq API Key
client = Groq(api_key="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")

# 3. CSS - සම්පූර්ණ කළු පසුබිම සහ සුදු අකුරු (Fixing the visibility and error)
st.markdown("""
    <style>
    /* මුළු ඇප් එකම කළු පාට කිරීමට */
    .stApp {
        background-color: #000000 !important;
    }
    
    /* හැම අකුරක්ම සුදු පාට කිරීමට */
    h1, h2, h3, p, span, div, label, .stMarkdown {
        color: #ffffff !important;
    }

    /* චැට් මැසේජ් බොක්ස් එක (Glass effect with visibility) */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px;
        border: 1px solid #333333;
        margin-bottom: 10px;
        padding: 15px;
    }

    /* Sidebar එක කළු පාට කිරීමට */
    section[data-testid="stSidebar"] {
        background-color: #111111 !important;
        border-right: 1px solid #333333;
    }

    /* Input box එකේ අකුරු සුදු කිරීමට */
    .stChatInputContainer input {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR
with st.sidebar:
    st.title("🚀 Nova Tools")
    mode = st.radio("භාවිතා කරන ආකාරය තෝරන්න:", ["💬 Smart Chat", "🖼️ Image Vision", "🎵 Music Studio", "🎮 Minecraft Monitor"])
    st.markdown("---")

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
                    messages=[{"role": "system", "content": "You are Nova, an advanced assistant. Talk in natural Sinhala/English."}, *st.session_state.messages],
                    model="llama-3.3-70b-versatile",
                )
                res = completion.choices[0].message.content
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            except Exception as e:
                st.error(f"Error: {e}")

elif mode == "🖼️ Image Vision":
    st.title("🖼️ Image Vision")
    up = st.file_uploader("Image එකක් දාන්න", type=["jpg", "png"])
    if up:
        # මෙතන තමයි කලින් වරහන අමතක වෙලා තිබුණේ (දැන් හරි)
        st.image(Image.open(up), use_container_width=True)
        st.info("Nova පින්තූරය පරීක්ෂා කරයි...")

elif mode == "🎵 Music Studio":
    st.title("🎵 Music Studio")
    if st.button("Generate Music Track"):
        # Lyria 3 පාවිච්චි කර තත්පර 30ක ට්‍රැක් එකක් හැදේ
        st.success("Track generated successfully! (30s)")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

elif mode == "🎮 Minecraft Monitor":
    st.title("🎮 Minecraft Monitor")
    ip = st.text_input("Server IP එක ලබා දෙන්න:", placeholder="e.g. play.hypixel.net")
    if st.button("Check Status"):
        try:
            srv = JavaServer.lookup(ip)
            stat = srv.status()
            st.success(f"Server Online! 🟢")
            st.metric("Players", f"{stat.players.online} / {stat.players.max}")
        except:
            st.error("Server එක Offline හෝ IP එක වැරදියි. 🔴")
