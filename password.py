import streamlit as st
import re
import random
import string
import pandas as pd

def check_password_strength(password):
    score = 0
    feedback = []
    
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Make it at least 8 characters long.")
    
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter (A-Z).")
    
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Include at least one lowercase letter (a-z).")
    
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Use at least one digit (0-9).")
    
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("Include at least one special character (!@#$%^&*).")
    
    if len(set(password)) < len(password) * 0.6:
        feedback.append("Avoid repeating characters too often.")
    
    if password.lower() in ["password", "123456", "qwerty", "admin", "letmein"]:
        feedback.append("Avoid common passwords.")
    
    if score <= 2:
        strength = "Weak"
        color = "red"
    elif score <= 4:
        strength = "Moderate"
        color = "orange"
    else:
        strength = "Strong"
        color = "green"
    
    return score, strength, color, feedback

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(length))

st.set_page_config(page_title="Password Strength Meter", layout="centered")

mode = st.radio("Select Mode:", ["Light Mode ☀️", "Dark Mode 🌙"], horizontal=True)
if mode == "Dark Mode 🌙":
    st.markdown("""
        <style>
            body, .stApp { background-color: #121212; color: white; }
            .stTextInput input { background-color: #333; color: white; border-radius: 5px; }
            .stButton>button { background-color: #444; color: white; border-radius: 5px; }
            .stMarkdown { color: white; }
            .stSlider .css-1aumxhk { color: purple !important; }
        </style>
    """, unsafe_allow_html=True)

st.title("🔐 Password Strength Meter")
st.markdown("🔒 Check the security level of your password and 🔑 generate strong passwords easily! 🔐")


st.header("🔍 Check Password Strength")
password = st.text_input("Enter your password:", type="password")
if st.button("Check Strength"):
    if password:
        score, strength, color, feedback = check_password_strength(password)
        
        st.markdown(f"### Strength: <span style='color:{color}; font-size:20px;'>{strength}</span>", unsafe_allow_html=True)
        
        if strength == "Strong":
            st.success("✅ Great! Your password is strong.")
        else:
            st.warning("⚠️ Your password can be improved. Suggestions:")
            for tip in feedback:
                st.write(f"- {tip}")
    else:
        st.error("Please enter a password to check its strength.")

st.header("🔑 Generate a Strong Password")
length = st.slider("Select Password Length:", min_value=8, max_value=24, value=12)
if 'password_history' not in st.session_state:
    st.session_state['password_history'] = []

if st.button("Generate Password"):
    generated_password = generate_password(length)
    st.session_state['password_history'].append(generated_password)
    st.text_input("Generated Password:", generated_password)

st.header("🔧 App Settings")

st.subheader("Password History")
if st.session_state['password_history']:
    df = pd.DataFrame(st.session_state['password_history'], columns=["Generated Passwords"])
    st.dataframe(df)
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Password History", csv, "password_history.csv", "text/csv", key='download-csv')
    
    if st.button("🗑️ Clear Password History"):
        st.session_state['password_history'] = []
        st.rerun()
else:
    st.info("No passwords generated yet.")

st.markdown("""
    <hr>
    <div style='text-align: center;'>
        Made with ❤️ using Streamlit | © 2025 Mehak Akram
    </div>
""", unsafe_allow_html=True)
