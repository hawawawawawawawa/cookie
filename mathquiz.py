import streamlit as st
if "page" not in st.session_state:
    st.session_state.page = 1
    st.latex(r"""
    \lim_{x \to \infty}\frac{x^2+2x+a}{x^2}=a , a = ?
    """)
    answer = st.selectbox(
        "정답을 입력하세요",
        ["1", "2", "3", "4"]
    )
    if st.button('정답 확인') :
        if answer == "1":
            st.title("정답")
            st.write("정답입니다.")
        else :
            st.write("다시 한 번 생각해보세요")
