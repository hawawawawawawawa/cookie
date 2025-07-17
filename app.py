import streamlit as st
import pandas as pd

# CSV 로드 함수
@st.cache_data
def load_data():
    return pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding="euc-kr")

df = load_data()

st.title("2025년 5월 기준 연령별 인구 현황 분석")

# 열 이름 확인용 (선택적으로 주석 처리 가능)
# st.write(df.columns.tolist())

# 전처리
region_col = "행정구역"
total_col = "2025년05월_계_총인구수"
age_columns = [col for col in df.columns if col.startswith("2025년05월_계_") and "세" in col]
age_labels = [col.replace("2025년05월_계_","") for col in age_columns]

# 필요한 열만 추출
df_age = df[[region_col, total_col] + age_columns].copy()
df_age.columns = ["행정구역", "총인구수"] + age_labels  # 열 이름 재정의

# 상위 5개 행정구역 추출
top5 = df_age.sort_values("총인구수", ascending=False).head(5)

# 연령별 인구만 추출 후 숫자 변환
age_data = top5.set_index("행정구역").drop(columns=["총인구수"])
age_data = age_data.apply(pd.to_numeric, errors='coerce').transpose()

# 시각화
st.subheader("상위 5개 행정구역 연령별 인구 변화 (선 그래프)")
st.line_chart(age_data)

st.caption("※ 연령은 세로축, 인구는 가로축에 표시됩니다.")
