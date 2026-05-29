import streamlit as st
import random

st.title("🎲 랜덤 뽑기")

items = st.text_area(
    "항목을 한 줄씩 입력하세요",
    "치킨\n피자\n햄버거"
)

if st.button("뽑기"):
    item_list = items.splitlines()
    result = random.choice(item_list)

    st.success(f"선택 결과: {result}")
