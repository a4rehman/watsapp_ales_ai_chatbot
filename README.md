# 🚗 Car Showroom AI Pro: WhatsApp Sales Bot

A premium WhatsApp Automation solution powered by **Google Gemini AI**. This bot acts as a 24/7 Car Sales & Service Assistant for your showroom, handling customer inquiries in English and Hindi.

## 🌟 Key Features
- **Google Gemini 1.5 Flash**: Lightning-fast, intelligent responses.
- **WhatsApp Web Integration**: Scan QR code to connect - no Twilio/Official API costs.
- **Premium Admin Dashboard**: Built with Streamlit for easy monitoring and control.
- **Secure Access**: Password-protected administrative controls.
- **Live Status Hub**: Monitor activity and connection status in real-time.

---

## 🛠️ Local Setup

### Prerequisites
- [Node.js](https://nodejs.org/) (v16+)
- [Python 3.9+](https://www.python.org/)

### 1. Clone & Install
```bash
# Install Node.js dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY='your_google_gemini_api_key'
ACCESS_CODE='your_secure_admin_code'
```

### 3. Run the Application
Start the Streamlit Admin Dashboard:
```bash
streamlit run app_streamlit.py
```
Then, use the "Launch AI Bot" button from the dashboard to start the WhatsApp engine.

---

## ☁️ Streamlit Cloud Deployment Guide

To deploy this project successfully on Streamlit Cloud, follow these steps:

### 1. Repository Structure
Ensure your GitHub repository contains these critical files:
- `index.js` (Node.js engine)
- `app_streamlit.py` (Main Python entry)
- `package.json` (Node dependencies)
- `requirements.txt` (Python dependencies)
- `packages.txt` (System dependencies for Chromium/Node)

### 2. Streamlit Cloud Settings
1. Go to [Streamlit Cloud](https://share.streamlit.io/).
2. Create a new app from your repo.
3. **Main file path**: `app_streamlit.py`
4. **Environment Variables (Secrets)**:
   Add your keys in the Streamlit Dashboard (Settings > Secrets):
   ```toml
   ACCESS_CODE = "your_code"
   GEMINI_API_KEY = "your_key"
   ```

### 3. Note on Cloud Environments
*Note: Since Streamlit Cloud doesn't support persistent disk storage by default, you may need to re-scan the QR code if the container restarts. For production-grade 24/7 hosting, consider a VPS or Railway.app.*

---

**Developed for Fiverr Client by AI Engineer Abdul Rehman**
