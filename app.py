import streamlit as st
from groq import Groq

# පිටුවේ සැකසුම්
st.set_page_config(page_title="Nova AI", page_icon="🤖", layout="centered")

# Groq API Key
client = Groq(api_key="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")

st.title("🤖 Nova AI Assistant")
st.caption("Intelligence Redefined - Super Fast & Smart")
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
        with st.spinner("Nova is thinking..."):
            try:
                # මෙන්න දැනට තියෙන ස්ථාවරම සහ බුද්ධිමත්ම මොඩල් එක
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system", 
                            "content": (
                                "You are Nova, an advanced and highly intelligent AI assistant, similar to Gemini or GPT-4. "
                                "1. Language: Automatically detect the user's language. If they speak in English, reply in professional English. If they speak in Sinhala, reply in clear, modern, and natural colloquial Sinhala. "
                                "2. Knowledge: You have deep knowledge in coding, science, history, and creative writing. "
                                "3. Instructions: Be helpful, accurate, and avoid archaic or weird translations. Talk like a smart human friend."
                            )
                        },
                        *st.session_state.messages
                    ],
                    model="llama-3.3-70b-versatile", # මේක තමයි දැන් තියෙන අලුත්ම සහ වැඩ කරන නම!
                )
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"තාක්ෂණික දෝෂයක්: {e}")
