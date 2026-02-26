import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime
import pytz

# --- 1. 核心設定校對 ---
api_key = st.secrets["GEMINI_API_KEY"].strip()
genai.configure(api_key=api_key)
# 使用你唯一成功的模型名稱
model = genai.GenerativeModel('gemini-2.5-flash')
tw_tz = pytz.timezone('Asia/Taipei')

# --- 2. 頁面配置 ---
st.set_page_config(page_title="產銷資料庫", layout="wide")
st.title("📊 產銷資料庫") # 恢復抬頭

# --- 3. 初始化權限清單 (Session State) ---
if "user_auth" not in st.session_state:
    # 預設管理員工號與姓名
    st.session_state.user_auth = {"113059": "管理員"}
if "login_logs" not in st.session_state:
    st.session_state.login_logs = []

# --- 4. 側邊欄：系統認證介面 ---
with st.sidebar:
    st.header("🔐 系統認證")
    input_id = st.text_input("工號", placeholder="請輸入工號")
    input_pw = st.text_input("密碼", type="password", placeholder="請輸入密碼")
    
    # 權限驗證邏輯
    is_admin = (input_id == "113059" and input_pw == "tl888")
    is_authorized_user = (input_id in st.session_state.user_auth and input_pw == "tl888")

    if is_admin or is_authorized_user:
        user_name = st.session_state.user_auth.get(input_id, "使用者")
        current_time = datetime.now(tw_tz).strftime('%Y-%m-%d %H:%M:%S')
        
        # 自動紀錄登入日誌
        if "active_user" not in st.session_state or st.session_state.active_user != input_id:
            st.session_state.login_logs.append({
                "時間": current_time, "工號": input_id, "姓名": user_name, "動作": "登入"
            })
            st.session_state.active_user = input_id

        st.success(f"✅ 已授權：{user_name}")
        st.info(f"📁 連動資料夾：營業部資料測試") # 顯示連動狀態
        
        if st.button("🔴 登出系統"):
            st.session_state.login_logs.append({
                "時間": datetime.now(tw_tz).strftime('%Y-%m-%d %H:%M:%S'),
                "工號": input_id, "姓名": user_name, "動作": "登出"
            })
            st.session_state.active_user = None
            st.rerun()

# --- 5. 主畫面：功能分頁 ---
if is_admin:
    # 管理員專屬分頁
    tab1, tab2, tab3 = st.tabs(["🤖 AI 助理分析", "👥 帳號管理", "📜 登入日誌"])
    
    with tab1:
        prompt = st.chat_input("請輸入關於產銷資料夾的問題...")
        if prompt:
            with st.chat_message("assistant"):
                try:
                    # 模擬雲端檔案分析
                    response = model.generate_content(f"請分析雲端硬碟內的所有產銷檔案
