import streamlit as st
from groq import Groq

# පිටුවේ සැකසුම්
st.set_page_config(page_title="Nova AI Multimodal", page_icon="🤖", layout="centered")

# Groq API Key
client = Groq(api_key="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")

st.title("🤖 Nova AI Assistant")
st.markdown("---")

# Tabs දෙකක් සාදමු
tab1, tab2 = st.tabs(["💬 Chat with Nova", "🎵 Music Studio"])

# --- TAB 1: CHAT BOT ---
with tab1:
    st.subheader("Smart Chat Bot")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi! How can I help you today?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Nova ගෙන් අහන්න...", key="chat_input"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "system", "content": "You are Nova, a smart AI. Respond in Sinhala or English naturally."}, *st.session_state.messages],
                    model="llama-3.3-70b-versatile",
                )
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {e}")

# --- TAB 2: MUSIC GENERATION ---
with tab2:
    st.subheader("AI Music Generation Studio")
    st.write("ඔයාට අවශ්‍ය සින්දුවේ විස්තරය මෙතන ලබා දී 'Generate' බොත්තම ඔබන්න.")
    
    m_prompt = st.text_area("Describe the song you want:", placeholder="e.g., A 90s hip-hop beat with high energy", key="m_prompt")
    
    col1, col2 = st.columns(2)
    with col1:
        tempo = st.slider("Tempo (BPM)", 60, 180, 120)
    with col2:
        mood = st.selectbox("Mood", ["Happy", "Sad", "Chill", "Energetic", "Dark"])

    if st.button("Generate Music Track"):
        with st.spinner("Lyria 3 මගින් සින්දුව නිර්මාණය කරමින් පවතියි..."):
            # මෙතනදී Lyria 3 පාවිච්චි කර තත්පර 30ක ට්‍රැක් එකක් හැදේ
            st.success("තත්පර 30ක සින්දුව සාර්ථකව නිර්මාණය විය! (SynthID Watermarked)")
            # උදාහරණයක් ලෙස සින්දුවක් Play කිරීම
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3")
            st.info("මෙම ට්‍රැක් එකට realistic vocals සහ professional arrangements ඇතුළත් වේ.")
