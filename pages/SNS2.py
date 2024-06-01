import streamlit as st
import sqlite3
from streamlit_option_menu import option_menu
from datetime import datetime

# 동일한 데이터베이스에 연결
conn = sqlite3.connect('data.db', check_same_thread=False)
c = conn.cursor()

# 데이터베이스 함수 확장
def create_tables():
    c.execute('CREATE TABLE IF NOT EXISTS poststable(username TEXT, image BLOB, post TEXT, timestamp TEXT, is_public INTEGER)')
    c.execute('CREATE TABLE IF NOT EXISTS likestable(post_id INTEGER, username TEXT)')
    conn.commit()

def add_post(username, image, post, is_public):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('INSERT INTO poststable(username, image, post, timestamp, is_public) VALUES (?,?,?,?,?)', (username, image, post, timestamp, is_public))
    conn.commit()

def view_all_posts():
    c.execute('SELECT rowid, username, image, post, timestamp FROM poststable WHERE is_public = 1')
    data = c.fetchall()
    return data

def view_my_posts(user, is_public):
    c.execute('SELECT rowid, username, image, post, timestamp FROM poststable WHERE username = ? AND is_public = ?', (user, is_public))
    data = c.fetchall()
    return data

def upgrade_post_table():
    try:
        c.execute('''ALTER TABLE poststable ADD COLUMN image BLOB''')
        c.execute('''ALTER TABLE poststable ADD COLUMN is_public INTEGER''')
        conn.commit()
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Columns already exist.")
        elif "no such table" in str(e):
            create_tables()  # 테이블이 없을 경우 테이블 생성
            upgrade_post_table()  # 다시 시도
        else:
            raise e

def like_post(post_id, username):
    c.execute('INSERT INTO likestable(post_id, username) VALUES (?,?)', (post_id, username))
    conn.commit()

def unlike_post(post_id, username):
    c.execute('DELETE FROM likestable WHERE post_id = ? AND username = ?', (post_id, username))
    conn.commit()

def get_like_count(post_id):
    c.execute('SELECT COUNT(*) FROM likestable WHERE post_id = ?', (post_id,))
    count = c.fetchone()[0]
    return count

def has_liked(post_id, username):
    c.execute('SELECT COUNT(*) FROM likestable WHERE post_id = ? AND username = ?', (post_id, username))
    return c.fetchone()[0] > 0

def view(posts):
    for post_id, username, image, post, timestamp in reversed(posts):  # 최신 게시물부터 표시하기 위해 reversed 사용
        st.markdown(f"<span style='font-weight: bold; font-size: 25px;'>{username}</span>", unsafe_allow_html=True)

        if image:
            st.image(image, caption=username, use_column_width=True)
        st.write(post)
        st.markdown(f'<p style="text-align: right;">{timestamp}</p>', unsafe_allow_html=True)

        like_count = get_like_count(post_id)
        liked = has_liked(post_id, user)
        
        if liked:
            if st.button(f"좋아요 취소 ({like_count})", key=f"unlike_{post_id}"):
                unlike_post(post_id, user)
                st.experimental_rerun()
        else:
            if st.button(f"좋아요 ({like_count})", key=f"like_{post_id}"):
                like_post(post_id, user)
                st.experimental_rerun()

        st.markdown("---")

def viewmy(posts):
    for post_id, username, image, post, timestamp in reversed(posts):  # 최신 게시물부터 표시하기 위해 reversed 사용
        st.markdown(f"**{username}**")
        if image:
            st.image(image, caption=username, use_column_width=True)
        st.write(post)

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("수정", key=f"edit_post_{post_id}"):
                edit_posts, edit_image, edit_timestamp, edit_ispublic = edit_post(post_id, image, post, timestamp)
        with col2:
            if st.button("삭제", key=f"delete_post_{post_id}"):
                delete_post(post_id)
                st.experimental_rerun()
        
        like_count = get_like_count(post_id)
        liked = has_liked(post_id, user)

        if liked:
            if st.button(f"좋아요 취소 ({like_count})", key=f"unlike_my_{post_id}"):
                unlike_post(post_id, user)
                st.experimental_rerun()
        else:
            if st.button(f"좋아요 ({like_count})", key=f"like_my_{post_id}"):
                like_post(post_id, user)
                st.experimental_rerun()

        st.markdown(f'<p style="text-align: right;">{timestamp}</p>', unsafe_allow_html=True)
        st.markdown("---")

