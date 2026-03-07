import streamlit as st
from groq import Groq

# පිටුවේ සැකසුම් සහ නම
st.set_page_config(page_title="Nova AI", page_icon="🤖", layout="centered")

# Groq API Key එක සම්බන්ධ කිරීම
# ඔයා එවපු Key එක මෙතන තියෙනවා
client = Groq(api_key="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")

st.title("🤖 Nova AI Assistant")
st.caption("Powered by Groq - Super Fast AI Service")
st.markdown("---")

# චැට් එක මතක තබා ගැනීම සඳහා
if "messages" not in st.session_state:
    st.session_state.messages = []

# කලින් කරපු මැසේජ් පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# අලුත් මැසේජ් එකක් ඇතුළත් කිරීම
if prompt := st.chat_input("Nova ගෙන් මොනවා හරි අහන්න..."):
    # ඔයාගේ මැසේජ් එක පෙන්වීම
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Nova ගේ පිළිතුර ලබා ගැනීම
    with st.chat_message("assistant"):
        with st.spinner("පිළිතුර සකසමින් පවතියි..."):
            try:
                # Llama 3 කියන බලවත්ම මොඩල් එක පාවිච්චි කිරීම
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system", 
                            "content": "You are Nova, a helpful AI assistant. Always respond in Sinhala language clearly and naturally."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    model="llama3-8b-8192",
                )
                
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"තාක්ෂණික ගැටලුවක්: {e}")
