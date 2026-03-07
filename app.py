import streamlit as st
from groq import Groq

# පිටුවේ සැකසුම්
st.set_page_config(page_title="Nova AI", page_icon="🤖")

# Groq API Key එක සම්බන්ධ කිරීම
client = Groq(api_key="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")

st.title("🤖 Nova AI Assistant")
st.caption("Powered by Groq - Super Fast AI")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Nova ගෙන් මොනවා හරි අහන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # මෙන්න මෙතන තමයි වෙනස කළේ - ලෝකයේ අලුත්ම Llama 3.1 මොඩල් එක
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are Nova, a helpful assistant. Respond in Sinhala language clearly."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.1-8b-instant", # මෙන්න අලුත්ම නම!
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error: {e}")