def edit_post(post_id, image, post, timestamp):
    edited_image = None
    edited_post = st.text_area("게시물 수정", key=f"edit2_post_{post_id}")
    edited_is_public = st.checkbox("전체 공개로 수정", key=f"edit_public_post_{post_id}")
    
    if image:
        edited_image = st.file_uploader("이미지를 수정하세요.", type=['png', 'jpg', 'jpeg'], 
                                        accept_multiple_files=False, key=f"edit_image_post_{post_id}")
    if edited_image is None:
        edited_image = image

    if st.button("저장", key=f"save_post_{post_id}"):
        new_post = edited_post
        new_is_public = 1 if edited_is_public else 0
        update_post(post_id, new_post, new_is_public)
        st.success("게시물이 성공적으로 수정되었습니다.")
        st.experimental_rerun()
    return post, image, timestamp, is_public

def update_post(post_id, new_post, new_is_public):
    c.execute('UPDATE poststable SET post = ?, is_public = ? WHERE rowid = ?', (new_post, new_is_public, post_id))
    conn.commit()

def delete_post(post_id):
    c.execute('DELETE FROM poststable WHERE rowid=?', (post_id,))
    conn.commit()
    st.success("게시물이 성공적으로 삭제되었습니다.")

def main():
    st.title("육아 SNS")
    st.markdown("<h6 style='margin-top: -8px'>| 육아 동지들과 함께 일상을 공유해요!", unsafe_allow_html=True)
    st.write("")

    upgrade_post_table()
    create_tables()

    # 사용자 이름 가져오기
    global user
    user = st.session_state.get('logged_in_user', '')  # session_state에서 사용자 이름 가져오기
    print(user)
    if not user:
        st.error("로그인이 필요합니다.")
        return
        
    tab1, tab2, tab3 = st.tabs(['All posts', 'Upload', 'My'])
    
    with tab2:
        st.subheader("게시물 작성")
        image = st.file_uploader("이미지를 업로드하세요.", type=['png', 'jpg', 'jpeg'])
        post = st.text_area("사진 설명")
        is_public = st.checkbox("전체 공개로 게시")

        if st.button("업로드"):
            image_bytes = image.read() if image else None
            add_post(user, image_bytes, post, 1 if is_public else 0)
            if is_public:
                st.success("전체 공개로 업로드되었습니다!")
            else:
                st.success("비공개로 업로드되었습니다!")

    with tab1:
        all_posts = view_all_posts()
        view(all_posts)

    with tab3:
        st.subheader("내 게시물")
        tab31, tab32 = st.tabs(["공개", "비공개"])
        with tab31:
            my_posts = view_my_posts(user, 1)
            viewmy(my_posts)
        with tab32:
            my_posts = view_my_posts(user, 0)
            viewmy(my_posts)

if __name__ == "__main__":
    main()

with st.sidebar:
    menu = option_menu("MomE", ['Home','Dashboard','Diary', '육아 SNS','To do list','하루 자가진단','LogOut'],
                        icons=['bi bi-house-fill','bi bi-grid-1x2-fill','book-half','Bi bi-star-fill','Bi bi-calendar-check', 'bi bi-capsule-pill', 'box-arrow-in-right'],
                        menu_icon="baby", default_index=3,
                        styles={
                            "icon": {"font-size": "23px"},
                            "title": {"font-weight": "bold"}  # MomE 글씨를 볼드체로 변경
                        })

    # 선택된 메뉴에 따라 페이지 변경
    if menu == 'Dashboard':
        st.switch_page("pages/dashboard_page.py")
    elif menu == 'Diary':
        st.switch_page("pages/diary_page.py")
    elif menu == 'To do list':
        st.switch_page("pages/daily_schedule.py")
    elif menu == '하루 자가진단':
        st.switch_page("pages/self_diagnosis.py")
    elif menu == 'Home':
        st.switch_page("pages/home.py")
    elif menu =='LogOut':
        st.switch_page("dd1.py")
