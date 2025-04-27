from openai import OpenAI

with open("./GPT_Key.txt", "r") as f:
  api_key = f.read().strip()
client = OpenAI(
  api_key=api_key
)

# type 1
# response = client.audio.speech.create(
#     model="tts-1",
#     voice="coral",  #Shimmer, alloy, ... 6개
#     input="해외 주식 세금 안내입니다. 해외 주식은 양도 소득세를 매년 5월에 정산해야하며 250만원 까지는 세금을 할당하지 않습니다.",
# )

# response.write_to_file("TTS1.mp3")

# type 2
with client.audio.speech.with_streaming_response.create(
    model="tts-1",
    voice="shimmer",
    input="해외 주식 세금 안내입니다. 해외 주식은 양도 소득세를 매년 5월에 정산해야하며 250만원 까지는 세금을 할당하지 않습니다."
) as response:
    response.stream_to_file("TTS1_2.mp3")
    
'''
python TTS.py
'''