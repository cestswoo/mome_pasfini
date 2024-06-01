import streamlit as st
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import random
import pandas as pd
import sqlite3
from datetime import datetime
from streamlit_option_menu import option_menu
import plotly.express as px

# 모델과 토크나이저 로드
model_name = 'nlptown/bert-base-multilingual-uncased-sentiment'
model_dir = "./models"

# 모델과 토크나이저를 로컬 디렉토리에서 로드
@st.cache_resource
def load_model_and_tokenizer():
    tokenizer = BertTokenizer.from_pretrained(model_name, cache_dir=model_dir, use_fast=True)
    model = BertForSequenceClassification.from_pretrained(model_name, cache_dir=model_dir)
    return tokenizer, model

tokenizer, model = load_model_and_tokenizer()

# SentiWord_Dict.txt 파일 로드 함수
def load_sentiword_dict(file_path):
    senti_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) == 2:  # Ensure there are exactly two parts
                word, score = parts
                senti_dict[word] = int(score)
    return senti_dict

# SentiWord_Dict.txt 파일 로드
sentiword_dict = load_sentiword_dict('pages/SentiWord_Dict.txt')

# BERT를 사용한 감성 분석 함수
def analyze_sentiment_bert(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    return probs.detach().numpy()[0]  # 첫 번째 결과만 반환

# 감성 점수 해석 및 메시지 반환 함수
def interpret_sentiment(probabilities):
    sentiments = ['매우 부정적', '부정적', '중립', '긍정적', '매우 긍정적']
    sentiment_probs = dict(zip(sentiments, probabilities))
    max_sentiment = max(sentiment_probs, key=sentiment_probs.get)

    messages = {
        '매우 부정적': ['오늘은 정말 힘든 하루였겠네요. 다음에는 분명 좋은 일들이 생길 거예요.', '하루를 마무리하기까지 정말 힘든 시간을 보내셨겠네요. 내일은 분명 더 나은 날이 될 거예요.', '어려운 하루를 보내셨겠어요. 하지만 그런 날들도 우리를 성장시키고 더 강하게 만들어 줍니다.',
                    '하루가 정말 어려웠겠어요. 하지만 고난을 이겨내는 데서 우리의 힘과 인내심을 발견할 수 있어요.', '오늘은 정말 힘든 날이었을 텐데요. 내일은 분명 더 나은 날이 올 거예요. 희망을 잃지 마세요.', '힘든 하루를 보내셨겠죠. 하지만 용기를 가져요. 내일은 새로운 시작이니까요.',
                    '힘든 하루를 보내셨군요, 곧 좋은 날이 올 거예요.','당신은 혼자가 아니에요, 함께 이겨낼 수 있어요.','항상 응원할게요. 당신은 소중한 존재라는 것을 잊지 마세요.','많이 힘드셨겠군요. 저는 당신이 얼마나 노력했는지 알고 있어요.'],
        '부정적': ['오늘은 정말 힘드셨을 테지만, 이런 날들도 지나갈 거예요.', '고된 하루를 보내셨겠네요. 내일은 분명히 더 나은 날이 될 거예요.', '어려운 하루를 보내셨을 텐데, 내일은 조금 더 나은 날이 될 거예요.',
                 '오늘은 정말 힘든 하루였겠지만, 이겨내는 데에는 항상 가치가 있어요.', '고된 하루를 보내셨겠지만, 내일은 새로운 시작이 될 거예요.', '힘든 시간을 보내셨겠어요. 하지만 그런 날들도 극복할 수 있을 거예요.',
                 '하루가 고된 시간이었을 테지만, 이런 날들도 우리를 더 강하게 만들어 줄 거예요.','지금 느끼는 감정은 자연스러운 거예요. 조금씩 나아질 거예요.','오늘도 수고했어요. 자신만을 위한 시간을 가져보는 건 어떨까요?'],
        '중립': ['평범한 하루였겠네요. 가끔은 그런 일상의 조용한 순간들이 가장 소중한 법이죠.', '일상적인 하루를 보내셨겠어요. 때로는 평온함이 가장 큰 축복이 될 수 있어요.', '무탈한 하루를 보내셨네요. 가벼운 일상 속에서도 소중한 순간들을 발견할 수 있어요.',
                '평범한 하루가 지나갔네요. 그 속에서도 소중한 것들을 발견할 수 있었길 바라요.', '무탈한 하루를 보내셨군요. 가끔은 일상의 안정이 최고의 선물일 때도 있어요.', '일상적인 하루가 지나갔어요. 하지만 그 속에서도 행복한 순간들이 있었을 거예요.',
                '오늘도 잘 이겨내셨어요. 작은 노력이 쌓여 결국 큰 변화를 이룰 거예요.','당신은 조금씩 성장하고 있다고 믿어요. 계속 나아가봐요.','무탈한 하루 중 미소 짓는 순간이 있었길 바라요. 오늘도 수고 많았어요.'],
        '긍정적': ['좋은 하루를 보내셨군요! 오늘은 그런 하루였나 봐요.', '행복한 하루를 보내셨겠어요! 이런 날들이 계속되길 바랄게요.', '좋은 하루를 보내셨네요! 감사한 마음으로 잠자리에 들 수 있을 거예요.',
                 '기쁜 하루를 보내셨겠어요! 더 많이 좋은 일들이 찾아오길 기대할게요.', '행복한 하루를 보내셨나 봐요! 이 기분을 잊지 않도록 노력해요.', '좋은 하루를 보내셨군요! 그 기쁨이 계속 이어지길 바라요.',
                 '행복한 하루를 보내셨겠어요! 오늘의 기쁨을 내일도 느낄 수 있길 바랄게요','행복한 하루를 보내셨군요! 이런 순간들이 매일 찾아오길 바랄게요','좋은 하루를 보내셨군요. 오늘 하루도 수고한 당신이 자랑스러워요!'],
        '매우 긍정적': ['정말 멋진 하루를 보내셨겠네요! 이런 순간이 계속 이어지길 바랄게요.', '최고의 하루를 보내셨군요! 이 기쁨이 더 오래 이어지길 기대할게요.', '놀라운 하루를 보내셨군요! 이런 순간이 더 자주 찾아오길 기대할게요.',
                    '놀라운 하루를 보내셨군요! 이 기쁨을 주변 사람들과 공유해보세요.', '정말 대단한 하루를 보내셨어요! 이런 기쁨이 더 많은 일상에 녹아들길 기대할게요.', '최상의 하루를 보내셨군요! 이런 순간을 기억하고 새로운 도전에도 힘을 내보세요.',
                    '정말 훌륭한 하루를 보내셨군요! 이런 순간들이 계속 당신과 함께하길 바랄게요.','놀라운 하루를 보내셨나 봐요! 이 기쁨을 계속 느끼며 더 많은 일에 도전해보세요.','멋진 하루를 보내셨겠네요! 매일이 오늘 같기를 바라요.']
    }

    random_message = random.choice(messages[max_sentiment])

    return sentiment_probs, random_message

# SentiWord_Dict.txt를 사용하여 일기에서 단어 찾기 함수
def find_sentiwords(text, senti_dict):
    found_words = []
    for word in text.split():
        if word in senti_dict:
            found_words.append((word, senti_dict[word]))
    return found_words

# 주제 리스트 정의
topics = [
'일주일 중 가장 기억에 남는 순간에 대해 써 보세요.', '여태까지 당연시해 왔지만 사실 숨겨져 있었던 재능이 있다면 무엇일까요?', '친구들이 놀랄 만한 나의 좋은 점은 무엇인가요?', '최근 경험한 것 중 가장 좋았거나 경외심을 불러일으켰던 순간은 무엇인가요?', '최근의 일들을 되돌아 보고 이번 주에 즐거움을 준 것에 대해 적어보세요.', '혼자서 일할 때와 다른 사람과 함께 일할 때 언제 더 창의적이라고 느끼나요? 왜 그런다고 생각하나요?',
    '어렸을 때 가장 즐겼던 예술 활동이나 다른 창의적인 활동에 대해 적어 보세요', '최근에 영감을 받았던 경험을 떠올려 보세요. 어떤 것으로 인해 영감을 받았는지 생각해 보세요.', '아는 사람 중 가장 창의력이 풍부한 사람은 누구인가요? 그 사람의 창의력에 대해 적어보세요.', '최근에 했던 새로운 아이디어를 생각해 보세요. 어떤 계기로 이런 아이디어가 떠올랐고 이 아이디어를 위해 어떻게 시간을 낼 수 있었나요?', '최근에 한 가지 배운 것이 있다면 무엇인가요? 그것은 어떤 면에서 중요한가요?', '밤에 잠 못 이루게 하는 생각은 무엇인가요?',
    '소중한 관계인 사람을 마음에 떠올려 보고 그 관계에서 배울 수 있는 점을 적어보세요.', '최근에 배운 것 중 모두가 알았으면 하는 것이 있나요?', '지금까지 만난 사람 중 가장 지혜로운 사람은 누구이며, 왜 그런가요?', '아이에게 가장 놀랐던 순간이 있었나요? 그 순간을 공유해주세요.', '배우자에게 감동 받았던 기억이 있나요? 그 기억을 공유해주세요.', '아이에게 감동 받았던 순간이 있나요? 그 순간을 적어주세요.', '아이를 기르며 가장 힘들었던 순간은 언제인가요? 그 순간을 말해주세요.', '배우자와 보낸 가장 기억에 남는 시간은 언제인가요? 그 시간의 기억을 말해주세요.',
    '언제 아이가 나를 웃게 만드나요?', '지금 이 순간에 감사한 것들이 있나요?', '오늘 나에게 해주고 싶은 위로와 격려의 말이 있나요?', '주변 사람들에게 받은 지지와 응원의 말들을 기록해주세요.', '나 자신에게 주고 싶은 작은 선물이나 보상을 적어주세요.', '오늘 나의 몸과 마음의 상태를 체크하고, 나를 위한 휴식 방법을 적습니다.', '아기의 작은 변화나 성장 과정을 적어보세요.', '아기를 돌보는 중에도 나만을 위한 시간을 가졌던 순간을 적어보세요.', '하루 일과를 정리해보고, 그 중에서 좋았던 부분들을 적어보세요.', '마음 챙김이나 명상을 하며 느꼈던 평온한 감정을 기록 해보세요'
]

# 주제 추천 함수
def recommend_topics(topics, num=6):
    return random.sample(topics, num)

# SQLite 데이터베이스 초기화 함수
def init_db():
    conn = sqlite3.connect('diary.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            date TEXT,
            diary TEXT,
            sentiment TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

# SQLite 데이터베이스에 일기 데이터를 저장하는 함수
def save_diary_to_db(username, date, diary, sentiment, message):
    conn = sqlite3.connect('diary.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO diary (username, date, diary, sentiment, message)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, date, diary, str(sentiment), message))
    conn.commit()
    conn.close()

# SQLite 데이터베이스에서 특정 사용자의 일기 데이터를 불러오는 함수
def load_diary_data(username):
    conn = sqlite3.connect('diary.db')
    cursor = conn.cursor()
    cursor.execute('SELECT date, diary, sentiment, message FROM diary WHERE username = ?', (username,))
    rows = cursor.fetchall()
    conn.close()
    return pd.DataFrame(rows, columns=['Date', 'Diary', 'Sentiment', 'Message'])

# Streamlit 앱 메인 함수
def main():
    # SQLite 데이터베이스 초기화
    init_db()

    # CSS 스타일 추가
    st.markdown(
        """
        <style>
        body {
            background-color: #FFFFFF; /* 배경을 흰색으로 설정 */
            color: #000000; /* 글자색을 검은색으로 설정 */
            font-family: 'Helvetica', sans-serif; /* 폰트를 Helvetica로 설정 */
        }
        .reportview-container .main .block-container {
            max-width: 80%; /* 전체 컨테이너의 최대 너비 설정 */
            margin: auto; /* 중앙 정렬 */
            padding: 2rem; /* 패딩 추가 */
        }
        .stTextArea textarea {
            height: 300px !important; /* 텍스트 영역의 높이를 300px로 설정 */
            font-size: 16px; /* 텍스트 영역의 폰트 크기 설정 */
        }
        .stButton button {
            background-color: #FFF9EF; /* 윤해 피그마에 있는 색 아무거나 가져옴 */
            color: white; /* 버튼 글자색을 흰색으로 설정 */
            border: none; /* 버튼 테두리 없애기 */
            border-radius: 12px; /* 버튼 테두리를 둥글게 설정 */
            padding: 10px 24px; /* 버튼 패딩 설정 */
            text-align: center; /* 텍스트 중앙 정렬 */
            text-decoration: none; /* 텍스트 데코레이션 없애기 */
            display: inline-block; /* 인라인 블록 설정 */
            font-size: 16px; /* 버튼 폰트 크기 설정 */
            margin: 4px 2px; /* 버튼 외부 마진 설정 */
            cursor: pointer; /* 커서를 포인터로 설정 */
        }
        .stButton button:hover {
            background-color: #FFEEEE; /* 버튼 호버 시 배경색 설정 */
        }
        .stDataFrame {
            font-size: 16px; /* 데이터프레임 폰트 크기 설정 */
        }
        .topic-card {
            background-color: #f9f9f9; /* 추천 주제 카드 배경색 설정 */
            border-radius: 8px; /* 카드 테두리를 둥글게 설정 */
            padding: 10px; /* 카드 패딩 설정 */
            margin: 5px 0; /* 카드 외부 마진 설정 */
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 카드 그림자 설정 */
            color: #000000; /* 카드 글자색을 검은색으로 설정 */
            font-size: 16px; /* 카드 폰트 크기 설정 */
        }
        /* title 스타일 추가 */
        .stMarkdown h1 {
            font-size: 24px; /* title 폰트 크기 설정 */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        st.title("오늘 하루는 어떠셨나요? 일기를 작성해주세요!")

        tabs = st.tabs(["일기 작성", "분석 결과", "지난 일기"])

        with tabs[0]:
            st.write("### 일기 주제 추천")
            recommended_topics = recommend_topics(topics, num=6)

            topic_cols = st.columns(2)  # 2열 형태로 만들기 위해 내부 열 구성

            for idx, topic in enumerate(recommended_topics):
                with topic_cols[idx % 2]:  # 2열로 나누어 주제 표시
                    st.markdown(f"<div class='topic-card'>• {topic}</div>", unsafe_allow_html=True)

            user_input = st.text_area("텍스트를 입력하세요:", "여기에 일기를 작성해 주세요.")
            
            if st.button("분석하기"):
                probabilities = analyze_sentiment_bert(user_input)
                sentiment_probs, result_message = interpret_sentiment(probabilities)

                # 일기 데이터 저장
                save_diary_to_db(st.session_state['logged_in_user'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user_input, sentiment_probs, result_message)

                # 상태에 분석 결과 저장
                st.session_state['sentiment_probs'] = sentiment_probs
                st.session_state['result_message'] = result_message
                st.session_state['user_input'] = user_input

                st.success("분석이 완료되었습니다. '분석 결과' 탭을 확인하세요.")

        with tabs[1]:
            if 'sentiment_probs' in st.session_state:
                st.write("### 분석 결과")
                st.write("감정 확률 분포:")
                for sentiment, prob in st.session_state['sentiment_probs'].items():
                    st.write(f"{sentiment}: {prob:.2%}")
                st.write(f"선택된 메시지: {st.session_state['result_message']}")
                
                # 시각화 추가
                st.write("### 감정 분포")
                # 원형 차트로 변경
                fig = px.pie(names=st.session_state['sentiment_probs'].keys(), values=st.session_state['sentiment_probs'].values())
                st.plotly_chart(fig)
                
                # SentiWord_Dict.txt에서 단어 찾기
                found_words = find_sentiwords(st.session_state['user_input'], sentiword_dict)
                if found_words:
                    negative_words = [word for word, score in found_words if score < 0]
                    positive_words = [word for word, score in found_words if score > 0]

                    st.write("### 일기에서 발견된 감성 단어")
                    if negative_words:
                        st.write(f"사용한 부정 단어: {', '.join(negative_words)}")
                    else:
                        st.write("사용한 부정 단어가 없습니다.")
                    
                    if positive_words:
                        st.write(f"사용한 긍정 단어: {', '.join(positive_words)}")
                    else:
                        st.write("사용한 긍정 단어가 없습니다.")
                else:
                    st.write("일기에서 감성 단어를 찾을 수 없습니다.")
            else:
                st.write("아직 분석 결과가 없습니다. 먼저 '일기 작성' 탭에서 분석을 진행하세요.")

        with tabs[2]:
            st.write("### 지난 일기")
            diary_data = load_diary_data(st.session_state['logged_in_user'])
            
            if not diary_data.empty:
                selected_date = st.selectbox("날짜 선택", diary_data['Date'].unique())
                
                if selected_date:
                    entry = diary_data[diary_data['Date'] == selected_date].iloc[0]
                    st.write(f"**일기 내용 ({selected_date})**:")
                    st.write(entry['Diary'])
                    st.write("**감정 확률 분포**:")
                    sentiment_probs = eval(entry['Sentiment'])
                    for sentiment, prob in sentiment_probs.items():
                        st.write(f"{sentiment}: {prob:.2%}")
                    st.write(f"**선택된 메시지**: {entry['Message']}")
            else:
                st.write("아직 저장된 일기가 없습니다.")
    else:
        st.error("로그인 후 이용해주세요")

with st.sidebar:
    menu = option_menu("MomE", ['Home','Dashboard','Diary','육아 SNS','To do list', '하루 자가진단', 'LogOut'],
                        icons=['bi bi-house-fill','bi bi-grid-1x2-fill','book-half','Bi bi-star-fill','Bi bi-calendar-check' ,'bi bi-capsule-pill', 'box-arrow-in-right'],
                        menu_icon="baby", default_index=2,
                        styles={
                            "icon": {"font-size": "23px"},
                            "title": {"font-weight": "bold"}  # MomE 글씨를 볼드체로 변경
                        })

# 선택된 메뉴에 따라 페이지 변경
if menu =='Home':
    st.switch_page("pages/home.py")
elif menu =='Dashboard':
    st.switch_page("pages/dashboard_page.py")
elif menu == '육아 SNS':
    st.switch_page("pages/SNS2.py")
elif menu == 'To do list':
    st.switch_page("pages/daily_schedule.py")
elif menu =='하루 자가진단': 
    st.switch_page("pages/self_diagnosis.py")
elif menu =='LogOut':
    st.switch_page('dd1.py')

if __name__ == "__main__":
    main()
