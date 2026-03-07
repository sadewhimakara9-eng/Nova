import streamlit as st
from groq import Groq

# පිටුවේ සැකසුම්
st.set_page_config(page_title="Nova AI", page_icon="🤖")

# Groq API Key
client = Groq(api_key="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")

st.title("🤖 Nova AI Assistant")
st.caption("Powered by Groq - Super Fast AI")
st.markdown("---")

# චැට් එක මතක තබා ගැනීම
if "messages" not in st.session_state:
    # ආරම්භක පණිවිඩය මෙතනට දාමු
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! How can I help you today? (ඔබට අද මම උදවු කරන්නේ කොහොමද?)"}
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
        try:
            # මෙතන තමයි උපදෙස් දෙන්නේ
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": "You are Nova, a friendly AI assistant. You must respond in clear, natural Sinhala language only. Avoid Tamil, Thai, or any mixed languages. If the user greets you, greet them back warmly in Sinhala."
                    },
                    # කලින් කරපු චැට් එකත් මොළයට දෙනවා
                    *st.session_state.messages
                ],
                model="llama-3.1-8b-instant",
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error: {e}")
