# 필요한 라이브러리 설치
# pip install streamlit pandas matplotlib

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# 사용자 정보 입력
def get_user_input():
    st.title("맞춤형 운동 & 건강 관리")
    name = st.text_input("이름")
    age = st.number_input("나이", min_value=10, max_value=100)
    height = st.number_input("키(cm)", min_value=100)
    weight = st.number_input("몸무게(kg)", min_value=30)
    goal = st.selectbox("운동 목표", ["체중 감량", "근육 증가", "건강 유지"])
    if st.button("운동 계획 추천받기"):
        return {"이름": name, "나이": age, "키": height, "몸무게": weight, "목표": goal}
    return None

# 운동 추천
def recommend_exercise(goal):
    if goal == "체중 감량":
        return ["러닝 30분", "점핑잭 3세트", "줄넘기 15분"]
    elif goal == "근육 증가":
        return ["푸쉬업 3세트", "스쿼트 4세트", "덤벨 컬 3세트"]
    else:
        return ["요가 20분", "스트레칭 15분", "걷기 30분"]

# 운동 기록 저장
def save_record(exercise):
    today = datetime.now().strftime("%Y-%m-%d")
    df = pd.DataFrame([[today, exercise]], columns=["날짜", "운동"])
    if os.path.exists("log.csv"):
        df.to_csv("log.csv", mode='a', header=False, index=False)
    else:
        df.to_csv("log.csv", index=False)

# 기록 시각화
def show_progress():
    if os.path.exists("log.csv"):
        df = pd.read_csv("log.csv")
        df["날짜"] = pd.to_datetime(df["날짜"])
        count_by_day = df.groupby("날짜").count()
        st.subheader("운동 기록 그래프")
        st.line_chart(count_by_day)

# 메인 앱 흐름
def main():
    st.sidebar.title("운동 관리 메뉴")
    page = st.sidebar.selectbox("이동할 페이지 선택", ["홈", "운동 추천", "기록 보기"])

    if page == "홈":
        user_data = get_user_input()
        if user_data:
            exercises = recommend_exercise(user_data["목표"])
            st.success(f"{user_data['이름']}님을 위한 추천 운동")
            for ex in exercises:
                st.write(f"- {ex}")
            if st.button("오늘 운동 완료"):
                for ex in exercises:
                    save_record(ex)
                st.success("운동 기록이 저장되었습니다!")

    elif page == "기록 보기":
        show_progress()

if __name__ == "__main__":
    main()
