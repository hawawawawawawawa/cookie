import streamlit as st
import pandas as pd

df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding="euc-kr")

st.title("열 이름 확인용 도우미")
st.write(df.columns.tolist())
