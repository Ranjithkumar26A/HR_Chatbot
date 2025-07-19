import warnings
import pandas as pd
import streamlit as st 
from main import Main_function

st.set_page_config(page_title="HR support", layout="wide")



with st.sidebar:
        st.sidebar.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

        [data-testid="stSidebar"] {
            background: linear-gradient(to bottom, #0d0d0d, #1a1a1a, #2a2a2a);
            font-family: 'Inter', sans-serif;
            padding: 20px;
            min-height: 100vh;
            border-right: 4px solid transparent;
            border-image: linear-gradient(to bottom, #ff6a00, #ee0979);
            border-image-slice: 1;
            animation: gradientFlow 20s ease infinite, fadeInSlide 0.7s ease-out;
            background-size: 400% 400%;
        }

        @keyframes gradientFlow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        @keyframes fadeInSlide {
        0% { opacity: 0; transform: translateX(-20px); }
        100% { opacity: 1; transform: translateX(0); }
        }

        .sidebar-header {
            font-size: 24px;
            font-weight: 700;
            text-align: center;
            background: linear-gradient(to right, #ff6a00, #ee0979);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 25px;
            animation: pulseIcon 2s infinite ease-in-out;
        }

        .sidebar-header span {
            margin-left: 10px;
        }

        @keyframes pulseIcon {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
        }

        .typing-container {
            font-size: 14.5px;
            line-height: 1.6;
            border-left: 3px solid #ff6a00;
            padding-left: 15px;
            animation: fadeInText 1s ease-out forwards;
            color: #f0f0f0;
            margin-bottom: 30px;
            max-width: 90%;
        }

        .typing-container::after {
            content: '|';
            animation: blink 0.8s infinite;
            margin-left: 2px;
            color: #ff6a00;
            font-weight: bold;
        }

        @keyframes blink {
            0% { opacity: 1; }
            50% { opacity: 0; }
            100% { opacity: 1; }
        }

        @keyframes fadeInText {
            0% { opacity: 0; transform: translateY(10px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        /* Add-on Features Section */
        .feature-section {
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid #333;
        }

        .feature-title {
            font-size: 15px;
            font-weight: 600;
            color: #ff6a00;
            margin-bottom: 10px;
        }

        .feature-item {
            display: flex;
            align-items: center;
            margin: 8px 0;
            color: #f5f5f5;
            font-size: 14px;
            transition: all 0.2s ease;
        }

        .feature-item:hover {
            color: #ee0979;
            transform: translateX(5px);
        }

        .feature-item i {
            margin-right: 10px;
            font-size: 16px;
        }
        </style>

        <div class="sidebar-header">💼 <span>HR Support</span></div>

        <div class="typing-container">
            I’m your intelligent HR assistant.<br>
            Instantly answer questions about leave, policies, or benefits.<br>
            Secure, helpful, and always available.
        </div>

        <div class="feature-section">
            <div class="feature-title">🔍 How I Can Help</div>
            <div class="feature-item"><i>📅</i> Check Leave Balance</div>
            <div class="feature-item"><i>📖</i> Search HR Policies</div>
            <div class="feature-item"><i>💰</i> View Payslips</div>
            <div class="feature-item"><i>🛠️</i> Raise a Support Ticket</div>
        </div>
        """, unsafe_allow_html=True)


def Response_function(user_input):
     Final_response = Main_function(user_input)
     return Final_response



if "message" not in st.session_state:
    st.session_state.message = []


user_input = st.chat_input('Ask your queryy...')

if user_input:
    with st.spinner("Fetching data"):
        response = Response_function(user_input)
        st.session_state.message.append({"role":"user","content":user_input})
        st.session_state.message.append({"role":"assistant","content":response})


    for message in st.session_state.message:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            