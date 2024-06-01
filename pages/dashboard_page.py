import streamlit as st
from streamlit_option_menu import option_menu

st.title("DashBoard")
st.markdown("<h6 style='margin-top: -8px'>| 산후 우울증 바로 알기", unsafe_allow_html=True)
st.write("")
st.write("")




st.markdown(
    """
    <style>
        .container{
            background-color: #f3f3f3;
            width: 340px;
            height:220px;
            padding: 20px;
            margin-bottom: 15px;
            border-radius:10px;
        }
        .container1{
            background-color: #f3f3f3;
            width: 340px;
            height:260px;
            padding: 20px;
            margin-bottom: 15px;
            border-radius:10px;
        }
        .container2{
            background-color: #f3f3f3;
            width: 705px;
            height:300px;
            padding: 20px;
            margin-bottom: 15px;
            border-radius:10px;
        }
        .servTitle {
            font-weight: bold;
            font-size: 25px;
        }
    </style>
    """,
    unsafe_allow_html=True
)
video_row1, video_row2 = st.columns(2)
st.write("")
st.divider()
row1,row2 = st.columns(2)

with video_row1:
    video_url = 'https://youtu.be/zqfFHWuS8aQ?feature=shared'
    st.video(video_url)

with video_row2:
    st.markdown(
        """
        <div class="container1">
            <p class="servTitle"> 산후 우울증이란?</p>
            산후우울증은 임신 마지막 달부터 출산 후 4주 이내에
        우울증 증상(우울, 불안초조, 불면, 죄책감 등)이 발생해
        그 증상이 2주 이상 지속되는 것을 말합니다.
        </div>
        """,
        unsafe_allow_html=True
    )



with row1:
    st.markdown(
        """
        <div class="container">
            <p class="servTitle"> 산후 우울증 증상</p>\n
            - 자꾸 우울한 기분이 들어요
            - 작은 일에도 과도하게 불안해요
            - 잠이 잘 오지 않아요
            - 체중에 변화가 찾아와요
        </div>
        """,
        unsafe_allow_html=True
    )

with row2:
    st.markdown(
        """
        <div class="container">
            <p class="servTitle"> 산후 우울증 치료</p>\n
            - 심리 치료
            - 약물 치료 
            : 증상이 심한 경우 의사와 상의 후 
              처방이 가능합니다
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
        """
        <div class="container2">
            <p class="servTitle">MomE를 통한 산후 우울증 치료 효과</p>\n
            - 일기를 쓰면서 오늘 하루 자신을 돌아볼 수 있는 시간 가짐
            - 댓글 기능이 남편과의 소통창구 역할을 할 수 있음
            - 육아 SNS를 통해 사람들과 동질감을 느끼고 위로받을 수 있음
            - 하루 자가진단 기능을 통해 매일매일 기분과 우울감을 기록
              * 기록된 데이터들을 시각화해서 내 상태 추이 파악 가능
              * 시각화 된 데이터는 의사 진단에 도움이 될 수 있음
        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")
st.divider()
st.write("")
st.write("")

tab1,tab2,tab3 = st.tabs(['산후 우울증 예방법', '산후 우울증 극복기','남편'])

with tab1:

    video_data = [
        {"link": "https://youtu.be/ZLSleUyjhC0?feature=shared", "description": "산후우울증의 원인과 예방방법은?"},
        {"link": "https://youtu.be/bfYV3vR6b-A?feature=shared", "description": "예방을 위해선 어떤 노력을? 치료는 어떻게… "},
        {"link": "https://youtu.be/1LvXgJJwVAI?feature=shared", "description": "산후우울증 예방을 위해 명심해야 할것"}
    ]

    # 각 영상을 그리드 형태로 배치
    col1, col2, col3 = st.columns(3)

    for i, video_info in enumerate(video_data):
        with eval(f"col{i+1}"):
            st.video(video_info["link"])
            st.write(video_info["description"])


with tab2:

    video_data1 = [
        {"link": "https://youtu.be/ptaJoWapgn8?feature=shared", "description": "슬기롭게 산후우울증 극복하는 세가지 방법"},
        {"link": "https://youtu.be/pWBcSvJzdVQ?feature=shared", "description": "산후우울증 극복하기/ 임신 출산 후 우울감은 왜 생길까?"},
        {"link": "https://youtu.be/PDqGEFPpiUE?feature=shared", "description": "아이도 같이 행복해지는 산후 우울증 극복하기"}
    ]

    # 각 영상을 그리드 형태로 배치
    col1, col2, col3 = st.columns(3)

    for i, video_info in enumerate(video_data1):
        with eval(f"col{i+1}"):
            st.video(video_info["link"])
            st.write(video_info["description"])


with tab3:

    video_data2 = [
        {"link": "https://youtu.be/JkMauvDHAzk?feature=shared", "description": "내 남편이 산후우울증?"},
        {"link": "https://youtu.be/E33Bzdav3Bo?feature=shared", "description": "엄마의 산후우울증을 몰랐던 아빠?"},
        {"link": "https://youtu.be/oMsyz-0IChM?feature=shared", "description": "아내가 출산 후 예민해졌어요. 어떻게 도와줘야 하나요?"}
    ]

    # 각 영상을 그리드 형태로 배치
    col1, col2, col3 = st.columns(3)

    for i, video_info in enumerate(video_data2):
        with eval(f"col{i+1}"):
            st.video(video_info["link"])
            st.write(video_info["description"])





with st.sidebar:
    menu = option_menu("MomE", ['Home','Dashboard','Diary','육아 SNS','To do list','하루 자가진단', 'LogOut'],
                        icons=['bi bi-house-fill','bi bi-grid-1x2-fill','book-half','Bi bi-star-fill','Bi bi-calendar-check' ,'bi bi-capsule-pill', 'box-arrow-in-right'],
                        menu_icon="baby", default_index=1,
                        styles={
                            "icon": {"font-size": "23px"},
                            "title": {"font-weight": "bold"}  # MomE 글씨를 볼드체로 변경
                        })

    # 선택된 메뉴에 따라 페이지 변경
if menu =='Home':
    st.switch_page("pages/home.py")
elif menu =='Diary':
    st.switch_page("pages/diary_page.py")
elif menu == '육아 SNS':
    st.switch_page("pages/SNS2.py")
elif menu == 'To do list':
    st.switch_page("pages/daily_schedule.py")
elif menu =='하루 자가진단': 
    st.switch_page("pages/self_diagnosis.py")
elif menu =='LogOut':
    st.switch_page("dd1.py")