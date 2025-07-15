import streamlit as st
st.latex(r"""
\lim_{x \to \infty}\frac{x^2+2x+a}{x^2}=a , a = ?
""")
answer = st.selectbox(
    "정답을 입력하세요",
    ["1", "2", "3", "4"]
)
