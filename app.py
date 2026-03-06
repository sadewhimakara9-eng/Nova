import streamlit as st
import google.generativeai as genai

# පිටුවේ සැකසුම් (Browser එකේ උඩ පෙනුම)
st.set_page_config(page_title="Nova AI", page_icon="🤖", layout="centered")

# API Key එක සම්බන්ධ කිරීම (Quotes ඇතුළේ ඔයාගේ Key එක තියෙන්න ඕනේ)
genai.configure(api_key="AIzaSyBUWBL0tDxB7orebDecsNStsZsgmIwWnh8")

st.title("🤖 Nova AI Assistant")
st.caption("මම ඔයාගේ පෞද්ගලික සහායක Nova. මගෙන් ඕනෑම දෙයක් අහන්න.")
st.markdown("---")

# චැට් එක මතක තබා ගැනීම සඳහා (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# කලින් කරපු මැසේජ් පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# අලුත් මැසේජ් එකක් ඇතුළත් කිරීම (Chat Input)
if prompt := st.chat_input("Nova ගෙන් මොනවා හරි අහන්න..."):
    # පරිශීලකයාගේ මැසේජ් එක පෙන්වීම
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Nova ගේ පිළිතුර ලබා ගැනීම
    with st.chat_message("assistant"):
        with st.spinner("හිතමින් පවතියි..."):
            try:
                # මෙතන 'gemini-pro' පාවිච්චි කරලා තියෙන්නේ අර 404 Error එක මකන්න
                model = genai.GenerativeModel('gemini-pro')
                
                # සිංහලෙන් පිළිතුරු දීමට Nova ට උපදෙස් දීම
                full_prompt = f"Please respond to this in Sinhala: {prompt}"
                response = model.generate_content(full_prompt)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"පොඩි අවුලක්: {e}")
