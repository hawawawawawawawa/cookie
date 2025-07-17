pip install plotly
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import re

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

# 연령 구간 문자열 → 숫자 변환 함수 (끝 숫자 추출)
def age_to_number(label):
    nums = re.findall(r'\d+', label)
    if nums:
        return int(nums[-1])  # 마지막 숫자 사용 ('100 이상' -> 100, '1000 이상' -> 1000)
    else:
        return -1  # 숫자 없으면 -1 (미취학 등)

age_numbers = [age_to_number(x) for x in age_data.index]
age_data['age_num'] = age_numbers

# 숫자 오름차순 정렬
age_data = age_data.sort_values('age_num')

# plotly 그래프 생성
fig = go.Figure()

for region in age_data.columns.drop('age_num'):
    fig.add_trace(go.Scatter(
        x=age_data['age_num'],
        y=age_data[region],
        mode='lines+markers',
        name=region
    ))

# x축 눈금 라벨을 원래 연령 문자열로 바꾸기 위한 ticktext, tickvals 설정
fig.update_layout(
    xaxis=dict(
        tickmode='array',
        tickvals=age_data['age_num'],
        ticktext=age_data.index.tolist(),
        title='연령',
    ),
    yaxis=dict(title='인구 수'),
    title='상위 5개 행정구역 연령별 인구 변화'
)

st.plotly_chart(fig, use_container_width=True)

# 원본 데이터도 같이 보여주기
st.subheader("원본 데이터 (일부)")
st.dataframe(df.head(20))
