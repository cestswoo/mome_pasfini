import sqlite3
import streamlit as st
from datetime import datetime
from streamlit_option_menu import option_menu

# 로그인 상태를 확인하는 함수
def check_login():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("로그인 후 이용해주세요")
        st.stop()

with st.sidebar:
    menu = option_menu("MomE", ['Home', 'Dashboard', 'Diary', '육아 SNS', 'To do list', '하루 자가진단', 'LogOut'],
                        icons=['bi bi-house-fill', 'bi bi-grid-1x2-fill', 'book-half', 'Bi bi-star-fill', 'Bi bi-calendar-check', 'bi bi-capsule-pill', 'box-arrow-in-right'],
                        menu_icon="baby", default_index=4,
                        styles={
                            "icon": {"font-size": "23px"},
                            "title": {"font-weight": "bold"}
                        })

    if menu == 'Dashboard':
        st.switch_page("pages/dashboard_page.py")
    elif menu == 'Diary':
        st.switch_page("pages/diary_page.py")
    elif menu == '육아 SNS':
        st.switch_page("pages/SNS2.py")
    elif menu == 'Home':
        st.switch_page("pages/home.py")
    elif menu == '하루 자가진단':
        st.switch_page('pages/self_diagnosis.py')
    elif menu == 'LogOut':
        st.session_state['logged_in'] = False
        st.switch_page("dd1.py")

# 데이터베이스 초기화
def init_db():
    conn = sqlite3.connect('daily_schedule.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            time TEXT,
            task TEXT,
            comments TEXT
        )
    ''')
    conn.commit()
    conn.close()

# 데이터 삽입 및 조회 함수
def add_schedule(date, time, task, comments):
    conn = sqlite3.connect('daily_schedule.db')
    c = conn.cursor()
    c.execute('INSERT INTO schedules (date, time, task, comments) VALUES (?, ?, ?, ?)',
              (date, time, task, comments))
    conn.commit()
    conn.close()

def get_schedules():
    conn = sqlite3.connect('daily_schedule.db')
    c = conn.cursor()
    c.execute('SELECT * FROM schedules ORDER BY datetime(date) DESC, datetime(time) DESC')
    schedules = c.fetchall()
    conn.close()
    return schedules

def delete_schedule(schedule_id):
    conn = sqlite3.connect('daily_schedule.db')
    c = conn.cursor()
    c.execute('DELETE FROM schedules WHERE id = ?', (schedule_id,))
    conn.commit()
    conn.close()

# 일정 작성 폼
def schedule_form():
    st.subheader("하루 일과 관리")
    date = st.date_input("날짜")
    time = st.time_input("시간")
    task = st.text_input("할 일")
    comments = st.text_area("메모")

    if st.button("일정 저장"):
        if task:
            add_schedule(date.strftime("%Y-%m-%d"), time.strftime("%H:%M:%S"), task, comments)
            st.success("일정이 저장되었습니다.")
            st.experimental_rerun()
        else:
            st.error("할 일을 입력해주세요.")

# 일정 목록 표시
def schedule_list():
    st.subheader("하루 일과 목록")
    schedules = get_schedules()
    for schedule in schedules:
        st.markdown(f"""
        **날짜:** {schedule[1]}  
        **시간:** {schedule[2]}  
        **할 일:** {schedule[3]}  
        **메모:** {schedule[4]}
        """, unsafe_allow_html=True)
        if st.button("일정 삭제", key=f'delete_button_{schedule[0]}'):
            delete_schedule(schedule[0])
            st.experimental_rerun()
        st.write("---")

# 일정 전체 삭제 함수
def delete_all_schedules():
    conn = sqlite3.connect('daily_schedule.db')
    c = conn.cursor()
    c.execute('DELETE FROM schedules')
    conn.commit()
    conn.close()
    st.success("모든 일정이 삭제되었습니다.")
    st.experimental_rerun()

# Streamlit 앱 실행
def main():
    # 로그인 상태 확인
    check_login()
    
    # CSS 스타일 추가
    st.markdown(
        """
        <style>
        body {
            background-color: #f0f2f6;
        }
        .reportview-container .main .block-container {
            padding: 2rem;
        }
        .stTextInput > div > div > input, .stTextArea > div > textarea {
            border: 1px solid #ccc;
            padding: 10px;
            border-radius: 5px;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 5px 10px;
            font-size: 12px;
            margin: 5px 2px;
            cursor: pointer;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        .fixed-button {
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 9999;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("하루 일과 관리")

    # 페이지 상단에 고정된 버튼
    if st.button("모든 일정 삭제", key='delete_all'):
        delete_all_schedules()

    # 페이지를 두 부분으로 나누기
    col1, col2 = st.columns(2)

    with col1:
        schedule_form()

    with col2:
        schedule_list()

if __name__ == "__main__":
    init_db()
    main()
