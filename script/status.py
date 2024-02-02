from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import subprocess
import socket
from datetime import datetime
from config_reader import read_slack_config

# 설정 읽기
slack_config = read_slack_config()
slack_token = slack_config['token']
channel_id = slack_config['channel_id']

# 슬랙 봇과 연결
client = WebClient(token=slack_token)

def check_service_status(service_name):
    try:
        # Linux 기반 시스템에서는 systemctl을 사용하여 서비스 상태 확인
        command = f"systemctl is-active {service_name}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        status = result.stdout.strip()
        if status == "active" :
            return f"{service_name}이 잘 동작하고 있답니다 :)"
        elif status == "inactive" :
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            host_name = socket.gethostname()
            server_ip = socket.gethostbyname(host_name)
            return f"현재 서비스가 비활성화 상태입니다:( 활성화 해주세요! \n서버 IP 주소: {server_ip}, 서비스 명: {service_name}, 문제 발생 확인 시간: {current_time}"
    except subprocess.CalledProcessError as e:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        host_name = socket.gethostname()
        server_ip = socket.gethostbyname(host_name)
        error_info = f"서버 IP 주소: {server_ip}, 서비스 명: {service_name}, 문제 발생 확인 시간: {current_time}"
        return f"Error: {e.stderr}\n {error_info}"

# 서비스 상태 확인
status_message = check_service_status("cron")

try:
    response = client.chat_postMessage(
        channel = channel_id, #채널 id를 입력합니다.
        text = status_message
    )
except SlackApiError as e:
    assert e.response["error"]
