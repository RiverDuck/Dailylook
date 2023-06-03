import requests
import json

with open('secret.json') as json_file:
    json_data = json.load(json_file)
    json_string3 = json_data["kakao_rest_key"]
    json_string4 = json_data["kakao_code_key"]
client_id = json_string3
code = json_string4

url = 'https://kauth.kakao.com/oauth/token'
client_id # '자신의 REST 키값'
redirect_uri = 'https://example.com/oauth'
code # '자신의 CODE 값'

data = {
    'grant_type':'authorization_code',
    'client_id':client_id,
    'redirect_uri':redirect_uri,
    'code': code,
    }

response = requests.post(url, data=data)
tokens = response.json()

#발행된 토큰 저장
with open("token.json","w") as kakao:
    json.dump(tokens, kakao)