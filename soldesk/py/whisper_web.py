import os
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import time
import tool
from openai import OpenAI

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

# 허용 가능한 파일 확장자 설정 (예: 오디오, 영상만 허용하도록 설정)
app.config['ALLOWED_EXTENSIONS'] = {'mp3', 'mp4'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# 25 M 제한
def allowed_size(size):
    return True if size <= 1024 * 1024 * 25 else False


# 기본페이지
@app.get("/")
def index():
    return "Web기반 STT서비스"
# Ajax 기반 파일 업로드 폼    
@app.get("/whisper_web") # http://localhost:5000/whisper_web
def whisper_web_form():
    return render_template('whisper_web.html')

# Ajax 기반 파일 업로드 처리    
@app.post("/whisper_web") # http://localhost:5000/whisper_web
def whisper_web_proc():
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
        # 저장할 경로 지정 (예: 'storage' 폴더에 저장)
        upload_folder = 'storage'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # 파일 저장 ★
        f.save(os.path.join(upload_folder,f.filename))

        # 파일 읽기 ★ 
        audio_file = open(os.path.join(upload_folder,f.filename),'rb')
        
        # STT 서비스
        transcript = client.audio.transcriptions.create(model='whisper-1',file=audio_file)
       # dict -> Response
        resp = jsonify({'message': transcript.text})
        print('->', type(resp)) # <class 'flask.wrappers.Response'>
        resp.status_code = 201 # 정상 처리
         
        # upload된 파일 삭제 
        # 파일이 존재하는지 확인 후 삭제
        audio_file.close() # PermissionError 발생함으로 파일을 닫을 것.
        f.close() 
        print('-> os.path.join(upload_folder, f.filename): ', os.path.join(upload_folder, f.filename))
        # 삭제할 파일 경로 조합, storage\somewhere.mp3 
        delete_file = os.path.join(upload_folder, f.filename) 
        
        if os.path.exists(delete_file):
            os.remove(delete_file) # 파일 이용을 모두 했음으로 파일 삭제
            # os.remove('./storage/somewhere.mp3')
            print(f'{delete_file} 파일 삭제')
        else:
            print(f'{delete_file} 파일 삭제 실패')

    else:
        resp = jsonify({'message': '전송 할 수 없는 파일 형식입니다.'})
        resp.status_code = 500 # 서버 에러
            
    return resp

    
app.run(host="0.0.0.0", port=5000, debug=True)  # 0.0.0.0: 모든 Host 에서 접속 가능, python recommend_movie.py

'''
cd openai
python whisper_web.py
http://127.0.0.1:5000/whisper_web
'''
