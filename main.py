import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# --- 1. 安全與金鑰設定 ---
# 在 Streamlit Cloud 上，這會自動從 Secrets 抓取金鑰
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ 尚未偵測到 API 金鑰！請在 Streamlit Secrets 中設定 GEMINI_API_KEY。")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

# --- 2. 網頁介面配置 ---
st.set_page_config(page_title="業務部 AI 助手", page_icon="📈")
st.title("🤖 業務部 ERP 資料助理 (測試版)")
st.caption("目前運作模式：讀取倉庫內的測試檔案 (test.txt)")

# --- 3. 讀取資料邏輯 ---
def load_context_data():
    # 預設讀取同資料夾下的 test.txt
    file_path = "test.txt"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return "警告：找不到 test.txt 檔案。請上傳該檔案以提供 ERP 參考資料。"

# --- 4. 對話記憶與顯示 ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# 顯示歷史訊息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. 處理用戶提問 ---
if prompt := st.chat_input("請問關於業務資料的問題？"):
    # 存入對話紀錄並顯示
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 呼叫 AI 處理
    with st.chat_message("assistant"):
        with st.spinner("AI 正在分析資料中..."):
            context = load_context_data()
            full_prompt = f"你是一個專業的業務數據分析師。請根據以下資料回答問題：\n\n【資料內容】\n{context}\n\n【用戶問題】\n{prompt}"
            
            try:
                response = model.generate_content(full_prompt)
                answer = response.text
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"AI 回應發生錯誤: {e}")
