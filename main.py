import streamlit as st
import google.generativeai as genai

# 1. 安全檢查：確認 Secrets 中是否有金鑰
if "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ 尚未偵測到 API 金鑰！請在 Streamlit Secrets 中設定 GEMINI_API_KEY。")
    st.stop()

# 2. 讀取金鑰並配置 (已確保字元校對為 P0B，非 POB)
api_key = st.secrets["GEMINI_API_KEY"].strip()
genai.configure(api_key=api_key)

# 3. 核心修正：使用通用模型名稱 gemini-pro，徹底跳過 1.5 版本
# 這是為了對接你的 2.5/3.0 帳號環境
model = genai.GenerativeModel('gemini-pro')

st.title("業務部 ERP 資料助理 (正規修正版)")
st.caption("連線狀態：Secrets 環境變數模式 (Gemini-Pro)")

# 你的 ERP 資料內容
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
            # 萬一還有問題，這裡會抓到最底層的錯誤代碼
            st.error(f"連線失敗原因：{str(e)}")
