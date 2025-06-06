# app.py
import streamlit as st
import openai
from datetime import datetime

api_key_ = st.secrets["OPENAI_API_KEY"]
# OpenAI API 초기화
client = openai.OpenAI(
    api_key= api_key_
)

# 세션 상태 초기화 (처음에만)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

if "chat_log" not in st.session_state:
    st.session_state.chat_log = f"\n=== 대화 시작: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n"

# Streamlit UI 구성
st.title("💬 GPT-3.5 Chatbot (Streamlit 버전)")
st.write("아래에 메시지를 입력하세요. 'exit'은 필요 없습니다. 😊")

# 사용자 입력
user_input = st.text_input("👤 나:", key="user_input")

# 전송 버튼 누르면 처리
if st.button("전송"):
    if user_input:
        # 메시지 추가
        st.session_state.messages.append({"role": "user", "content": user_input})

        try:
            # OpenAI API 호출
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )

            reply = response.choices[0].message.content.strip()

            # assistant 응답 추가
            st.session_state.messages.append({"role": "assistant", "content": reply})

            # 로그 업데이트
            st.session_state.chat_log += f"👤 나: {user_input}\n"
            st.session_state.chat_log += f"🤖 챗봇: {reply}\n\n"

        except Exception as e:
            st.error(f"⚠️ 오류 발생: {e}")

# 이전 대화 출력
st.subheader("📝 대화 내용")
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**👤 나:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**🤖 챗봇:** {msg['content']}")

# 로그 저장 버튼
if st.button("💾 대화 로그 저장"):
    log_filename = "chat_log.txt"
    with open(log_filename, "a", encoding="utf-8") as log_file:
        log_file.write(st.session_state.chat_log)
    st.success(f"대화 로그가 {log_filename} 에 저장되었습니다!")
