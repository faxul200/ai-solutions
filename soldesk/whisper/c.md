
mp4 용량이 커서 text 추출 오류난 최대 25MB 까지 가능함
테스트 mp4는 40메가 오류남 -> ffmpeg 를 이용해 mp3로 변환 4.8메가 -> mp3를 text로 변환

한국어 크기가 너무 큼,허용하는 최대 파일 크기(약 25MB = 26214400 바이트)
ffmpeg.exe 시스템 환경변수에 추가
ffmpeg -i kimchi.mp4 -vn -acodec libmp3lame -b:a 64k kimchi.mp3

시스템 환경변수
path 
C:\LLM\setup\whisper

ffmpeg.exe
자료실에 있어



Run SQL Command Line
오라클system.txt
