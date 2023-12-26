import streamlit as st
import pandas as pd
import plotly.express as px

# Sample data
df = pd.read_csv("https://raw.githubusercontent.com/cgwatertech/GW_mnt/main/cgwt.csv")

# Sidebar (왼쪽 프레임)
st.sidebar.title("위치 리스트")

# 'Time'을 제외한 컬럼들을 선택 박스에 넣음
selected_location = st.sidebar.selectbox("위치 선택", df.columns[1:])

# 이미지 업로드
uploaded_file = st.file_uploader("이미지 파일을 업로드하세요.", type=["jpg", "jpeg", "png"])

# Main content (오른쪽 프레임)
st.title("지하수위 관측 웹페이지")

# Table (오른쪽 아래 프레임)
st.subheader("데이터 표")
st.write(df)

# Plot (오른쪽 위 프레임)
st.subheader("선택한 위치에 대한 그래프")

# 선택한 위치에 대한 그래프를 새 창으로 열기
if st.button("그래프 보기"):
    # 선택한 위치에 대한 평균 값을 계산
    avg_value = df[selected_location].mean()

    # 평균 값으로 새로운 데이터 프레임을 만듦
    avg_df = pd.DataFrame({'Time': df['Time'], selected_location: avg_value})

    # 그래프 그리기
    fig = px.line(df, x="Time", y=selected_location, title=f"{selected_location} 위치의 지하수위 변화")

    # y 축 리미트 설정
    fig.update_layout(yaxis=dict(range=[avg_value - 3, avg_value + 4]))

    # 확대 및 축소 기능 추가
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                x=1.05,
                y=0.8,
                buttons=[
                    dict(label="전체보기", method="relayout", args=["yaxis", dict(range=[df[selected_location].min(), df[selected_location].max()])]),
                    dict(label="기본값", method="relayout", args=["yaxis", dict(range=[avg_value - 3, avg_value + 4])]),
                ],
            ),
        ]
    )

    st.plotly_chart(fig)

# 이미지 표시
if uploaded_file is not None:
    st.subheader("업로드한 이미지")
    st.image(uploaded_file, caption="업로드한 이미지", use_column_width=True)
