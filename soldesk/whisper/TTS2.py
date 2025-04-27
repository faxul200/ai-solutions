from openai import OpenAI
import pygame
with open("./GPT_Key.txt", "r") as f:
  api_key = f.read().strip()
client = OpenAI(
  api_key=api_key
)

# OpenAI 클라이언트에서 음성 합성(TTS: Text-to-Speech)을 요청하는 코드
response = client.audio.speech.create(
    model="tts-1",  # 사용하려는 텍스트-음성 변환(TTS) 모델 지정 ("tts-1" 모델)
    voice="nova",   # 사용할 음성의 이름을 지정 ("nova"는 선택한 음성)
    input='''
    해외 주식 세금 안내입니다. 
    해외 주식은 양도 소득세를 매년 5월에 정산해야하며 250만원 까지는 세금을 할당하지 않습니다.
    만약 500만원의 수익이 발생한다면 250만원을 제외한 250만원에 대해서, 세금 22%인 55만원을
    납부하셔야합니다.
    ''',
)

response.write_to_file("TTS2.mp3")

# pygame 믹서 초기화
pygame.mixer.init()

# mp3 파일 로드
pygame.mixer.music.load('TTS2.mp3')

# mp3 파일 재생
pygame.mixer.music.play()

# 음악이 끝날 때까지 프로그램 실행 유지
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10) # Clock(): 프레임 속도를 제어하는 데 사용, tick(10): 초당 10 프레임
    
'''
activate ai
python TTS2.py
'''

