import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="연도별 학급당 학생 수", layout="wide")

st.title("📊 연도별 학급당 학생 수 시각화")
st.markdown("2025년 5월 기준 데이터를 기반으로 작성된 시각화입니다.")

# CSV 파일 불러오기 (EUC-KR 인코딩)
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, encoding='euc-kr')

        # '연도' 열이 있는 경우 정수형으로 변환
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

    except Exception as e:
        st.error(f"파일을 불러오는 중 오류가 발생했습니다: {e}")
else:
    st.info("왼쪽 상단에서 CSV 파일을 업로드해주세요.")
