import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from datetime import datetime, timedelta

# Sample data
df = pd.read_csv("https://raw.githubusercontent.com/cgwatertech/GW_mnt/main/cgwt.csv")

# Sidebar (왼쪽 프레임)
st.sidebar.title("위치 리스트")

# 'Time'을 제외한 컬럼들을 선택 박스에 넣음
selected_location = st.sidebar.selectbox("위치 선택", df.columns[1:])

# 각 위치의 최초 시작 날짜와 마지막 날짜 계산
start_dates = {}
end_dates = {}
for col in df.columns:
    if col == 'Time' or col == selected_location:
        continue
    start_dates[col] = df.loc[df[col].first_valid_index(), 'Time']
    end_dates[col] = df.loc[df[col].last_valid_index(), 'Time']

# Main content (오른쪽 프레임)
st.title("지하수위 관측 웹페이지")

# 이미지 표시
st.image("https://raw.githubusercontent.com/cgwatertech/GW_mnt/main/desKTOP_IMG.png", use_column_width=True)

# Plot (오른쪽 아래 프레임)
st.subheader(f"{selected_location} 위치의 지하수위 변화")

# 선택한 위치에 대한 평균 값을 계산
avg_value = df[selected_location].mean()
mx_value = df[selected_location].max()
mn_value = df[selected_location].min()
rng_value = (mx_value - mn_value) * 5  # 기본 범위 크기 5
rng_vale = rng_value / 2

# 평균 값으로 새로운 데이터 프레임을 만듦
avg_df = pd.DataFrame({'Time': df['Time'], selected_location: avg_value})
# 그래프 그리기
fig = px.line(df, x="Time", y=selected_location, title=f"{selected_location} 위치의 지하수위 변화")

# y 축 리미트 설정
fig.update_layout(yaxis=dict(range=[avg_value - rng_vale, avg_value + rng_vale]))

# 반응형으로 그래프 표시
st.plotly_chart(fig, use_container_width=True)

# 선택 결과를 새로운 창에서 보여주기
selected_data_preview = df[['Time', selected_location]].copy()

# 인덱스를 감춤
selected_data_preview.set_index('Time', inplace=True)

# 왼쪽 프레임에 데이터를 미리보는 창
st.sidebar.subheader("선택된 자료 미리보기")
st.sidebar.write(selected_data_preview.sort_index().head(15))

# 각 위치의 최초 시작 날짜와 마지막 날짜 출력
st.sidebar.subheader("각 위치의 최초 시작 날짜와 마지막 날짜")
for col in start_dates:
    st.sidebar.write(f"{col}: 시작일 - {start_dates[col]}, 종료일 - {end_dates[col]}")
