# main.py
import streamlit as st
import hashlib
from db_utils import get_connection, init_db

init_db()
conn = get_connection()
c = conn.cursor()

# DB Functions
def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username, password) VALUES (?, ?)', (username, password))
    conn.commit()

def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username = ? AND password = ?', (username, password))
    return c.fetchall()

def view_all_users():
    c.execute('SELECT * FROM userstable')
    return c.fetchall()

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

st.title("MomE")
st.markdown("<h6 style='margin-top: -8px'>| MomEase : 엄마의 편안함</h6>", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'logged_in_user' not in st.session_state:
    st.session_state['logged_in_user'] = ''

tab1, tab2 = st.tabs(["Login", "Sign up"])

with tab1:
    st.subheader("로그인")
    username = st.text_input("ID")
    password = st.text_input("Password", type='password')
    if st.button("로그인"):
        hashed_pswd = make_hashes(password)
        result = login_user(username, check_hashes(password, hashed_pswd))
        if result:
            st.session_state['logged_in_user'] = username
            st.session_state['logged_in'] = True
            st.switch_page("pages/home.py")
        else:
            st.warning("아이디/비밀번호가 틀렸습니다!")

with tab2:
    st.subheader("회원가입")
    new_user = st.text_input("ID", key='ID')
    new_password = st.text_input("Password", type='password', key="new_password")
    if st.button("회원가입"):
        add_userdata(new_user, make_hashes(new_password))
        st.success("회원가입이 완료되었습니다. 로그인 탭으로 가서 로그인하세요.")

st.image("media/homeImg 1.png")
