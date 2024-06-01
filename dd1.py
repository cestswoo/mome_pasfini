import streamlit as st
import hashlib
import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()

# DB Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_userdata(username,password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    conn.commit()

def login_user(username,password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    data = c.fetchall()
    return data

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

st.title("MomE")
st.markdown("<h6 style='margin-top: -8px'>| MomEase : 엄마의 편안함</h2>", unsafe_allow_html=True)

# 세션 상태에 'logged_in' 상태가 없으면 초기화
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'logged_in_user' not in st.session_state:
    st.session_state['logged_in_user'] = ''

# if st.session_state['logged_in']: 
#     st.write(f"환영합니다, {st.session_state['logged_in_user']}님!")
#     st.switch_page("pages/home.py")
# else:
tab1, tab2 = st.tabs(["Login", "Sign up"])

with tab1:
    st.subheader("로그인")
    username = st.text_input("ID")
    password = st.text_input("Password", type='password')
    if st.button("로그인"):
        create_usertable()
        hashed_pswd = make_hashes(password)
        result = login_user(username, check_hashes(password, hashed_pswd))
        if result:
            st.session_state['logged_in_user'] = username  # Save logged in username in session state
            st.session_state['logged_in'] = True
            st.switch_page("pages/home.py")
            # st.experimental_rerun()  # 페이지 리로드
        else:
            st.warning("아이디/비밀번호가 틀렸습니다!")

with tab2:
    st.subheader("회원가입")
    new_user = st.text_input("ID", key='ID')
    new_password = st.text_input("Password", type='password', key="new_password")
    
    if st.button("회원가입"):
        create_usertable()
        add_userdata(new_user, make_hashes(new_password))
        st.success("회원가입이 완료되었습니다. 로그인 탭으로 가서 로그인하세요.")
        # st.info("Go to Login Menu to login")

st.image("media/homeImg 1.png")
