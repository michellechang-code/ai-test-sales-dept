import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime
import pytz  # 處理台灣時間

# --- 1. 核心校對設定 ---
# 確保從 Secrets 讀取金鑰
api_key = st.secrets["GEMINI_API_KEY"].strip()
genai.configure(api_key=api_key)
# 沿用你唯一成功接通的模型名稱
model = genai.GenerativeModel('gemini-2.5-flash')

# 台灣時區設定
tw_tz = pytz.timezone('Asia/Taipei')

# --- 2. 頁面配置 ---
st.set_page_config(page_title="產銷資料庫", layout="wide")
st.title("📊 產銷資料庫") # 恢復你要求的抬頭

# --- 3. 初始化 Session State (存放登入紀錄) ---
if "user_list" not in st.session_state:
    # 預設允許的工號與姓名
    st.session_state.user_list = {"ADMIN": "管理員", "TL001": "張小明"}
if "login_logs" not in st.session_state:
    st.session_state.login_logs = []

# --- 4. 側邊欄：登入系統 ---
with st.sidebar:
    st.header("🔐 系統認證")
    input_id = st.text_input("工號", placeholder="請輸入工號")
    input_pw = st.text_input("密碼", type="password", placeholder="請輸入密碼")
    
    # 驗證邏輯
    is_admin = (input_pw == "tl888" and input_id == "ADMIN")
    is_user = (input_pw == "tl888" and input_id in st.session_state.user_list)

    if is_admin or is_user:
        current_time = datetime.now(tw_tz).strftime('%Y-%m-%d %H:%M:%S')
        user_name = st.session_state.user_list.get(input_id, "管理員")
        
        # 紀錄登入 (僅在切換狀態時紀錄一次)
        if "last_login" not in st.session_state or st.session_state.last_login != input_id:
            st.session_state.login_logs.append({
                "時間": current_time, "工號": input_id, "姓名": user_name, "動作": "登入"
            })
            st.session_state.last_login = input_id

        st.success(f"✅ 歡迎，{user_name}")
        st.write(f"🕒 登入時間：{current_time}")
        
        st.divider()
        # 顯示雲端資料夾連動狀態
        st.info("📁 連動資料夾：營業部資料測試")
        st.caption("ID: 1OqpfW7lzCLnjPRmcDjAR_qXgX9PhPLgf")
        
        if st.button("🔴 登出系統"):
            st.session_state.login_logs.append({
                "時間": datetime.now(tw_tz).strftime('%Y-%m-%d %H:%M:%S'),
                "工號": input_id, "姓名": user_name, "動作": "登出"
            })
            st.session_state.last_login = None
            st.rerun()

# --- 5. 主畫面：功能分頁 ---
if is_admin:
    tab1, tab2, tab3 = st.tabs(["🤖 AI 助理分析", "👥 管理員：帳號管理", "📜 管理員：登入日誌"])
    
    with tab1:
        st.header("🤖 AI 產銷助手")
        prompt = st.chat_input("請輸入關於雲端資料夾的問題...")
        if prompt:
            with st.chat_message("assistant"):
                try:
                    # 模擬分析雲端檔案邏輯
                    response = model.generate_content(f"分析雲端資料夾並回答：{prompt}")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"分析失敗：{str(e)}")

    with tab2:
        st.header("新增允許登入人員")
        new_id = st.text_input("新工號")
        new_name = st.text_input("新姓名")
        if st.button("確認授權"):
            if new_id and new_name:
                st.session_state.user_list[new_id] = new_name
                st.success(f"已授權：{new_name} ({new_id})")
            else:
                st.warning("請完整輸入工號與姓名")

    with tab3:
        st.header("系統登入/登出紀錄")
        df_logs = pd.DataFrame(st.session_state.login_logs)
        if not df_logs.empty:
            st.dataframe(df_logs.sort_values(by="時間", ascending=False), use_container_width=True)
        else:
            st.info("目前尚無登入紀錄")

elif is_user:
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
    st.info("👈 請在左側輸入工號與密碼 (tl888) 以解鎖產銷資料庫。")
