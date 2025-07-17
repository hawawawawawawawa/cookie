import streamlit as st
import pandas as pd
import plotly.express as px

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

        school_columns = [col for col in df.columns if col != '연도']

        if school_columns:
            df_melt = df.melt(id_vars='연도', value_vars=school_columns, var_name='항목', value_name='학생수')

            fig = px.bar(
                df_melt,
                x='학생수',       # 가로 막대 길이
                y='연도',         # 세로축(카테고리)
                color='항목',
                barmode='group',
                orientation='h',  # 여기서 가로 막대 그래프 설정
                title='연도별 학급당 학생 수 (가로 막대 그래프)'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("데이터에 '연도' 외 표시할 학생 수 컬럼이 없습니다.")
        
        st.markdown("✅ 데이터 출처: 2025년 5월 기준 교육 통계")
    else:
        st.error("데이터에 '연도' 컬럼이 없습니다.")
