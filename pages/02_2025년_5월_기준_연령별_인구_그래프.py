import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# CSV 로드 함수
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

# 상위 5개 행정구역 이름으로 필터 (직접 지정)
selected_regions = ["경기도", "서울", "부산", "경상남도", "인천"]
top5 = df_age[df_age["행정구역"].isin(selected_regions)].copy()

# 각 행정구역별 대표 위도, 경도 (대략적인 중심 좌표)
location_data = {
    "행정구역": ["서울", "경기도", "부산", "경상남도", "인천"],
    "lat": [37.5665, 37.4138, 35.1796, 35.1796, 37.4563],
    "lon": [126.9780, 127.5183, 129.0756, 128.6936, 126.7052]
}
loc_df = pd.DataFrame(location_data)

# top5와 위치정보 병합
map_df = pd.merge(top5, loc_df, on="행정구역", how="inner")

# 지도 중심 좌표 설정 (중심점 평균)
center_lat = map_df["lat"].mean()
center_lon = map_df["lon"].mean()

# NaN 제거 후 중심 좌표 계산
valid_coords = df[['위도', '경도']].dropna()
center_lat = valid_coords['위도'].mean()
center_lon = valid_coords['경도'].mean()

# folium 지도 생성
m = folium.Map(location=[center_lat, center_lon], zoom_start=7)


# folium 지도 생성
m = folium.Map(location=[center_lat, center_lon], zoom_start=7)

# 인구수에 따라 마커 원 크기 조절
for _, row in map_df.iterrows():
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=max(row["총인구수"] / 100000, 5),  # 최소 반경 5, 인구수에 비례 확대
        color="blue",
        fill=True,
        fill_color="blue",
        fill_opacity=0.5,
        popup=f"{row['행정구역']}: {row['총인구수']:,}명"
    ).add_to(m)

st.subheader("상위 5개 행정구역 인구 분포 지도")
st_folium(m, width=700, height=500)

st.subheader("원본 데이터 (일부)")
st.dataframe(df.head(20))
