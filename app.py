import streamlit as st
import google.generativeai as genai

# පිටුවේ සැකසුම්
st.set_page_config(page_title="Nova AI", page_icon="🤖")

# API Key එක සම්බන්ධ කිරීම (මෙතන Quotes දාලා තියෙන්නේ දැන්)
genai.configure(api_key="AIzaSyCthzTiHqgDOg3PQJZwRLLUsvOoxhPkjOk")

st.title("🤖 Nova AI Assistant")
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
            model = genai.GenerativeModel('gemini-1.5-flash')
            # සිංහලෙන් උත්තර දීමට උපදෙස් දීම
            response = model.generate_content("Respond in Sinhala: " + prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("පොඩි ගැටලුවක්. පසුව උත්සාහ කරන්න.")
