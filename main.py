import streamlit as st
import google.generativeai as genai

# 已修正：將第 9 個字元從英文字母 O 改為數字 0
api_key = "AIzaSyD_P0BROdrNvPlcx8Y9g8hRDHFHdnzQkZ4"

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("業務部 ERP 資料助理 (最終正確版)")
st.caption("連線狀態：金鑰字元修正模式")

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
            full_prompt = f"請根據以下資料回答問題：\n{erp_context}\n\n問題：{prompt}"
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Google API 報錯細節：{str(e)}")
