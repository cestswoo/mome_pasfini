# import yaml
# import streamlit_authenticator as stauth
# from streamlit_authenticator.utilities.hasher import Hasher

# names = ["yunhae"]
# usernames = ["yunhae"]
# passwords = ["1234"] # yaml 파일 생성하고 비밀번호 지우기!

# hashed_passwords = Hasher(passwords).generate() # 비밀번호 해싱
# print(hashed_passwords)

# data = {
#     "credentials" : {
#         "usernames":{
#             usernames[0]:{
#                 "name":names[0],
#                 "password":hashed_passwords[0]
#                 },   
                     
#             }
#     },
#     "cookie": {
#         "expiry_days" : 0, # 만료일, 재인증 기능 필요없으면 0으로 세팅
#         "key": "some_signature_key",
#         "name" : "some_cookie_name"
#     },
#     "preauthorized" : {
#         "emails" : [
#             "susu12356@gmail.com"
#         ]
#     }
# }

# with open('config.yaml','w') as file:
#     yaml.dump(data, file, default_flow_style=False)



# import yaml
# import streamlit as st
# import streamlit_authenticator as stauth
# from streamlit_authenticator.utilities.hasher import Hasher

# def add_user_to_config():
#     names = []
#     usernames = []
#     passwords = [] # yaml 파일 생성하고 비밀번호 지우기!
#     username = st.text_input("Enter username")
#     password = st.text_input("Enter password", type="password")
#     email = st.text_input("Enter email")
#     submitted = st.button("submit")
#     if submitted:
#         names.append(username)
#         usernames.append(username)
#         passwords.append(password)

#         hashed_passwords = Hasher(passwords).generate() # 비밀번호 해싱
#         print(hashed_passwords)

#         data = {
#             "credentials" : {
#                 "usernames":{
#                     usernames[0]:{
#                         "name":names[0],
#                         "password":hashed_passwords[0]
#                     },    
#                 }
#             },
#             "cookie": {
#                 "expiry_days" : 0, # 만료일, 재인증 기능 필요없으면 0으로 세팅
#                 "key": "some_signature_key",
#                 "name" : "some_cookie_name"
#             },
#             "preauthorized" : {
#                 "emails" : [
#                     email
#                 ]
#             }
#         }

#         with open('config.yaml','w') as file:
#             yaml.dump(data, file, default_flow_style=False)