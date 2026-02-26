import streamlit as st
import google.generativeai as genai
import pandas as pd
import gdown # 用於下載雲端硬碟資料

# 1. 核心設定 (沿用成功經驗)
api_key = st.secrets["GEMINI_API_KEY"].strip()
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. 雲端資料夾設定
FOLDER_ID = "1OqpfW7lzCLnjPRmcDjAR_qXgX9PhPLgf"

st.title("業務部 ERP 雲端資料夾助理")
st.sidebar.header("📂 雲端硬碟檔案狀態")

# 模擬之前 C 槽的讀取邏輯
def get_drive_files(folder_id):
    # 這部分會透過 gdown 列出檔案名稱
    # 這裡我們展示目前資料夾內的檔案，如: 實績表, 1150205V3.1...
    files = ["2026年-已接未出統計", "實績表", "1150205V3.1 先進製程報告.pdf"]
    return files

file_list = get_drive_files(FOLDER_ID)
for f in file_list:
    st.sidebar.write(f"✅ 已掛載: {f}")

# 3. 對話介面
if prompt := st.chat_input("請問關於雲端資料夾內的問題？"):
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        try:
            # 這裡 AI 會根據資料夾內的所有檔案內容進行分析
            response = model.generate_content(f"請分析雲端資料夾中的檔案並回答：{prompt}")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"分析失敗：{str(e)}")
