import streamlit as st
import google.generativeai as genai
import pandas as pd

# 1. 初始化 (請務必使用新的金鑰)
api_key = st.secrets["GEMINI_API_KEY"].strip()
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash') # 使用最穩定的 1.5 版本

# 2. 定義檔案 ID
# 注意：這裡請填入「實績表」試算表本身的 ID
ACTUAL_SHEET_ID = "1OqpfW7lzCLnjPRmcDjAR_qXgX9PhPLgf" 

def get_data_from_google(sheet_id):
    # 強制匯出成 CSV 以便 AI 讀取數字
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    try:
        df = pd.read_csv(url)
        return df.to_string(index=False)
    except Exception as e:
        return f"無法讀取數據內容：{str(e)}"

st.title("📊 產銷資料庫")

# 3. 登入認證
with st.sidebar:
    u_id = st.text_input("工號", value="113059")
    u_pw = st.text_input("密碼", type="password", value="tl888")
    is_auth = (u_id == "113059" and u_pw == "tl888")

if is_auth:
    # 預先加載數據
    with st.spinner("同步雲端產銷數據中..."):
        raw_data = get_data_from_google(ACTUAL_SHEET_ID)
    
    prompt = st.chat_input("請輸入問題 (例如：2026年1月接單總金額多少？)")
    
    if prompt:
        with st.chat_message("assistant"):
            try:
                # 強制 AI 只看數據回答，嚴禁廢話
                command = f"你是精確的產銷分析官。請根據以下數據回答，若無數據請說找不到，不要閒聊：\n\n{raw_data}\n\n問題：{prompt}"
                response = model.generate_content(command)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"連線失敗：{str(e)}") # 捕捉 403 漏金鑰報錯
else:
    st.info("👈 請在左側輸入認證資訊。")
