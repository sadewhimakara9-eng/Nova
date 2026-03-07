import streamlit as st
from groq import Groq

# පිටුවේ සැකසුම්
st.set_page_config(page_title="Nova AI", page_icon="🤖")

# Groq API Key
client = Groq(api_key="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")

st.title("🤖 Nova AI Assistant")
st.caption("Powered by Groq - Super Fast AI")
st.markdown("---")

# චැට් එක මතක තබා ගැනීම සහ ආරම්භක පණිවිඩය
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
        try:
            # මෙන්න මෙතන තමයි Nova ගේ සිංහල හදන්නේ
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "You are Nova, a friendly Sri Lankan AI assistant. "
                            "You must respond in clear, natural, and modern colloquial Sinhala (not formal or archaic). "
                            "Avoid words like 'නමස්කාර', 'මහත්මයා', or 'පරිශීලකයා'. "
                            "Talk like a normal Sri Lankan friend. "
                            "Use phrases like 'මොකක්ද වෙන්න ඕනේ?', 'මම කොහොමද උදවු කරන්නේ?' etc. "
                            "Strictly no Tamil, Thai, or mixed languages."
                        )
                    },
                    *st.session_state.messages
                ],
                model="llama-3.1-8b-instant",
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error: {e}")
