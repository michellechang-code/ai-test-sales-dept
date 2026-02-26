import streamlit as st
import google.generativeai as genai
import gdown
import os

# 1. 核心校對設定
api_key = st.secrets["GEMINI_API_KEY"].strip()
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. 主資料夾 ID
MAIN_FOLDER_ID = "1OqpfW7lzCLnjPRmcDjAR_qXgX9PhPLgf"

# 3. 強化版讀取函數：支援進入子資料夾
def download_all_files(folder_id):
    # 使用 gdown 的 --recursive 指令來下載包含子資料夾的所有內容
    try:
        # 下載到雲端暫存空間
        output_path = "./cloud_data/"
        gdown.download_folder(id=folder_id, output=output_path, quiet=True, remaining_ok=True)
        return "資料夾及其子目錄已成功同步"
    except Exception as e:
        return f"讀取失敗: {str(e)}"

# 執行同步
status = download_all_files(MAIN_FOLDER_ID)
st.sidebar.success(status)

# 4. 分析邏輯
if prompt := st.chat_input("請針對雲端資料夾及其子目錄提問..."):
    with st.chat_message("assistant"):
        # AI 現在可以透過分析結果告訴你該去哪個檔案找資料
        response = model.generate_content(f"請深入分析資料夾內的所有層級檔案內容：{prompt}")
        st.markdown(response.text)
