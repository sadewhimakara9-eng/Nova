import streamlit as st
import google.generativeai as genai

# පිටුවේ පෙනුම සැකසීම
st.set_page_config(page_title="Nova AI", page_icon="🤖")

# API Key එක සම්බන්ධ කිරීම
genai.configure(api_key="AIzaSyBUWBL0tDxB7orebDecsNStsZsgmIwWnh8")

st.title("🤖 Nova AI Assistant")
st.caption("මම Nova. මගෙන් ඕනෑම දෙයක් අහන්න.")
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
            # මෙතන 'models/' කෑල්ල අයින් කරලා නම විතරක් පාවිච්චි කරනවා
            # මෙය ඕනෑම Gemini API එකක වැඩ කරන ස්ථාවරම ක්‍රමයයි
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            
            response = model.generate_content("Respond clearly in Sinhala: " + prompt)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("පිළිතුරක් ලබා ගැනීමට නොහැකි විය.")
        except Exception as e:
            # වැරැද්ද හරියටම පෙන්වීමට debug කිරීම
            st.error(f"තාක්ෂණික ගැටලුවක්: {str(e)}")
