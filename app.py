import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Nova AI", page_icon="🤖")
st.title("🤖 Nova AI Assistant")

# ඔයාගේ API Key එක මෙතන Quotes ඇතුළට හරියටම දාන්න
# උදා: "AIzaSy..."
genai.configure(api_key="AIzaSyCthzTiHqgDOg3PQJZwRLLUsvOoxhPkjOk")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Nova ගෙන් අහන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # මෙතනින් තමයි ඇත්තම ලෙඩේ පෙන්වන්නේ
            st.error(f"ඇප් එකේ ගැටලුවක්: {e}")
