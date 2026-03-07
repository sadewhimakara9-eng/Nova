import streamlit as st
from groq import Groq

# 1. Page Config
st.set_page_config(page_title="Nova File Reader", page_icon="📄", layout="centered")

# 2. Groq API Key
client = Groq(api_key="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")

# 3. CSS - පිරිසිදු කළු පසුබිම සහ පැහැදිලි අකුරු
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    h1, h2, h3, p, span, div, label, .stMarkdown { color: #ffffff !important; }
    
    /* Input Boxes වල ලියන අකුරු කළු පාටින් පේන්න හැදීම */
    .stTextInput input, .stTextArea textarea {
        color: #000000 !important; 
        background-color: #ffffff !important;
        font-weight: bold !important;
    }
    
    /* Upload කරන කොටුවේ පාට */
    [data-testid="stFileUploader"] {
        background-color: #1a1a1a;
        padding: 20px;
        border-radius: 10px;
        border: 1px dashed #444;
    }
    
    .stButton>button {
        background-color: #ffffff !important;
        color: #000000 !important;
        width: 100%;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. UI
st.title("📄 Nova Advanced File Reader")
st.write("ඔයාගේ Text File එක අප්ලෝඩ් කරලා ඒක ගැන ඕනම දෙයක් අහන්න.")

# File Uploader
uploaded_file = st.file_uploader("Text file එකක් තෝරන්න (.txt)", type=["txt"])

if uploaded_file is not None:
    # ගොනුව කියවීම
    content = uploaded_file.read().decode("utf-8")
    
    with st.expander("ගොනුවේ අඩංගු දේ බලන්න"):
        st.text_area("File Content:", value=content, height=200, disabled=True)

    st.markdown("---")
    
    # ප්‍රශ්නය ඇසීම
    user_question = st.text_input("මේ ගොනුව ගැන Nova ගෙන් අහන්න:", placeholder="උදා: මේකේ තියෙන වැදගත්ම කරුණු 3 මොනවාද?")

    if st.button("Nova ගෙන් අසන්න"):
        if user_question:
            with st.spinner("Nova පිළිතුර සකසමින් පවතියි..."):
                try:
                    # AI එකට Context එක සහ ප්‍රශ්නය යැවීම
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "system",
                                "content": f"You are an assistant that analyzes text documents. Here is the context from the file: {content}"
                            },
                            {
                                "role": "user",
                                "content": user_question
                            }
                        ],
                        model="llama-3.3-70b-versatile",
                    )
                    
                    st.subheader("🤖 Nova ගේ පිළිතුර:")
                    st.info(chat_completion.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("කරුණාකර ප්‍රශ්නයක් ඇතුළත් කරන්න.")
else:
    st.info("පටන් ගැනීමට .txt ගොනුවක් අප්ලෝඩ් කරන්න.")
