import streamlit as st
from groq import Groq

# පිටුවේ සැකසුම්
st.set_page_config(page_title="Nova AI", page_icon="🤖", layout="centered")

# Groq API Key
client = Groq(api_key="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")

st.title("🤖 Nova AI Assistant")
st.caption("Advanced AI - Super Fast & Intelligent")
st.markdown("---")

# චැට් එක මතක තබා ගැනීම
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! How can I help you today? (ඔයාට අද මම උදවු කරන්නේ කොහොමද?)"}
    ]

# පණිවිඩ පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# පරිශීලකයාගෙන් අහන දේ
if prompt := st.chat_input("Nova ගෙන් මොනවා හරි අහන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # මෙතන තමයි Nova ව බුද්ධිමත් කරන්නේ
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system", 
                            "content": (
                                "You are Nova, a highly intelligent and helpful AI assistant like GPT-4 or Gemini. "
                                "1. Language: Detect the user's language automatically. If the user asks in English, reply in English. If the user asks in Sinhala, reply in clear, modern, and natural Sinhala. "
                                "2. Style: Be smart, helpful, and concise. Avoid weird or archaic words. "
                                "3. Capabilities: You can help with coding, writing, solving problems, and general knowledge. "
                                "4. Personality: Friendly and professional."
                            )
                        },
                        *st.session_state.messages
                    ],
                    model="llama-3.1-70b-versatile", # මම මෙතනට මීට වඩා ලොකු මොළයක් (70B) දැම්මා!
                )
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {e}")
