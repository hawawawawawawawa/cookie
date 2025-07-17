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

# 각 지역의 총인구수 (예시 데이터, 실제 값으로 수정 가능)
region_population = {
    '서울특별시': '9,489,496명',
    '경기도': '13,860,983명',
    '인천광역시': '2,969,992명',
    '부산광역시': '3,299,011명',
    '경상남도': '3,235,581명'
}

# 지도 중심을 서울로 설정
m = folium.Map(location=[36.5, 127.5], zoom_start=7)

# 지도에 원 추가
for region in top5:
    lat, lon = region_coords[region]
    population = region_population.get(region, "인구 정보 없음")
    popup_text = f"<b>{region}</b><br>총인구수: {population}"
    folium.CircleMarker(
        location=[lat, lon],
        radius=15,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.3,
        popup=folium.Popup(popup_text, max_width=300)
    ).add_to(m)

# 지도 출력
st_data = st_folium(m, width=800, height=600)
