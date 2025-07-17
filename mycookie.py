import streamlit as st
import pandas as pd

st.set_page_config(page_title="연도별 학급당 학생 수", layout="wide")
st.title("📊 연도별 학급당 학생 수 시각화")

try:
    df = pd.read_csv("년도별학급당학생수.csv", encoding='utf-8')
except FileNotFoundError:
    st.error("년도별학급당학생수.csv 파일을 찾을 수 없습니다.")
except Exception as e:
    st.error(f"데이터 로드 중 오류가 발생했습니다: {e}")
else:
    if '연도' in df.columns:
        df['연도'] = pd.to_numeric(df['연도'], errors='coerce')
        df = df.dropna(subset=['연도'])
        df['연도'] = df['연도'].astype(int)

        # 예를 들어 '평균학급당학생수' 컬럼이 있다고 가정
        if '평균학급당학생수' in df.columns:
            df_chart = df.set_index('연도')['평균학급당학생수']
            st.line_chart(df_chart)
        else:
            # 여러 컬럼을 모두 사용
            school_columns = [col for col in df.columns if col != '연도']
            df_chart = df.set_index('연도')[school_columns]
            st.line_chart(df_chart)

        st.markdown("✅ 데이터 출처: 2025년 5월 기준 교육 통계")
    else:
        st.error("데이터에 '연도' 컬럼이 없습니다.")
