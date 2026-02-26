import streamlit as st
import google.generativeai as genai
import pandas as pd
import gdown
import os

# 1. 安全讀取金鑰 (校對為數字 0)
api_key = st.secrets["GEMINI_API_KEY"].strip()
genai.configure(api_key=api_key)

# 2. 核心設定：使用你唯一成功過的名稱
model = genai.GenerativeModel('gemini-2.5-flash')

# 3. 雲端資料夾 ID
FOLDER_ID = "1OqpfW7lzCLnjPRmcDjAR_qXgX9PhPLgf"

st.title("業務部 ERP 雲端資料助理")
st.caption("連線狀態：Google Workspace 資料夾模式")

# 模擬 C 槽檔案清單讀取
@st.cache_data
def load_cloud_data(folder_id):
    # 下載雲端資料夾清單 (此處為示意，gdown 會處理實際下載)
    # 針對 image_c024c0.png 內容進行校對
    file_info = "資料夾包含：2026年-已接未出統計, 實績表, 1150205V3.1 報告"
    return file_info

cloud_data = load_cloud_data(FOLDER_ID)

if prompt := st.chat_input("請針對雲端資料夾提問..."):
    with st.chat_message("assistant"):
        try:
            # 結合雲端硬碟內容回答
            full_prompt = f"分析以下雲端資料：\n{cloud_data}\n問題：{prompt}"
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"分析失敗：{str(e)}")
