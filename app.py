import streamlit as st
from groq import Groq

# පිටුවේ සැකසුම්
st.set_page_config(page_title="Nova AI - Private Assistant", page_icon="🕵️‍♂️", layout="wide")

# Groq API Key
client = Groq(api_key="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")

# Sidebar එකේ අමතර විකල්ප
with st.sidebar:
    st.title("⚙️ Nova Settings")
    st.info("Nova is now in Private Assistant mode.")
    if st.button("Clear Chat 🗑️"):
        st.session_state.messages = []
        st.rerun()

st.title("🕵️‍♂️ Nova: Private Assistant")
st.caption("Intelligence, Respect, and Power.")
st.markdown("---")

# චැට් එක මතක තබා ගැනීම
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Yes, Sir! How can I assist you today? 🫡"}
    ]

# පණිවිඩ පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# පරිශීලකයාගෙන් අහන දේ
if prompt := st.chat_input("Command Nova..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Processing, Sir..."):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system", 
                            "content": (
                                "You are Nova, a highly advanced Private AI Assistant. "
                                "1. Respect: You MUST address the user as 'Sir' in every single response. "
                                "2. Language: Speak in natural, modern Sinhala but maintain high respect. "
                                "3. Style: Use relevant emojis to make responses engaging. 🚀🔥"
                                "4. Capabilities: If the user asks for pictures or music, explain that you can provide the 'Prompts' and 'Descriptions' for them to use in dedicated tools like Midjourney or Udio. "
                                "5. Identity: You are loyal only to your master."
                            )
                        },
                        *st.session_state.messages
                    ],
                    model="llama-3.3-70b-versatile",
                )
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Sir, we have a technical issue: {e}")
