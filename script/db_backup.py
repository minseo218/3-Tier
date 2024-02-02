import os
import subprocess
import datetime
import json
import gzip
import shutil
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import traceback
from config_reader import read_slack_config, read_database_config, read_remote_config, read_local_config

# Slack 설정 읽기
slack_config = read_slack_config()
slack_token = slack_config['slack_token']
channel_id = slack_config['channel_id']

# 데이터베이스 설정 읽기
database_config = read_database_config()
db_name = database_config['db_name']
db_user = database_config['db_user']
db_password = database_config['db_password']

# 원격 서버 설정 읽기
remote_config = read_remote_config()
remote_user = remote_config['remote_user']
remote_ip = remote_config['remote_ip']
remote_path = remote_config['remote_path']

# 로컬 설정 읽기
local_config = read_local_config()
backup_path = local_config['backup_path']

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
