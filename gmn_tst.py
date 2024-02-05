import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from datetime import datetime

# Sample data
df = pd.read_csv("https://raw.githubusercontent.com/cgwatertech/GW_mnt/main/cgwt.csv")

# Sidebar (왼쪽 프레임)
st.sidebar.title("위치 리스트")

# 'Time'을 제외한 컬럼들을 선택 박스에 넣음
selected_location = st.sidebar.selectbox("위치 선택", df.columns[1:])

# Time 열을 DateTime 객체로 변환
df['Time'] = pd.to_datetime(df['Time'])

# 시작 날짜와 끝 날짜 선택
start_date = st.sidebar.date_input("시작 날짜 선택", min_value=df['Time'].min(), max_value=df['Time'].max(), value=df['Time'].min())
end_date = st.sidebar.date_input("끝 날짜 선택", min_value=df['Time'].min(), max_value=df['Time'].max(), value=df['Time'].max())

# datetime 객체로 변환
start_date = datetime.combine(start_date, datetime.min.time())
end_date = datetime.combine(end_date, datetime.min.time())

# 시작 날짜와 끝 날짜 사이의 데이터 필터링
filtered_data = df[(df['Time'] >= start_date) & (df['Time'] <= end_date)]

# Main content (오른쪽 프레임)
st.title("지하수위 관측 웹페이지")

# 이미지 표시
st.image("https://raw.githubusercontent.com/cgwatertech/GW_mnt/main/desKTOP_IMG.png", use_column_width=True)

# Plot (오른쪽 아래 프레임)
st.subheader(f"{selected_location} 위치의 지하수위 변화 ({start_date}부터 {end_date})")

# 선택한 위치에 대한 평균 값을 계산
avg_value = filtered_data[selected_location].mean()

# 평균 값으로 새로운 데이터 프레임을 만듦
avg_df = pd.DataFrame({'Time': filtered_data['Time'], selected_location: avg_value})

# 그래프 그리기
fig = px.line(filtered_data, x="Time", y=selected_location, title=f"{selected_location} 위치의 지하수위 변화 ({start_date}부터 {end_date})")

# y 축 리미트 설정
fig.update_layout(yaxis=dict(range=[avg_value - 3, avg_value + 4]))

# x 축 tick 및 라벨 설정
tickvals = filtered_data['Time'].iloc[::len(filtered_data) // 5]  # 7 ticks로 나누기
ticktext = [val.strftime('%Y-%m-%d %H') for val in tickvals]
fig.update_layout(xaxis=dict(tickvals=tickvals, ticktext=ticktext))

# 확대 및 축소 기능 추가
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            x=1.05,
            y=0.8,
            buttons=[
                dict(label="전체보기", method="relayout", args=["yaxis", dict(range=[filtered_data[selected_location].min(), filtered_data[selected_location].max()])]),
                dict(label="기본값", method="relayout", args=["yaxis", dict(range=[avg_value - 3, avg_value + 4])]),
            ],
        ),
    ]
)

# 반응형으로 그래프 표시
st.plotly_chart(fig, use_container_width=True)

# 선택한 그래프의 시간과 데이터 다운로드 버튼
selected_data = filtered_data[['Time', selected_location]]
csv_selected_data = selected_data.to_csv(index=False)
b64_selected_data = base64.b64encode(csv_selected_data.encode()).decode()
st.markdown(f'<a href="data:file/csv;base64,{b64_selected_data}" download="selected_data.csv">선택 그래프 데이터 다운로드</a>', unsafe_allow_html=True)

# 전체 데이터 다운로드 버튼
csv_all_data = df.to_csv(index=False)
b64_all_data = base64.b64encode(csv_all_data.encode()).decode()
st.markdown(f'<a href="data:file/csv;base64,{b64_all_data}" download="all_data.csv">전체 자료 다운로드</a>', unsafe_allow_html=True)

# 선택 결과를 새로운 창에서 보여주기
selected_data_preview = filtered_data[['Time', selected_location]].copy()

# 인덱스를 감춤
selected_data_preview.set_index('Time', inplace=True)

# 선택 결과를 새로운 창에서 보여주기
new_window = st.sidebar.empty()  # 새로운 창을 열기 위한 준비
with new_window:
    st.write(selected_data_preview)
