# 필요한 라이브러리 설치
# pip install streamlit pandas matplotlib

import streamlit as st
import pandas as pd
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

# 운동 추천 (요청하신 대로 수정 반영)
def recommend_exercise(goal):
    if goal == "체중 감량":
        return [
            {"이름": "러닝", "세트": 1, "반복": 2, "거리": "5km"},
            {"이름": "점핑잭", "세트": 3, "반복": 2, "개수": "20개"},
            {"이름": "줄넘기", "세트": 3, "반복": 1, "개수": "100개"}
        ]
    elif goal == "근육 증가":
        return [
            {"이름": "푸쉬업", "세트": 5, "반복": 1, "개수": "20"},
            {"이름": "스쿼트", "세트": 4, "반복": 1, "개수": "30"},
            {"이름": "덤벨 컬", "세트": 3, "반복": 12, "무게": "5kg"}
        ]
    else:  # 건강 유지
        return [
            {"이름": "요가", "세트": 1, "반복": 20, "무게": "없음"},
            {"이름": "스트레칭", "세트": 2, "반복": 15, "무게": "없음"},
            {"이름": "걷기", "세트": 1, "반복": 30, "거리": "8km"}
        ]

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
    st.title("운동 기록 보기")
    if os.path.exists("log.csv"):
        df = pd.read_csv("log.csv")
        df["날짜"] = pd.to_datetime(df["날짜"])
        count_by_day = df.groupby("날짜").count()
        st.subheader("운동 기록 그래프")
        st.line_chart(count_by_day)

        st.subheader("운동 기록 상세")
        st.dataframe(df)
    else:
        st.write("운동 기록이 없습니다.")

# 운동 추천 페이지 내용
def exercise_recommendation_page():
    st.title("운동 추천 페이지")
    goal = st.selectbox("목표를 선택하세요", ["체중 감량", "근육 증가", "건강 유지"])
    if st.button("추천 운동 보기"):
        exercises = recommend_exercise(goal)
        df = pd.DataFrame(exercises)
        st.table(df)

# 메인 앱 흐름
def main():
    st.sidebar.title("운동 관리 메뉴")
    page = st.sidebar.selectbox("이동할 페이지 선택", ["홈", "운동 추천", "기록 보기"])

    if page == "홈":
        user_data = get_user_input()
        if user_data:
            exercises = recommend_exercise(user_data["목표"])
            st.success(f"{user_data['이름']}님을 위한 추천 운동")
            df = pd.DataFrame(exercises)
            st.table(df)

            if st.button("오늘 운동 완료"):
                for ex in exercises:
                    # 기록 문자열 만들기 (거리/개수/무게 중 있는 필드 사용)
                    details = ""
                    if "거리" in ex:
                        details = ex["거리"]
                    elif "개수" in ex:
                        details = ex["개수"]
                    elif "무게" in ex:
                        details = ex["무게"]

                    record = f"{ex['이름']} - {ex['세트']}세트 x {ex['반복']}회 ({details})"
                    save_record(record)
                st.success("운동 기록이 저장되었습니다!")

    elif page == "운동 추천":
        exercise_recommendation_page()

    elif page == "기록 보기":
        show_progress()

if __name__ == "__main__":
    main()
