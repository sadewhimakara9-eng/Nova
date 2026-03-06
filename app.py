import streamlit as st
import google.generativeai as genai

# පිටුවේ සැකසුම් සහ පෙනුම
st.set_page_config(page_title="Nova AI", page_icon="🤖", layout="centered")

# CSS මගින් පෙනුම තවත් ලස්සන කිරීම
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stTextInput > div > div > input { border-radius: 20px; }
    </style>
    """, unsafe_allow_config=True)

# API Key එක සම්බන්ධ කිරීම
genai.configure(AIzaSyBUWBL0tDxB7orebDecsNStsZsgmIwWnh8)

st.title("🤖 Nova AI Assistant")
st.caption("මම ඔයාගේ පෞද්ගලික සහායක Nova. මගෙන් ඕනෑම දෙයක් අහන්න.")

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
        with st.spinner("හිතමින් පවතියි..."):
            model = genai.GenerativeModel('gemini-1.5-flash')
            # සිංහලෙන් උත්තර දීමට උපදෙස් දීම
            response = model.generate_content("Respond in Sinhala: " + prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
