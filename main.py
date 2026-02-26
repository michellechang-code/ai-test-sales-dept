import streamlit as st
import google.generativeai as genai
import pandas as pd

# 1. 核心校對：使用你唯一成功的模型名稱
api_key = st.secrets["GEMINI_API_KEY"].strip()
genai.configure(api_key=api_key)
# 修正：務必使用 gemini-2.5-flash，這是你帳號唯一成功的路徑
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. 定義實績表檔案 ID (根據 image_c024c0.png 正確檔案)
# 確保這個 ID 是「實績表」這個試算表本身的 ID
DATA_FILE_ID = "1OqpfW7lzCLnjPRmcDjAR_qXgX9PhPLgf" 

def fetch_real_data(file_id):
    # 強制導向 CSV 匯出格式以獲取真實數字
    url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv"
    try:
        df = pd.read_csv(url)
        # 只取前 100 列避免過大報錯，確保 AI 能讀到數據
        return df.head(100).to_string(index=False)
    except Exception as e:
        return f"數據讀取失敗: {str(e)}"

st.title("📊 產銷資料庫")

# 3. 側邊欄認證 (管理員：113059)
with st.sidebar:
    u_id = st.text_input("工號", value="113059")
    u_pw = st.text_input("密碼", type="password", value="tl888")
    is_admin = (u_id == "113059" and u_pw == "tl888")

# 4. 主程式：讀取數據並精確回答
if is_admin:
    # 執行讀取真實 Excel 數據
    real_context = fetch_real_data(DATA_FILE_ID)
    
    prompt = st.chat_input("請輸入問題 (例如：1月接單總金額多少？)")
    if prompt:
        with st.chat_message("assistant"):
            try:
                # 強制 AI 只針對數據回答，不再閒聊
                instruction = f"你是精確的數據分析師。請根據以下產銷數據回答，若無數據請說找不到：\n\n{real_context}\n\n問題：{prompt}"
                response = model.generate_content(instruction)
                st.markdown(response.text)
            except Exception as e:
                # 捕獲 PermissionDenied 或其他 API 報錯
                st.error(f"連線失敗：{str(e)}")
else:
    st.info("👈 請在左側輸入認證資訊。")
