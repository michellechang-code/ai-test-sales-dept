import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime
import pytz

# --- 1. 核心設定校對 ---
# 確保 API Key 字元 P0B 正確
api_key = st.secrets["GEMINI_API_KEY"].strip()
genai.configure(api_key=api_key)

# 使用你唯一成功接通的模型名稱
model = genai.GenerativeModel('gemini-2.5-flash')
tw_tz = pytz.timezone('Asia/Taipei')

# --- 2. 頁面配置與抬頭 ---
st.set_page_config(page_title="產銷資料庫", layout="wide")
st.title("📊 產銷資料庫") 

# --- 3. 初始化 Session State ---
if "user_auth" not in st.session_state:
    # 管理員預設工號 113059
    st.session_state.user_auth = {"113059": "管理員"}
if "login_logs" not in st.session_state:
    st.session_state.login_logs = []

# --- 4. 側邊欄：認證介面 ---
with st.sidebar:
    st.header("🔐 系統認證")
    input_id = st.text_input("工號", placeholder="請輸入工號")
    input_pw = st.text_input("密碼", type="password", placeholder="請輸入密碼")
    
    # 管理員與員工驗證
    is_admin = (input_id == "113059" and input_pw == "tl888")
    is_authorized_user = (input_id in st.session_state.user_auth and input_pw == "tl888")

    if is_admin or is_authorized_user:
        user_name = st.session_state.user_auth.get(input_id, "使用者")
        current_time = datetime.now(tw_tz).strftime('%Y-%m-%d %H:%M:%S')
        
        if "active_user" not in st.session_state or st.session_state.active_user != input_id:
            st.session_state.login_logs.append({
                "時間": current_time, "工號": input_id, "姓名": user_name, "動作": "登入"
            })
            st.session_state.active_user = input_id

        st.success(f"✅ 已授權：{user_name}")
        st.info("📁 連動資料夾：營業部資料測試") #
        
        if st.button("🔴 登出系統"):
            st.session_state.login_logs.append({
                "時間": datetime.now(tw_tz).strftime('%Y-%m-%d %H:%M:%S'),
                "工號": input_id, "姓名": user_name, "動作": "登出"
            })
            st.session_state.active_user = None
            st.rerun()

# --- 5. 主畫面：分頁與功能 ---
if is_admin:
    # 管理員後台：分析、管理、日誌
    tab1, tab2, tab3 = st.tabs(["🤖 AI 助理分析", "👥 帳號管理", "📜 登入日誌"])
    
    with tab1:
        st.header("🤖 AI 產銷助手")
        prompt = st.chat_input("請針對雲端產銷資料提問...")
        if prompt:
            with st.chat_message("assistant"):
                try:
                    # 修正第 68 行引號問題
                    analysis_prompt = f"請分析雲端硬碟內的產銷檔案：{prompt}"
                    response = model.generate_content(analysis_prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"分析失敗：{str(e)}")

    with tab2:
        st.header("管理員：授權新成員")
        new_id = st.text_input("新增工號", key="new_staff_id")
        new_name = st.text_input("員工姓名", key="new_staff_name")
        if st.button("確認授權"):
            if new_id and new_name:
                st.session_state.user_auth[new_id] = new_name
                st.success(f"已授權：{new_name} ({new_id})")
            else:
                st.warning("請填寫完整資訊")

    with tab3:
        st.header("系統登入日誌")
        if st.session_state.login_logs:
            df_logs = pd.DataFrame(st.session_state.login_logs)
            st.dataframe(df_logs.sort_values(by="時間", ascending=False), use_container_width=True)
        else:
            st.info("尚無紀錄")

elif is_authorized_user:
    # 一般員工介面
    st.header("🤖 產銷 AI 助理")
    prompt = st.chat_input("請輸入您的產銷疑問...")
    if prompt:
        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"連線失敗：{str(e)}")

else:
    # 未登入顯示，已移除密碼提示 (tl888)
    st.info("👉 請在左側輸入工號與密碼以解鎖產銷資料庫。")
