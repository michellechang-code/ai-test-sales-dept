import streamlit as st
import google.generativeai as genai
import pandas as pd

# 1. 核心校對設定
api_key = st.secrets["GEMINI_API_KEY"].strip()
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash') # 沿用唯一成功的模型

# 2. 定義雲端檔案 ID (來自 image_c024c0.png)
files_to_read = {
    "實績表": "1OqpfW7lzCLnjPRmcDjAR_qXgX9PhPLgf", # 主資料夾 ID，實際應用建議放個別檔案 ID
    "2026年-已接未出統計": "1OqpfW7lzCLnjPRmcDjAR_qXgX9PhPLgf"
}

# 3. 讀取 Google Sheets 函數
def get_excel_data(sheet_id):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
    try:
        df = pd.read_csv(url)
        return df.to_string(index=False)
    except:
        return ""

st.title("📊 產銷資料庫")

# 4. 側邊欄驗證 (維持管理員 113059)
with st.sidebar:
    input_id = st.text_input("工號")
    input_pw = st.text_input("密碼", type="password")
    is_auth = (input_id == "113059" and input_pw == "tl888")

# 5. 主程式：直接餵數據給 AI
if is_auth:
    # 這裡會直接抓取試算表內容作為 AI 的知識庫
    data_context = ""
    for name, fid in files_to_read.items():
        data_context += f"\n--- {name} 內容 ---\n{get_excel_data(fid)}\n"

    prompt = st.chat_input("請輸入產銷問題 (例如：1月接單總金額多少？)")
    if prompt:
        with st.chat_message("assistant"):
            # 強制 AI 根據讀取到的表格數據回答
            full_prompt = f"請根據以下表格數據精確回答：\n{data_context}\n問題：{prompt}"
            res = model.generate_content(full_prompt)
            st.markdown(res.text)
else:
    st.info("👈 請在左側輸入工號與密碼 (113059/tl888) 以解鎖。")
