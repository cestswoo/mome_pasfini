import base64
import streamlit as st
from streamlit_option_menu import option_menu
import os

# Define and apply custom fonts using @font-face
st.markdown(
    """
    <style>
    @font-face {
        font-family: 'NanumPen';
        src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2101@1.0/NanumPen.woff') format('woff');
        font-weight: normal;
        font-style: normal;
    }

    @font-face {
        font-family: 'NanumGothic';
        src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2104@1.0/NanumGothic.woff') format('woff');
        font-weight: normal;
        font-style: normal;
    }

    .title-font {
        font-family: 'NanumPen', sans-serif;
        font-size: 24px;
        font-weight: bold;
    }

    .body-font {
        font-family: 'NanumGothic', sans-serif;
        font-size: 18px;
        font-weight: 500;
        color: #091747;
    }

    .stApp {
        background: #FEF9F0;
    }
    .Container {
        width: 710px;
        width: 100%; /* 부모 컨테이너 너비 */
        height: 100vh; /* 부모 컨테이너 높이 */
        overflow: hidden;
        border-radius: 30px;
    }
    .homeImg {
        position: relative; /* 내부 요소 고정 */
        width: 707px;
        height: 471px;
        border-radius: 30px;
    }
    .textContainer {
        position: absolute;
        top: 10%;
        left: 75%;
        transform: translate(-50%, -50%);
        display: flex;
        flex-direction: column;
        color: white;
        width: 170px;
        height: 90px;
        text-align: start;
    }
    .logo {
        font-size: 60px;
        font-weight: bold;
        color: white;
    }
    .logo-below {
        position: absolute; /* 위치 고정 */
        top: 80%;
        left: 1%;
        width: 120px;
        font-size: 13px;
        font-weight: lighter;
        color: white;
    }
    .adText {
        position: absolute; /* 위치 고정 */
        top: 28%;
        left: 30%;
        transform: translateX(-50%);
        width: 229px;
        height: 95px;
        font-size: 40px;
        font-weight: 400px;
        color: white;
    }
    .mainContainer {
        display: flex;
        flex-direction: column;
        align-items: center;
        position: absolute;
        top: 50%;
        width: 707px;
        height: 2150px;
        background-color: white;
        border-radius: 30px 30px 0px 0px;
    }
    .contentIndex {
        font-weight: bold;
        font-size: 20px;
        margin-top: 20px;
        margin-bottom: 30px;
    }
    .aboutUsContent {
        text-align: center;
        margin-bottom: 35px;
        font-size: 17px;
    }
    .divider {
        width: 250px;
        height: 2px;
        background-color: black;
        margin-bottom: 55px;
    }
    .serviceComponent {
        position: relative;
        margin-left: 22.5px;
        margin-right: 50px;
        margin-bottom: 24px;
        width: 302px;
        height: 240px;
        border-radius: 30px;
        background-color: #F6F6F6;
        display: flex;
        flex-direction: column;
        align-items: start;
    }
    .titleContainer {
        margin: 30px 0px 20px 35px;
        position: relative;
        width: 200;
        height: 56px;
        display: flex;
        flex-direction: row;
        align-items: center;
    }
    .titleBar {
        position: relative;
        width: 2px;
        height: 42px;
        background-color: #000000;
        margin-right: 10px;
    }
    .title {
        margin-top: 4px;
        margin-right: 40px;
        position: relative;
        font-size: 20px;
        font-weight: bold;
        color: black;
        line-height: 1.2;
    }
    .serviceDetail {
        color: black;
        font-weight: 800;
        margin-left: 30px;
        position: relative;
        font-size: 16px;
        text-align: start;
        line-height: 1.4;
        width: 240px;
        height: 50px;
    }
    .imgContainer {
        width: 302px;
        height: 420px;
        margin-left: 25px;
        margin-bottom: 20px;
    }
    .copyRightDivider {
        width: 600px;
        height: 1.7px;
        background-color: black;
        margin-bottom: 55px;
    }
    .contact {
        margin: 0px 12px;
        font-size: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def load_image(image_path):
    if not os.path.exists(image_path):
        st.error(f"File not found: {image_path}")
        return None
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        encoded_image = base64.b64encode(data).decode()
        return encoded_image
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return None

image_path = "./media/homeImg.jpg"
Img1_path = './media/Img1.jpg'
Img2_path = './media/Img2.jpg'
Img3_path = './media/Img3.jpg'
Img4_path = './media/Img4.jpg'

homeImg = load_image(image_path)
if homeImg:
    st.markdown(f'''
        <div class="Container body-font">
            <div class="homeImg">
                <img src="data:image/jpg;base64,{homeImg}" />
                <div class="textContainer">
                    <div class="logo title-font">MomE</div>
                    <div class="logo-below">Always here for you</div>
                </div>
                <div class="adText title-font">We Care<br>Your Mind</div>
            </div>
            <div class="mainContainer">
                <div class="contentIndex title-font">About Us</div>
                <div class="divider"></div>
                <div class="aboutUsContent body-font">
                    MomE은 산후우울증을 겪었거나 겪고 있는 엄마와 가족들을 위한 특별한 공간입니다.<br>
                    당신의 여정에 함께하며 희망과 회복의 길로 안내합니다. <br><br>
                    산후우울증은 많은 엄마들이 경험하는 어려운 감정입니다. <br>
                    MomE는 이러한 감정을 이해하고 공감하며, 회복을 도와드리기 위해 만들어졌습니다. <br>
                    당신의 마음을 치유하고, 행복한 순간들을 만들어 나갈 수 있는 여정,<br>
                    MomE와 함께하세요.
                </div>
                <div class="divider"></div>
                <div class="contentIndex title-font">Our Service</div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    row1, row2 = st.columns(2)

    with row1:
        st.markdown(f"""
            <div class="serviceComponent body-font">
                <div class="titleContainer">
                    <div class="titleBar"></div>
                    <div class="title title-font"> 육아 일기장<br>서비스</div>
                </div>
                <div class="serviceDetail"> 
                    산모가 육아 일기를 작성하며
                    자신의 마음도 함께 돌아볼 수 있는
                    서비스를 제공합니다.<br><br>
                    가족과 함께 일상을 공유해보세요.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        Img_02 = load_image(Img2_path)
        if Img_02:
            st.markdown(
                f'''
                <div class="imgContainer">
                    <img src="data:image/jpg;base64,{Img_02}" />
                </div>
                ''',
                unsafe_allow_html=True
            )

        st.markdown(f"""
            <div class="serviceComponent body-font">
                <div class="titleContainer">
                    <div class="titleBar"></div>
                    <div class="title title-font"> 산후우울증<br>바로알기</div>
                </div>
                <div class="serviceDetail">
                    산후우울증<br>(postpartum depression)<br>
                    에 대한 원인, 증상,치료 등<br>
                    기본정보 제공합니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        Img_04 = load_image(Img4_path)
        if Img_04:
            st.markdown(
                f'''
                <div class="imgContainer">
                    <img src="data:image/jpg;base64,{Img_04}"/>
                </div>
                ''',
                unsafe_allow_html=True
            )

    with row2:
        Img_01 = load_image(Img1_path)
        if Img_01:
            st.markdown(
                f'''
                <div class="imgContainer">
                    <img src="data:image/jpg;base64,{Img_01}" />
                </div>
                ''',
                unsafe_allow_html=True
            )

        st.markdown(f"""
            <div class="serviceComponent body-font">
                <div class="titleContainer">
                    <div class="titleBar"></div>
                    <div class="title title-font">일기장 감정 <br>분석 서비스</div>
                </div>
                <div class="serviceDetail">
                    일기장 단어 분석을 통해<br>감정 변화를 추적하고 긍정적인<br>피드백을 제공하여 더 건강한 육아를 할 수 있도록 지원합니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        Img_03 = load_image(Img3_path)
        if Img_03:
            st.markdown(
                f'''
                <div class="imgContainer">
                    <img src="data:image/jpg;base64,{Img_03}" />
                </div>
                ''',
                unsafe_allow_html=True
            )

        st.markdown(f"""
            <div class="serviceComponent body-font">
                <div class="titleContainer">
                    <div class="titleBar"></div>
                    <div class="title title-font"> 산후우울증 자가진단<br>테스트</div>
                </div>
                <div class="serviceDetail">
                    에딘버러 산후우울증 척도<br>
                    K-EPDS를 이용하여 산후 우울증<br>
                    자가진단 및 시각화 데이터를<br>
                    제공합니다. 
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # 문의 및 저작권 표시
    st.markdown("""
        <div class="contact body-font">
            MomE ｜ 주소 경기도 용인시 처인구 외대로 81 한국외국어대학교 ｜ 이메일 susu492@naver.com<br>
            ⓒ MomE
        </div>
    """, unsafe_allow_html=True)
else:
    st.error("Failed to load the home image.")

# Sidebar menu
with st.sidebar:
    menu = option_menu("MomE", ['Home', 'Dashboard', 'Diary', '육아 SNS', 'To do list', '하루 자가진단', 'LogOut'],
                        icons=['bi bi-house-fill', 'bi bi-grid-1x2-fill', 'book-half', 'Bi bi-star-fill', 'Bi bi-calendar-check', 'bi bi-capsule-pill', 'box-arrow-in-right'],
                        menu_icon="baby", default_index=0,
                        styles={
                            "icon": {"font-size": "23px"},
                            "title": {"font-weight": "bold"}
                        })

    # Page navigation
    if menu == 'Dashboard':
        st.switch_page("pages/dashboard_page.py")
    elif menu == 'Diary':
        st.switch_page('pages/diary_page.py')
    elif menu == '육아 SNS':
        st.switch_page('pages/SNS2.py')
    elif menu == 'To do list':
        st.switch_page('pages/daily_schedule.py')
    elif menu == '하루 자가진단': 
        st.switch_page('pages/self_diagnosis.py')
    elif menu == 'LogOut':
        st.switch_page('dd1.py')
