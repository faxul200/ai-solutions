import os
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import time
import tool
from openai import OpenAI
import base64
import json

with open("./GPT_Key.txt","r") as fa:
    api_key = fa.read().strip()

client = OpenAI(
  api_key=api_key
)

app = Flask(__name__)  # __name__ == '__main__'
CORS(app)

# app.config['UPLOAD_FOLDER']='C:/ai/deploy/whisper/storage'

# 업로드할 파일의 최대 크기 설정 (16MB로 설정 예시)
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# 허용 가능한 파일 확장자 설정 (예: 이미지만 허용하도록 설정)
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# 25 M 제한
def allowed_size(size):
    return True if size <= 1024 * 1024 * 25 else False

# image base64인코딩, utf-8변환
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# 기본페이지
@app.get("/")
def index():
    return "Web기반 image인식 서비스"
# Ajax 기반 파일 업로드 폼    
@app.get("/menu_web") # http://localhost:5000/menu_web
def menu_web_form():
    return render_template('menu_web.html')

# Ajax 기반 파일 업로드 처리    
@app.post("/menu_web") # http://localhost:5000/menu_web
def menu_web_proc():
    time.sleep(3)
    #유저가 업로드한 파일 받기
    f = request.files['file']
    file_size = len(f.read())
    #파일포인터를 맨 처음으로 이동
    f.seek(0)
    # print('-> file_size:', file_size)
    
    if allowed_size(file_size) == False: # 25 MB 초과
        resp = jsonify({'message': "파일 사이즈가 25M를 넘습니다. 파일 용량: " + str(round(file_size/1024/1024)) + ' MB'})
        resp.status_code = 500 # 서버 에러
        return resp
    # else: # 25 MB 이하
    if f and allowed_file(f.filename): # 허용 가능한 파일 확장자인지 확인
        # 저장할 경로 지정,절대경로 (예: 'static/uploads' 폴더에 저장)
        upload_folder = os.path.join(os.getcwd(),'static','uploads')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # 파일 저장 ★
        f.save(os.path.join(upload_folder,f.filename))

        # 파일 읽기 ★ 사용안함
        # audio_file = open(os.path.join(upload_folder,f.filename),'rb')
        
        # 업로드된 파일 경로
        image_path = os.path.join(upload_folder,f.filename)
        
        # 인코딩
        base64_image = encode_image(image_path)
        
        # 이미지 인식 서비스 Vision.opynb 에서 copy
        # transcript = client.chat.completions.create(model = "gpt-4o-mini",file=base64_image)
        
        response = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "메뉴 알려줘 \n\n출력 형식: { \"res\"':'메뉴명}"
                },
                {
                "type": "image_url",
                "image_url": 
                    {"url": f"data:image/jpeg;base64,{base64_image}"}
                }
            ]
            }
        ],
        max_tokens = 300
        )
        print(response.choices[0].message.content)
        res = response.choices[0].message.content
        json_obj = json.loads(res)
        print(f"메뉴명:{json_obj['res']}")

        fname = f.filename
        menu_name = json_obj['res']
                
        resp = jsonify({"fname": fname,"menu_name":menu_name})
        
        
        # print('->', type(resp)) # <class 'flask.wrappers.Response'>
        # resp.status_code = 201 # 정상 처리
         
        # upload된 파일 삭제 
        # 파일이 존재하는지 확인 후 삭제
        # image_path.close() # PermissionError 발생함으로 파일을 닫을 것. 사용안함
        f.close() 
        # print('-> os.path.join(upload_folder, f.filename): ', os.path.join(upload_folder, f.filename))
        # 삭제할 파일 경로 조합, storage\somewhere.mp3 
        # delete_file = os.path.join(upload_folder, f.filename) 
        
        # if os.path.exists(delete_file):
        #     os.remove(delete_file) # 파일 이용을 모두 했음으로 파일 삭제
        #     # os.remove('./storage/somewhere.mp3')
        #     print(f'{delete_file} 파일 삭제')
        # else:
        #     print(f'{delete_file} 파일 삭제 실패')

    else:
        resp = jsonify({'message': '전송 할 수 없는 파일 형식입니다.'})
            
    return resp

    
app.run(host="0.0.0.0", port=5000, debug=True)  # 0.0.0.0: 모든 Host 에서 접속 가능, python recommend_movie.py

'''
cd openai
python whisper_web.py
http://127.0.0.1:5000/whisper_web
'''
