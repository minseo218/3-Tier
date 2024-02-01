import os
import subprocess
import datetime
import json
import gzip
import shutil
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import traceback

# 환경 변수 설정
db_name = "db_name"  # 데이터베이스 이름
db_user = "db_user_name"        # 백업 사용자 이름
db_password = "your_db_password"       # 백업 사용자 비밀번호
backup_path = "backup_local_path"  # 로컬 백업 경로
remote_user = "remote_server_user_name"      # 원격 서버 사용자 이름
remote_ip = "remote_server_ip"         # 원격 서버 IP 주소
remote_path = "your_backup_remote_path"  # 원격 서버 백업 경로
slack_token = "your_app_token"  # Slack 토큰
channel_id = "your_channel_id"    # Slack 채널 ID

# Slack 클라이언트 초기화
client = WebClient(token=slack_token)

def backup_db():
    # 현재 날짜 및 시간을 이용한 백업 파일 이름 생성 
    date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"{db_name}_{date}.sql"
    backup_filepath = os.path.join(backup_path, backup_filename)

    # MariaDB 백업 명령어 실행
    os.system(f"mysqldump -u {db_user} -p{db_password} {db_name} > {backup_filepath}")

    # 파일 압축
    with open(backup_filepath, 'rb') as f_in, gzip.open(f'{backup_filepath}.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    os.remove(backup_filepath)

    return backup_filepath + ".gz"

def send_to_remote_server(local_file):
    # SCP를 사용하여 로컬 파일을 원격 서버로 전송
    scp_command = f"scp {local_file} {remote_user}@{remote_ip}:{remote_path}"
    process = subprocess.Popen(scp_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.communicate()

def send_slack_message(message):
    try:
        # Slack 메시지 전송
        response = client.chat_postMessage(channel=channel_id, text=message)
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")

def main():
    try:
        start_time = datetime.datetime.now()
        # 데이터베이스 백업
        backup_file = backup_db()
        # SCP를 사용하여 백업 파일 전송
        send_to_remote_server(backup_file)
        
        end_time = datetime.datetime.now()
        elapsed_time = (end_time - start_time).total_seconds()
        backup_size = os.path.getsize(backup_file)

        # 결과 정보 전송
        message = (f"Backup이 정상적으로 완료되었답니다 :) 걱정마세효!\n"
                   f"Database: {db_name}\n"
                   f"Backup File: {backup_file}\n"
                   f"Size: {backup_size} bytes\n"
                   f"Start Time: {start_time}\n"
                   f"End Time: {end_time}\n"
                   f"Total Time: {elapsed_time} seconds")
        send_slack_message(message)
    except Exception as e:
        error_message = f"Backup 중 오류가 발생하였습니다"
        error_message += traceback.format_exc()
        send_slack_message(error_message)

if __name__ == "__main__":
    main()

