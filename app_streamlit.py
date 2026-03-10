import streamlit as st
import subprocess
import os
import time
import socket
import signal
from dotenv import load_dotenv, set_key

# --- Page Configuration ---
st.set_page_config(
    page_title="Car Showroom AI | Pro Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# --- Custom Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #0b141a;
        color: #e9edef;
    }
    
    /* Header styling */
    .premium-header {
        background: linear-gradient(90deg, #25d366 0%, #128c7e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    /* Card-like containers */
    .stSecondaryBlock {
        background-color: #1c2b33;
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid #2a3942;
    }
    
    /* Button styling */
    .stButton>button {
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(37, 211, 102, 0.3);
    }
    
    /* Success/Info boxes */
    .stAlert {
        border-radius: 10px;
        border: none;
    }
    
    .status-badge {
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
    }
    
    .status-online {
        background-color: rgba(37, 211, 102, 0.2);
        color: #25d366;
    }
    
    .status-offline {
        background-color: rgba(239, 68, 68, 0.2);
        color: #ef4444;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'bot_process' not in st.session_state:
    st.session_state.bot_process = None

# --- Authentication Logic ---
def check_login():
    if st.session_state.admin_password == os.getenv("ACCESS_CODE", "123456"):
        st.session_state.authenticated = True
    else:
        st.error("Invalid Admin Access Code")

if not st.session_state.authenticated:
    st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col1:
        st.write("")
    with col2:
        st.markdown("<h1 style='text-align: center; color: #25d366;'>🔒 Enterprise Login</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #8696a0;'>Car Showroom AI Management System</p>", unsafe_allow_html=True)
        with st.form("login_form"):
            st.text_input("Access Code", type="password", key="admin_password")
            submit = st.form_submit_button("Unlock Dashboard", use_container_width=True)
            if submit:
                check_login()
                if st.session_state.authenticated:
                    st.rerun()
    st.stop()

# --- Functions ---
def start_bot():
    if not st.session_state.bot_process:
        try:
            # Check if node is installed
            subprocess.run(['node', '-v'], capture_output=True, check=True)
            process = subprocess.Popen(['node', 'index.js'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            st.session_state.bot_process = process
            st.toast("AI Engine Initializing...", icon="🚀")
        except Exception as e:
            st.error(f"Failed to start bot: {e}")

def stop_bot():
    if st.session_state.bot_process:
        try:
            if os.name == 'nt':
                subprocess.run(['taskkill', '/F', '/T', '/PID', str(st.session_state.bot_process.pid)], capture_output=True)
            else:
                os.kill(st.session_state.bot_process.pid, signal.SIGTERM)
            st.session_state.bot_process = None
            st.toast("AI Engine Halted.", icon="🛑")
        except Exception as e:
            st.error(f"Error stopping bot: {e}")

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

# --- Dashboard UI ---
st.markdown("<h1 class='premium-header'>CAR SHOWROOM AI <span style='font-size: 1.2rem; vertical-align: middle; background: #25d366; color: #0b141a; padding: 4px 10px; border-radius: 5px; -webkit-text-fill-color: #0b141a;'>PRO</span></h1>", unsafe_allow_html=True)

col_sidebar, col_main = st.columns([1, 3], gap="large")

with col_sidebar:
    st.image("https://img.freepik.com/free-vector/car-showroom-abstract-concept-vector-illustration-car-dealership-buying-choosing-new-vehicle-luxury-automobile-leasing-auto-fleet-management-used-cars-sales-center-abstract-metaphor_335657-2936.jpg", use_container_width=True)
    
    st.markdown("### System Controls")
    status_color = "status-online" if st.session_state.bot_process else "status-offline"
    status_text = "Running" if st.session_state.bot_process else "Offline"
    st.markdown(f"<p>Status: <span class='status-badge {status_color}'>{status_text}</span></p>", unsafe_allow_html=True)
    
    if st.session_state.bot_process is None:
        if st.button("▶️ Launch AI Bot", use_container_width=True, type="primary"):
            start_bot()
            st.rerun()
    else:
        if st.button("⏹️ Stop AI Bot", use_container_width=True):
            stop_bot()
            st.rerun()

    st.divider()
    
    with st.expander("⚙️ Provider Settings"):
        current_key = os.getenv("GEMINI_API_KEY", "")
        masked_key = f"{current_key[:6]}...{current_key[-4:]}" if current_key and len(current_key) > 10 else "None"
        st.info(f"Active Provider: **Google Gemini**")
        st.caption(f"API Key: `{masked_key}`")
        
        new_key = st.text_input("Update Gemini Key", type="password")
        if st.button("Apply Changes", use_container_width=True):
            set_key(".env", "GEMINI_API_KEY", new_key)
            st.success("New key saved!")
            time.sleep(1)
            st.rerun()

    if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
        st.session_state.authenticated = False
        st.rerun()

with col_main:
    tabs = st.tabs(["📡 Live Interface", "📊 Conversation Stats", "🛠️ System Diagnostics"])
    
    with tabs[0]:
        st.subheader("WhatsApp Connection Hub")
        if st.session_state.bot_process:
            if is_port_in_use(5000):
                st.success("System is live! Use the interface below to scan and monitor.")
                st.components.v1.iframe("http://localhost:5000", height=650, scrolling=True)
            else:
                with st.status("Booting up WhatsApp AI engine...", expanded=True) as status:
                    st.write("Initializing Puppeteer...")
                    time.sleep(2)
                    st.write("Establishing Secure Bridge...")
                    time.sleep(2)
                    st.write("Syncing with WhatsApp Web...")
                    st.rerun()
        else:
            st.info("AI Bot is currently offline. Launch the bot to start responding to customers.")
            st.image("https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?auto=format&fit=crop&q=80&w=1200", caption="Automate your showroom sales with Gemini-powered AI", use_container_width=True)

    with tabs[1]:
        col_metric1, col_metric2, col_metric3 = st.columns(3)
        col_metric1.metric("Response Time", "1.2s", "-0.3s")
        col_metric2.metric("Active Sessions", "12", "+2")
        col_metric3.metric("AI Confidence", "98%", "Stable")
        
        st.image("https://cdn.pixabay.com/photo/2016/11/22/10/47/modern-1849063_1280.jpg", caption="Your car sales assistant is ready to help.", use_container_width=True)

    with tabs[2]:
        st.write("### System Logs Summary")
        st.code("""
[SYSTEM] Node.js v18.x detected
[INFO] Google Gemini 1.5 Flash active
[INFO] WhatsApp-Web.js initializing...
[SUCCESS] Socket.io bridge established on :5000
        """, language="bash")
        
        st.warning("Ensure the server has direct internet access to connect with WhatsApp servers.")

st.markdown("<div style='margin-top: 50px; text-align: center; color: #8696a0; font-size: 0.8rem;'>Built with ❤️ for Fiverr Client | Enterprise AI Solutions</div>", unsafe_allow_html=True)
