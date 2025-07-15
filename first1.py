import streamlit as st
st.title('나의 첫 웹 서비스 만들기!!')
st.latex(r"""
\lim_{x \to \infty} {\(x^2+2x+a\)}^2
""")
name = st.text_input('이름을 입력해주세요 : ')
menu = st.selectbox('좋아하는 음식을 선택해주세요:', ['냉모밀','쌀국수','돈까스','짜장면'])
if st.button('인사말 생성') : 
  st.write(name+'님! 당신이 좋아하는 음식은 '+menu+'이군요?! 저도 좋아요!!')
