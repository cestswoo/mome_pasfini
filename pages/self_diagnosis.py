# self_diagnosis.py
import streamlit as st
import sqlite3
from streamlit_option_menu import option_menu
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from db_utils import get_connection, init_db

init_db()
conn = get_connection()
c = conn.cursor()

def save_result(user, selected_date, scores, total_score):
    try:
        c.execute('''
            INSERT INTO self_diagnosis (user, date, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, total_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user, selected_date, scores['q1'], scores['q2'], scores['q3'], scores['q4'], scores['q5'], scores['q6'], scores['q7'], scores['q8'], scores['q9'], scores['q10'], total_score))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"An error occurred: {e}")

def get_results(user):
    c.execute('''
        SELECT date, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, total_score
        FROM self_diagnosis
        WHERE user = ?
        ORDER BY date DESC
    ''', (user,))
    return c.fetchall()

def question_block(text, answer_option, key):
    text_area = st.container()
    text_area.write(text)
    return answer_option[st.radio("", options=list(answer_option.keys()), key=key, help=" ")]

st.markdown(
    """
    <style>
        .header {
            color: #FF69B4;
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .intro-box {
            background-color: #fbecf7;
            color: #000000;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
        }
        .intro-text {
            font-size: 20px;
            margin-bottom: 20px.
        }
        .result {
            background-color: #FFC0CB;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px.
        }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    st.title("Self-diagnosis")
    st.markdown("<h6 style='margin-top: -8px'>| 산후 우울증에 대해 알아보고 자가 진단해보세요</h6>", unsafe_allow_html=True)
    st.write("")

    user = st.session_state.get('logged_in_user', '')
    if not user:
        st.error("로그인이 필요합니다.")
        return
    
    tab1, tab2 = st.tabs(['자가진단', '결과'])

    with tab1:
        selected_date = st.date_input("오늘의 날짜를 선택해 주세요", value=datetime.now())
        st.write("")

        answer_option = {
            '전혀 그렇지 않음': 0,
            '가끔 그렇음': 1,
            '종종 그렇음': 2,
            '대부분 그렇음': 3
        }

        col1, col2 = st.columns(2)
        with col1:
            q1 = question_block(f"**1. 우스운 것이 눈에 잘 띄고 웃을 수 있었다.**", answer_option, key='q1')
            q3 = question_block(f"**3. 일이 잘못되면 필요 이상으로 자신을 탓해왔다.**", answer_option, key='q3')
            q5 = question_block(f"**5. 별 이유 없이 겁먹거나 공포에 휩싸였다.**", answer_option, key='q5')
            q7 = question_block(f"**7. 너무나 불안한 기분이 들어 잠을 잘 못 잤다.**", answer_option, key='q7')
            q9 = question_block(f"**9. 너무나 불행한 기분이 들어 울었다.**", answer_option, key='q9')
            
        with col2:
            q2 = question_block(f'**2. 즐거운 기대감에 어떤 일을 손꼽아 기다렸다.**', answer_option, key='q2')
            q4 = question_block(f"**4. 별 이유 없이 불안해지거나 걱정이 되었다.**", answer_option, key='q4')
            q6 = question_block(f"**6. 처리할 일들이 쌓여만 있다.**", answer_option, key='q6')
            q8 = question_block(f"**8. 슬프거나 비참한 느낌이 들었다.**", answer_option, key='q8')
            q10 = question_block(f"**10. 나 자신을 해치는 생각이 들었다.**", answer_option, key='q10')

        if st.button("결과 확인하기"):
            st.subheader("결과")

            scores = {
                'q1': q1,
                'q2': q2,
                'q3': q3,
                'q4': q4,
                'q5': q5,
                'q6': q6,
                'q7': q7,
                'q8': q8,
                'q9': q9,
                'q10': q10
            }

            total_score = sum(scores.values())

            if total_score >= 13:
                st.error("치료가 시급합니다. 이 경우 반드시 정신건강 전문가의 도움을 받으셔야 합니다. 산후우울증은 정서적 문제뿐만 아니라 뇌 신경전달 물질의 불균형과 관련이 있으며, 적절한 치료를 받는 것이 중요합니다. 전문가와 함께 산후우울에 대한 이야기를 나누고 적절한 치료를 받아보시기 바랍니다.")
            elif total_score >= 9:
                st.warning("상담이 필요합니다. 산후 우울증 위험이 높은 것으로 나타났습니다. 전문가의 상담을 받아보시는 것이 좋습니다. 무엇이든 치료보다는 예방이 좋습니다. 조금 더 정확한 결과를 알아보고 싶다면 정신건강 전문가를 방문해 상담과 진료를 받아보시길 바랍니다.")
            else:
                st.success("정상 범위입니다. 산후 우울증 위험이 낮은 것으로 나타났습니다. 그러나 주변 지원 및 관리가 필요할 수 있습니다. 자신의 감정을 받아들이고 남편과 가족들과 나누며, 신체적 정서적 안정을 취할 수 있도록 함께 협력하고 노력해주세요.")

            save_result(user, selected_date, scores, total_score)

    with tab2:
        results = get_results(user)
        if not results:
            st.error("데이터가 없습니다. 먼저 자가 진단을 진행해주세요.")
            st.stop()

        color_labels = {
            0: ('#baef9d', '전혀 그렇지 않음 / 0점'),
            1: ('#e8ef9d', '가끔 그렇음 / 1점'),
            2: ('#efd39d', '종종 그렇음 / 2점'),
            3: ('#efae9d', '대부분 그렇음 / 3점')
        }

        col1, _, col2 = st.columns([1, 0.15, 1])
        with col1:
            st.subheader("Test Result")
            st.write("")
            st.write("🙂 0-8점")
            st.write("| 정상 범위입니다")
            st.write("🙁 9-12점")
            st.write("| 일반적으로 산모들이 느끼는 우울보다 더 많은 우울감을 느끼고 있습니다. 전문가와의 상담을 권유드립니다.")
            st.write("😔 13-30점")
            st.write("| 산후 우울증을 겪고 계신 상황인 것 같습니다. 주변 병원에서 치료를 받아보시는 것을 권유드립니다.")
        with col2:
            st.subheader("Answers")
            for score, label in color_labels.values():
                st.markdown(f"- <span style='color:{score}; font-size: 150%'>&#11044;</span> {label}", unsafe_allow_html=True)
                st.write("")
        st.divider()

        st.subheader("Test Record")
        for record in results:
            date = record[0]
            total_score = record[11]
            scores = record[1:11]
            
            fig, ax = plt.subplots(figsize=(8, 0.5))
            for i, score in enumerate(scores):
                ax.scatter(i + 1, 0, color=color_labels[score][0], s=500)
                ax.text(i + 1, 0, str(i + 1), ha='center', va='center', fontsize=12)
            ax.set_xlim(0.5, len(scores) + 0.5)
            ax.set_ylim(-0.1, 0.1)
            ax.axis('off')

            if total_score < 9:
                st.write(f"🙂| {date} / Total score : {total_score} |")
            elif 9 <= total_score <= 12:
                st.write(f"🙁| {date} / Total score : {total_score} |")
            else:
                st.write(f"😔| {date} / Total score : {total_score} |")

            st.pyplot(fig)
            st.write("")

with st.sidebar:
    menu = option_menu("MomE", ['Home', 'Dashboard', 'Diary', '육아 SNS', 'To do list', '하루 자가진단', 'LogOut'],
                        icons=['bi bi-house-fill', 'bi bi-grid-1x2-fill', 'book-half', 'Bi bi-star-fill', 'Bi bi-calendar-check', 'bi bi-capsule-pill', 'box-arrow-in-right'],
                        menu_icon="baby", default_index=5,
                        styles={
                            "icon": {"font-size": "23px"},
                            "title": {"font-weight": "bold"}
                        })

    if menu == 'Dashboard':
        st.switch_page("pages/dashboard_page.py")
    elif menu == 'Diary':
        st.switch_page('pages/diary_page.py')
    elif menu == '육아 SNS':
        st.switch_page('pages/SNS2.py')
    elif menu == 'Home':
        st.switch_page('pages/home.py')
    elif menu == 'To do list':
        st.switch_page('pages/daily_schedule.py')
    elif menu == 'LogOut':
        st.switch_page("dd1.py")

if __name__ == "__main__":
    init_db()
    main()
