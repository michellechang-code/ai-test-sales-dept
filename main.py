import streamlit as st
import google.generativeai as genai
import pandas as pd

# 1. 核心設定：使用目前最穩定的模型名稱
api_key = st.secrets["GEMINI_API_KEY"].strip()
genai.configure(api_key=api_key)
# 修正：改用 gemini-1.5-flash 以避開 403/404 權限問題
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. 雲端檔案 ID (來自你的 Google Drive)
# 注意：這些 ID 必須是個別「檔案」的 ID，而非資料夾 ID
SHEET_IDS = {
    "實績表": "1OqpfW7lzCLnjPRmcDjAR_qXgX9PhPLgf", 
    "2026接單統計": "1OqpfW7lzCLnjPRmcDjAR_qXgX9PhPLgf"
}

def get_data(sid):
    # 強制轉換為 CSV 下載連結
    url = f"https://docs.google.com/spreadsheets/d/{sid}/export?format=csv"
    try:
        df = pd.read_csv(url)
        return df.to_string(index=False)
    except Exception as e:
        return f"(檔案讀取失敗: {str(e)})"

st.title("📊 產銷資料庫")

# 3. 側邊欄驗證 (管理員：113059 / tl888)
with st.sidebar:
    u_id = st.text_input("工號", value="113059")
    u_pw = st.text_input("密碼", type="password", value="tl888")
    is_ok = (u_id == "113059" and u_pw == "tl888")

# 4. 主程式：獲取數據並回答
if is_ok:
    # 這裡會讀取真實數據，解決 AI 空談問題
    with st.spinner("正在讀取雲端產銷數據..."):
        context_data = ""
        for name, sid in SHEET_IDS.items():
            context_data += f"\n[{name}數據]\n{get_data(sid)}\n"

    prompt = st.chat_input("請輸入問題 (例如：1月接單總金額多少？)")
    if prompt:
        with st.chat_message("assistant"):
            try:
                # 結合數據與問題，強制 AI 報數
                full_msg = f"請根據以下產銷數據回答，若無數據請說找不到，不要閒聊：\n{context_data}\n問題：{prompt}"
                res = model.generate_content(full_msg)
                st.markdown(res.text)
            except Exception as e:
                # 這裡會顯示具體的 API 錯誤細節
                st.error(f"API 連線失敗：{str(e)}")
else:
    st.info("👈 請正確輸入認證資訊。")
