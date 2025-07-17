import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="연도별 학급당 학생 수", layout="wide")

st.title("📊 연도별 학급당 학생 수 시각화")
st.markdown("2025년 5월 기준 데이터를 기반으로 작성된 시각화입니다.")

if True:
    df = pd.read_csv("년도별학급당학생수.csv", encoding='euc-kr')
    if '연도' in df.columns:
        df['연도'] = pd.to_numeric(df['연도'], errors='coerce')
        df = df.dropna(subset=['연도'])
        df['연도'] = df['연도'].astype(int)

        # 학급당 학생 수 열만 추출
    school_columns = [col for col in df.columns if col != '연도']
    df_chart = df.set_index('연도')[school_columns]

    st.subheader("📈 학급당 학생 수 추이")
    st.line_chart(df_chart)

    st.markdown("✅ 데이터 출처: 2025년 5월 기준 교육 통계")
