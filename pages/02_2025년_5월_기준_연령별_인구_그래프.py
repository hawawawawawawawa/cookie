import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# CSV 파일 불러오기
df = pd.read_csv("2025_05_population.csv", encoding="cp949")

# 사용할 행정구역 필터링
target_areas = ["경기도", "서울특별시", "부산광역시", "경상남도", "인천광역시"]
df = df[df["행정구역"].isin(target_areas)]

# 지역 중심 좌표 설정 (예시 좌표, 필요 시 조정)
area_coords = {
    "서울특별시": [37.5665, 126.9780],
    "경기도": [37.4138, 127.5183],
    "인천광역시": [37.4563, 126.7052],
    "부산광역시": [35.1796, 129.0756],
    "경상남도": [35.4606, 128.2132]
}

# 지도 중심점 계산
center_lat = sum([area_coords[area][0] for area in target_areas]) / len(target_areas)
center_lon = sum([area_coords[area][1] for area in target_areas]) / len(target_areas)

# 지도 생성
m = folium.Map(location=[center_lat, center_lon], zoom_start=7)

# 원 추가
for _, row in df.iterrows():
    area = row["행정구역"]
    total_pop = row["2025년05월_계_총인구수"]
    lat, lon = area_coords[area]

    # 원 마커 생성
    folium.CircleMarker(
        location=[lat, lon],
        radius=15,
        color="blue",
        fill=True,
        fill_color="blue",
        fill_opacity=0.4,
        popup=f"{area}<br>총인구: {total_pop:,}명"
    ).add_to(m)

# Streamlit에 지도 렌더링
st.title("2025년 5월 기준 연령별 인구수")
st_data = st_folium(m, width=700, height=500)
