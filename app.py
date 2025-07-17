import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.title("2025년 5월 기준 연령별 인구 현황")

# CSV 읽기 (실제 환경에 맞게 경로 조정)
df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='euc-kr')

# 총인구수 정리 (문자열에서 쉼표 제거 후 int 변환)
df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '').astype(int)

# 연령별 컬럼 추출 및 이름 정리
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and ('세' in col or '100세 이상' in col)]
new_columns = []
for col in age_columns:
    if '100세 이상' in col:
        new_columns.append('100세 이상')
    else:
        new_columns.append(col.replace('2025년05월_계_', '').replace('세', '') + '세')

df_age = df[['행정구역', '총인구수'] + age_columns].copy()
df_age.columns = ['행정구역', '총인구수'] + new_columns

# 상위 5개 행정구역 추출
top5_df = df_age.sort_values(by='총인구수', ascending=False).head(5)

# === Folium 지도를 위한 위경도 데이터 (행정구역별 대표 좌표) ===
# 실제 좌표는 정확히 확인해서 바꾸셔야 합니다
location_data = {
    "행정구역": top5_df["행정구역"].tolist(),
    "lat": [37.5665, 37.4138, 35.1796, 35.1796, 37.4563],  # 서울, 경기도, 부산, 경상남도, 인천 예시 좌표
    "lon": [126.9780, 127.5183, 129.0756, 128.6936, 126.7052]
}
loc_df = pd.DataFrame(location_data)

# top5_df와 위경도 데이터 병합
map_df = pd.merge(top5_df, loc_df, on='행정구역', how='inner')

# 지도 중심 좌표 (평균)
center_lat = map_df['lat'].mean()
center_lon = map_df['lon'].mean()

# folium 지도 생성
m = folium.Map(location=[center_lat, center_lon], zoom_start=7)

# 인구수에 따라 원 크기 조절해서 마커 표시
for _, row in map_df.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=7,               # 원 크기 작게 고정 (원하는 크기로 조절 가능)
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.3,       # 반투명도 낮게 설정 (0~1 사이, 0에 가까울수록 투명)
        popup=f"{row['행정구역']}: {row['총인구수']:,}명"
    ).add_to(m)

st.subheader("📍 상위 5개 행정구역 인구 분포 지도")
st_folium(m, width=700, height=500)

# 원본 데이터 테이블
st.subheader("📊 원본 데이터 (상위 5개 행정구역)")
st.dataframe(top5_df)

# 연령별 선그래프 출력
st.subheader("📈 상위 5개 행정구역 연령별 인구 변화")

age_columns_only = top5_df.columns[2:]  # 연령 컬럼 리스트

for idx, row in top5_df.iterrows():
    st.write(f"### {row['행정구역']}")
    # 쉼표 제거 후 int 변환
    age_data = row[2:].astype(str).str.replace(',', '').astype(int)
    age_df = pd.DataFrame({
        '연령': age_columns_only,
        '인구수': age_data.values
    }).set_index('연령')
    st.line_chart(age_df)
