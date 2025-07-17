import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="2025년 5월 기준 연령별 인구 지도", layout="wide")

st.title("2025년 5월 기준 연령별 인구 지도")
st.write("상위 5개 지역(서울, 경기, 인천, 부산, 경상남도)을 지도에 표시합니다.")

# 상위 5개 지역 목록
top5 = ['서울특별시', '경기도', '인천광역시', '부산광역시', '경상남도']

# 각 지역의 위도, 경도 정보
region_coords = {
    '서울특별시': [37.5665, 126.9780],
    '경기도': [37.4138, 127.5183],
    '인천광역시': [37.4563, 126.7052],
    '부산광역시': [35.1796, 129.0756],
    '경상남도': [35.4606, 128.2132],
}

# 각 지역의 총인구수 (숫자 타입)
region_population = {
    '서울특별시': 9489496,
    '경기도': 13860983,
    '인천광역시': 2969992,
    '부산광역시': 3299011,
    '경상남도': 3235581
}

# 인구수 최대/최소값 추출
pop_values = list(region_population.values())
pop_min, pop_max = min(pop_values), max(pop_values)

# radius 스케일링 함수 (인구수에 비례, 최소 8, 최대 30)
def scale_radius(pop):
    min_radius = 8
    max_radius = 30
    # 인구수 비율 (0~1)
    ratio = (pop - pop_min) / (pop_max - pop_min)
    return min_radius + ratio * (max_radius - min_radius)

# 지도 중심을 서울로 설정
m = folium.Map(location=[36.5, 127.5], zoom_start=7)

# 지도에 원 추가
for region in top5:
    lat, lon = region_coords[region]
    pop = region_population.get(region, 0)
    radius = scale_radius(pop)
    popup_text = f"<b>{region}</b><br>총인구수: {pop:,}명"
    folium.CircleMarker(
        location=[lat, lon],
        radius=radius,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.3,
        popup=folium.Popup(popup_text, max_width=300)
    ).add_to(m)

# 지도 출력
st_data = st_folium(m, width=800, height=600)
