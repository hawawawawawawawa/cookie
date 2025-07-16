import streamlit as st
import pandas as pd

# CSV 파일 로딩
@st.cache_data
def load_data():
    df = pd.read_csv('202505_202505_연령별인구현황_월간.csv', encoding='euc-kr')
    return df

df = load_data()

st.title("2025년 5월 기준 연령별 인구 현황 분석")

# 원본 데이터 표시
st.subheader("원본 데이터")
st.dataframe(df)

# 전처리
age_columns = [col for col in df.columns if col.startswith("2025년05월_계_")]
age_labels = [col.replace("2025년05월_계_", "") for col in age_columns]
df_age = df[["행정기관", "총인구수"] + age_columns].copy()
df_age.columns = ["행정기관", "총인구수"] + age_labels

# 총인구수 기준 상위 5개 행정구역 추출
top5 = df_age.sort_values("총인구수", ascending=False).head(5)

# 연령별 인구 수 데이터만 추출하여 숫자형 변환
age_data = top5.set_index("행정기관").drop(columns=["총인구수"])
age_data = age_data.apply(pd.to_numeric, errors='coerce').transpose()

# 시각화
st.subheader("상위 5개 행정구역 연령별 인구 변화 (선 그래프)")
st.line_chart(age_data)

# 참고 안내
st.caption("※ 연령은 세로축, 인구는 가로축(시간 흐름 아님)에 표시됩니다.")
