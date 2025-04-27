import os
import time
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import openai
import tool
from werkzeug.utils import secure_filename

app = Flask(__name__)  # __name__ == '__main__'
CORS(app)

# app.config['UPLOAD_FOLDER']='C:/ai/deploy/whisper/storage'

# 업로드할 파일의 최대 크기 설정 (16MB로 설정 예시)
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Flask 환경 변수 설정, 허용 가능한 파일 확장자 설정 (예: 이미지 파일만 허용하도록 설정)
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'png', 'gif'}

# '.'을 기준으로 확장자를 분리하여 소문자로 변경후 업로드 가능한 파일형식인지 체크
# rsplit('.',1) : 오른쪽에서 1번만 분활 
def allowed_file(filename):   # ccc.bbb.aaa.jpg => [ccc.bbb.aaa, jpg]
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# 25 M 제한
def allowed_size(size):
    return True if size <= 1024 * 1024 * 25 else False

# 기본페이지 http://127.0.0.1:5000
@app.get('/')
def index():
    return "파일 업로드 서비스"

# 파일 전송 폼
@app.get("/fileupload") # http://localhost:5000/fileupload
def fileupload_form():
    return render_template("fileupload.html")
# 파일 전송 처리
@app.post("/fileupload") # http://localhost:5000/fileupload
def fileupload_proc():  
    time.sleep(3) #3초 중지
    f = request.files['file'] 
    file_size = len(f.read())
    f.seek(0) # 파일 포인터를 처음으로 이동
    
    if allowed_size(file_size) == False:
        resp = jsonify({'message': "파일 사이즈가 25M를 넘습니다." + str(file_size/1024/1024) + ' M'})  # dict -> json string
        resp.status_code = 500 # 서버 에러
    
    # 허용 가능한 파일 확장자인지 확인
    if f and allowed_file(f.filename):
        # 저장할 경로 지정 (예: 'storage' 폴더에 저장)
        upload_folder = 'storage'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        # 파일저장
        f.save(os.path.join(upload_folder,f.filename))
        # filename = secure_filename(f.filename)  # 파일명 보안 처리
        # f.save(os.path.join(upload_folder, filename))  # 파일 저장
                
        # dict -> json string
        resp = jsonify({'message':'파일을 저장했습니다.'})

    else:
        resp = jsonify({'message': '전송 할 수 없는 파일 형식입니다.'})  # dict -> json string
        # resp.status_code = 500 # 서버 에러
        
    return resp

    
app.run(host="0.0.0.0", port=5000, debug=True)  # 0.0.0.0: 모든 Host 에서 접속 가능, python recommend_movie.py

'''
activate ai
python fileupload.py
http://localhost:5000/fileupload
'''

