FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /usr/src/app

# 프로젝트 파일 복사
COPY . .

# 필요 라이브러리 설치
RUN pip install -r requirements.txt

# 기본 명령어를 bash로 설정
CMD ["/bin/bash"]