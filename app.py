import streamlit as st
import google.generativeai as genai

# පිටුවේ පෙනුම සැකසීම
st.set_page_config(page_title="Nova AI", page_icon="🤖")

# ඔයා එවපු අලුත්ම API Key එක මෙන්න
genai.configure(api_key="AIzaSyD2y83ac1I40JHexIWSlm9rm_LOodZWEUQ")

st.title("🤖 Nova AI Assistant")
st.caption("දැන් මම වැඩ! මගෙන් ඕනෑම දෙයක් අහන්න.")
st.markdown("---")

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
            # ස්ථාවරම මොඩල් එක
            model = genai.GenerativeModel('gemini-1.5-flash')
            # සිංහලෙන් පිළිතුරු දීමට උපදෙස් දීම
            response = model.generate_content("Respond in Sinhala: " + prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
