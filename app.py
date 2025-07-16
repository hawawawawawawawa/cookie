import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding="euc-kr")

df = load_data()

st.title("2025년 5월 기준 연령별 인구 현황 분석")

region_col = "행정구역"
total_col = "2025년05월_계_총인구수"
age_columns = [col for col in df.columns if col.startswith("2025년05월_계_") and "세" in col]
age_labels = [col.replace("2025년05월_계_", "") for col in age_columns]

df_age = df[[region_col, total_col] + age_columns].copy()
df_age.columns = ["행정구역", "총인구수"] + age_labels

top5 = df_age.sort_values("총인구수", ascending=False).head(5)

age_data = top5.set_index("행정구역").drop(columns=["총인구수"])
age_data = age_data.apply(pd.to_numeric, errors='coerce').transpose()

# 인덱스(연령) 목록 출력 (순서대로 정렬 기준 만들기 위해)
all_age_labels = age_data.index.tolist()

# 숫자만 있는 구간 추출 및 정렬
def age_key(x):
    try:
        return int(x.replace("세",""))
    except:
        # 숫자 아닌 구간은 큰 수로 처리해 뒤로 보냄
        return 9999

sorted_ages = sorted(all_age_labels, key=age_key)

# 정렬 순서에 맞게 데이터 재배열
age_data = age_data.loc[sorted_ages]

st.subheader("상위 5개 행정구역 연령별 인구 변화 (선 그래프)")
st.line_chart(age_data)

st.subheader("원본 데이터 (일부)")
st.dataframe(df.head(20))

st.caption("※ 연령은 세로축, 인구는 가로축에 표시됩니다.")
