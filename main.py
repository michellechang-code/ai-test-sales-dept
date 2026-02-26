import streamlit as st
import google.generativeai as genai

# 1. 正規安全讀取模式 (請確保 Streamlit Secrets 裡有存好 GEMINI_API_KEY)
if "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ 尚未偵測到 API 金鑰！請在 Streamlit Secrets 中設定 GEMINI_API_KEY。")
    st.stop()

# 2. 配置金鑰 (校對為成功過的 P0B 格式)
api_key = st.secrets["GEMINI_API_KEY"].strip()
genai.configure(api_key=api_key)

# 3. 核心修正：使用你之前唯一成功過的核心名稱 'gemini-2.5-flash'
model = genai.GenerativeModel('gemini-2.5-flash')

st.title("業務部 ERP 資料助理 (正規安全版)")
st.caption("連線狀態：成功環境對接模式 (Gemini 2.5 Flash)")

# 模擬 ERP 資料內容
erp_context = """
2026年營業目標：1億2千萬新台幣。
主要推廣產品：AI 自動化排程系統、ERP 整合模組。
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("請問關於業務資料的問題？"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # 傳送請求給 AI
            full_prompt = f"請根據以下資料回答問題：\n{erp_context}\n\n問題：{prompt}"
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # 如果失敗，會抓到最底層的錯誤
            st.error(f"連線失敗原因：{str(e)}")
