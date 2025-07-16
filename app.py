import streamlit as st
import pandas as pd

# CSV 로드
@st.cache_data
def load_data():
    return pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding="euc-kr")

df = load_data()

st.title("2025년 5월 기준 연령별 인구 현황 분석")

# 열 이름 확인
st.subheader("📋 열 이름 목록")
st.write(df.columns.tolist())

# 전처리
age_columns = [col for col in df.columns if col.startswith("2025년05월_계_")]
age_labels = [col.replace("2025년05월_계_", "") for col in age_columns]

# 실제 열 이름에 맞게 수정 (예시는 꼭 실제 출력 보고 고치기!)
real_region_col = "행정구역"
real_total_col = "총인구수 (명)"

# 추출 및 컬럼명 정리
df_age = df[[real_region_col, real_total_col] + age_columns].copy()
df_age.columns = ["행정구역", "총인구수"] + age_labels

# 상위 5개 행정구역
top5 = df_age.sort_values("총인구수", ascending=False).head(5)

# 연령별 인구 수 전처리
age_data = top5.set_index("행정구역").drop(columns=["총인구수"])
age_data = age_data.apply(pd.to_numeric, errors='coerce').transpose()

# 시각화
st.subheader("상위 5개 행정구역 연령별 인구 변화 (선 그래프)")
st.line_chart(age_data)

# 안내
st.caption("※ 연령은 세로축, 인구는 가로축에 표시됩니다.")
