import streamlit as st
import google.generativeai as genai

# 直接設定金鑰，跳過 Secrets 保險箱
api_key = "AIzaSyD_POBR0drNvPlcx8Y9g8hRDHFHdnzQkZ4"

# 初始化 Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("業務部 ERP 資料助理 (測試版)")
st.caption("目前運作模式：直接讀取內嵌金鑰模式")

# 模擬讀取 ERP 資料 (這裡之後可以對接你的 test.txt)
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
            # 結合 ERP 資料與使用者問題
            full_prompt = f"請根據以下資料回答問題：\n{erp_context}\n\n問題：{prompt}"
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"AI 回應發生錯誤: {e}")
