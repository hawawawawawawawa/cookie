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

        # '일반계고'와 '일반고' 합쳐서 '고등학교' 컬럼 생성
        df['고등학교'] = df.get('일반계고', 0) + df.get('일반고', 0)

        # 그래프에 사용할 컬럼 리스트 지정 (초등학교, 중학교, 유치원, 고등학교)
        selected_columns = ['초등학교', '중학교', '유치원', '고등학교']

        # 실제 데이터에 없는 컬럼은 제외
        selected_columns = [col for col in selected_columns if col in df.columns]

        if selected_columns:
            df_melt = df.melt(id_vars='연도', value_vars=selected_columns, var_name='항목', value_name='학생수')
            df_melt['연도'] = df_melt['연도'].astype(str)

            fig = px.bar(
                df_melt,
                x='연도',
                y='학생수',
                color='항목',
                barmode='group',
                title='연도별 학급당 학생 수 (초/중/고/유치원)'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("필요한 컬럼이 데이터에 없습니다.")

        st.markdown("✅ 데이터 출처: 2025년 5월 기준 교육 통계")
    else:
        st.error("데이터에 '연도' 컬럼이 없습니다.")
