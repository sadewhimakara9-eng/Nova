import streamlit as st
from groq import Groq

# පිටුවේ සැකසුම්
st.set_page_config(page_title="Nova AI Studio", page_icon="🤖", layout="wide")

# Groq API Key (AI එකට)
client = Groq(api_key="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")

st.title("🤖 Nova AI Music Studio")
st.caption("Chat with AI & Generate Professional Music")
st.markdown("---")

# Sidebar එකේ Music Settings දාමු
with st.sidebar:
    st.header("🎵 Music Generation")
    st.write("ඔයාට ඕන සින්දුව ගැන විස්තර කරන්න.")
    music_prompt = st.text_area("සින්දුවේ විස්තරය (Description):", placeholder="e.g. A chill lo-fi beat with a rainy mood")
    
    if st.button("Generate Music"):
        with st.spinner("සින්දුව හදමින් පවතියි..."):
            # මෙතනදී Lyria 3 පාවිච්චි කරලා සින්දුව Generate වෙනවා
            # දැනට අපි මෙතන Place holder එකක් දාමු ඇප් එක වැඩ කරනවා බලන්න
            st.success("Music track generated successfully! (තත්පර 30)")
            # මෙතන සින්දුව play වෙන player එක එනවා
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

# චැට් එක මතක තබා ගැනීම
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! How can I help you today? මට පුළුවන් ඔයා එක්ක චැට් කරන්න වගේම සින්දු හදලා දෙන්නත්."}
    ]

# පණිවිඩ පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# චැට් එකේ වැඩ කටයුතු
if prompt := st.chat_input("Nova ගෙන් මොනවා හරි අහන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": "You are Nova, an advanced AI assistant who can chat and help with music. Talk in natural Sinhala/English."
                    },
                    *st.session_state.messages
                ],
                model="llama-3.3-70b-versatile",
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error: {e}")
