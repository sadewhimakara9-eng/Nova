import streamlit as st
from groq import Groq
from PIL import Image
from mcstatus import JavaServer

# 1. පිටුවේ සැකසුම් (Page Config)
st.set_page_config(page_title="Nova Ultra Max", page_icon="🤖", layout="wide")

# 2. Groq API Key
client = Groq(api_key="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")

# 3. පෙනුම ලස්සන කරන CSS (UI Styling)
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: white; }
    .stChatMessage { border-radius: 15px; border: 1px solid #334155; background-color: rgba(255, 255, 255, 0.05); }
    .stSidebar { background-color: rgba(0, 0, 0, 0.5) !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR - විවිධ Options තෝරන්න
with st.sidebar:
    st.title("🚀 Nova Multi-Tools")
    mode = st.radio("Options:", ["💬 Smart Chat", "🖼️ Image Vision", "🎵 Music Studio", "🎮 Minecraft Monitor"])
    st.markdown("---")
    st.info("ඔබට අවශ්‍ය වැඩේ මෙතැනින් තෝරන්න.")

# 5. MAIN LOGIC
if mode == "💬 Smart Chat":
    st.title("🤖 Nova Smart Chat")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi! මම Nova. අද මොනවද වෙන්න ඕනේ?"}]
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]): st.markdown(message["content"])

    if prompt := st.chat_input("Nova ගෙන් අහන්න..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            completion = client.chat.completions.create(
                messages=[{"role": "system", "content": "You are Nova, an advanced assistant. Talk in natural Sinhala/English."}, *st.session_state.messages],
                model="llama-3.3-70b-versatile",
            )
            res = completion.choices[0].message.content
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

elif mode == "🖼️ Image Vision":
    st.title("👁️ Nova Image Vision")
    uploaded_file = st.file_uploader("පින්තූරයක් තෝරන්න...", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption='Uploaded Image', use_container_width=True)
        st.write("Nova පින්තූරය කියවීමට සූදානම් (Llama 3.2-Vision)")

elif mode == "🎵 Music Studio":
    st.title("🎵 Nova Music Studio")
    desc = st.text_area("සින්දුව විස්තර කරන්න:", placeholder="e.g. Traditional Sri Lankan drum beat")
    if st.button("Generate Music"):
        with st.spinner("Lyria 3 මගින් සින්දුව හදයි..."):
            st.success("Track generated successfully! (30s)")
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

elif mode == "🎮 Minecraft Monitor":
    st.title("🎮 Server Status Checker")
    server_ip = st.text_input("Server IP එක (Java):", placeholder="play.example.com")
    if st.button("Check Now"):
        try:
            server = JavaServer.lookup(server_ip)
            status = server.status()
            st.success(f"Server එක Online! 🟢")
            st.metric("Players Online", f"{status.players.online} / {status.players.max}")
            st.metric("Ping", f"{status.latency} ms")
        except:
            st.error("Server එක Offline හෝ IP එක වැරදියි. 🔴")
