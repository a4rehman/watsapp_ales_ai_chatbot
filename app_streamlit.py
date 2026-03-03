import streamlit as st
import subprocess
import os
import time
import socket
import signal
from dotenv import load_dotenv, set_key

# Page Config
st.set_page_config(page_title="AI Car Sales Manager", page_icon="🚗", layout="wide")
load_dotenv()

# --- Security: Admin Login ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def check_login():
    if st.session_state.admin_password == os.getenv("ACCESS_CODE", "123456"):
        st.session_state.authenticated = True
        st.rerun()
    else:
        st.error("Invalid Admin Password")

if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center; color: #25d366;'>🔒 Secure Admin Access</h1>", unsafe_allow_html=True)
    with st.container():
        left, mid, right = st.columns([1,1,1])
        with mid:
            st.text_input("Enter Admin Password", type="password", key="admin_password", on_change=check_login)
            st.button("Unlock Dashboard", on_click=check_login, use_container_width=True)
    st.stop() # Stop execution here until logged in

# --- After Authentication ---
# Main styling and logic below...
st.markdown("""
<style>
    .main { background-color: #0b141a; }
    h1, h2, h3 { color: #25d366 !important; font-weight: 700 !important; }
    .stButton>button { background-color: #25d366; color: #0b141a; font-weight: bold; border-radius: 10px; border: none; padding: 10px 20px; }
</style>
""", unsafe_allow_html=True)

if 'bot_process' not in st.session_state:
    st.session_state.bot_process = None

def start_bot():
    if not st.session_state.bot_process:
        process = subprocess.Popen(['node', 'index.js'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        st.session_state.bot_process = process
        st.toast("Bot Starting...", icon="🚀")

def stop_bot():
    if st.session_state.bot_process:
        if os.name == 'nt': subprocess.run(['taskkill', '/F', '/T', '/PID', str(st.session_state.bot_process.pid)], capture_output=True)
        else: os.kill(st.session_state.bot_process.pid, signal.SIGTERM)
        st.session_state.bot_process = None
        st.toast("Bot Stopped!", icon="🛑")

col1, col2 = st.columns([1, 2])

with col1:
    st.image("https://img.freepik.com/free-vector/car-showroom-abstract-concept-vector-illustration-car-dealership-buying-choosing-new-vehicle-luxury-automobile-leasing-auto-fleet-management-used-cars-sales-center-abstract-metaphor_335657-2936.jpg", use_container_width=True)
    st.title("Admin Dashboard")
    
    if st.session_state.bot_process is None:
        if st.button("▶️ Launch Bot", use_container_width=True): start_bot()
    else:
        if st.button("⏹️ Stop Bot", use_container_width=True): stop_bot()

    with st.expander("⚙️ Secure Settings"):
        # Key is now MASKED by default as a password input
        current_key = os.getenv("OPENAI_API_KEY", "")
        masked_key = f"{current_key[:6]}...{current_key[-4:]}" if len(current_key) > 10 else "No Key Set"
        st.write(f"Active Key: `{masked_key}`")
        
        new_key = st.text_input("Update OpenAI Key", type="password")
        if st.button("Update"):
            set_key(".env", "OPENAI_API_KEY", new_key)
            st.success("Key updated and hidden!")

    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.rerun()

with col2:
    st.header("WhatsApp Live Status")
    
    def check_port(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0

    if st.session_state.bot_process:
        if check_port(5000):
            st.success("✅ Secure Connection Active")
            st.components.v1.iframe("http://localhost:5000", height=600)
        else:
            st.warning("🔄 Initializing AI Engine... Scanning system ports.")
            time.sleep(3)
            st.rerun()
    else:
        st.info("System is offline. Launch to connect WhatsApp.")

st.caption("Built for Fiverr Client by AI Engineer Abdul Rehman")
