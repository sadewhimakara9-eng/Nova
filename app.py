import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Nova AI", page_icon="🤖")
st.title("🤖 Nova AI Assistant")

# API Key සම්බන්ධ කිරීම
genai.configure(api_key="AIzaSyBUWBL0tDxB7orebDecsNStsZsgmIwWnh8")

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
        # පිළිවෙළින් මොඩල් වර්ග 3ක්ම ට්‍රයි කරනවා
        models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
        success = False
        
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Respond in Sinhala: " + prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                success = True
                break # එකක් වැඩ කළොත් ඉතිරි ඒවා බලන්නේ නැහැ
            except:
                continue
        
        if not success:
            st.error("කනගාටුයි, කිසිදු මොඩලයක් සම්බන්ධ කරගත නොහැකි විය. කරුණාකර මද වෙලාවකින් උත්සාහ කරන්න.")
