import streamlit as st
from google import genai

# 페이지 설정
st.set_page_config(
    page_title="연애 상담 AI",
    page_icon="💕",
)

st.title("💕 연애 상담 AI")
st.caption("Gemini 2.5 Flash Lite 기반")

# API 키 확인
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("GEMINI_API_KEY가 Secrets에 설정되어 있지 않습니다.")
    st.stop()

# 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요. 연애 고민을 편하게 이야기해 주세요. "
                "상황을 자세히 설명해 주시면 더 도움이 되는 답변을 드릴 수 있습니다."
            ),
        }
    ]

# 기존 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
prompt = st.chat_input("연애 고민을 입력하세요")

if prompt:
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Gemini용 대화 이력 구성
        history_text = ""

        for msg in st.session_state.messages:
            if msg["role"] == "user":
                history_text += f"사용자: {msg['content']}\n"
            else:
                history_text += f"상담사: {msg['content']}\n"

        system_prompt = """
당신은 공감 능력이 뛰어난 연애 상담 전문가입니다.

규칙:
- 상대방을 비난하지 말 것
- 현실적이고 균형 잡힌 조언 제공
- 충분한 공감 표현
- 위험한 행동을 부추기지 말 것
- 한국어로 답변
"""

        full_prompt = f"""
{system_prompt}

다음은 지금까지의 대화입니다.

{history_text}

상담사 답변:
"""

        with st.chat_message("assistant"):
            with st.spinner("답변 생성 중..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=full_prompt,
                )

                answer = response.text

                st.markdown(answer)

        # 응답 저장
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

    except Exception as e:
        error_message = f"오류가 발생했습니다: {str(e)}"

        with st.chat_message("assistant"):
            st.error(error_message)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": error_message,
            }
        )
