import streamlit as st
import google.generativeai as genai

# 直接填入你那把「之前能動」的金鑰，請確保引號內沒有任何隱形空格
api_key = "AIzaSyD_POBR0drNvPlcx8Y9g8hRDHFHdnzQkZ4"

# 配置金鑰
genai.configure(api_key=api_key)

# 針對 2.5/3.0 環境帳號，這是目前對接新版 API 最標準的模型代碼
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("業務部 ERP 資料助理 (2.5/3.0 版)")
st.caption("連線狀態：直接金鑰模式")

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
            # 結合 ERP 資料與問題發送給 AI
            full_prompt = f"請根據以下資料回答問題：\n{erp_context}\n\n問題：{prompt}"
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # 如果還是報錯，這行會吐出最原始的 Google 拒絕原因
            st.error(f"Google API 回傳錯誤細節：{str(e)}")
