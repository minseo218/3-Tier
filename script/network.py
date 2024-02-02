from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import json
import yaml
import csv
from datetime import datetime
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from config_reader import read_slack_config

# 설정 읽기
slack_config = read_slack_config()
slack_token = slack_config['token']
channel_id = slack_config['channel_id']

client = WebClient(token=slack_token)

def read_file_and_send_slack(file_path, channel):
    with open(file_path, 'r') as file:
        contents = file.read()

    try:
        response = client.files_upload_v2(
            channels=channel,
            content=contents,
            filename=file_path,
            initial_comment=f"Contents of {file_path}"
        )
    except SlackApiError as e:
        print(f"Error in read_file_and_send_slack: {e}")
        assert e.response["error"]

def check_network_status():
    server_ip = "172.16.1.10"

    try:
        response = requests.get(f"http://{server_ip}", timeout=5)
        status = "Success" if response.status_code == 200 else "Failed"
    except requests.ConnectionError:
        status = "Failed"

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 통계 정보 생성
    stats = {
        'timestamp': current_time,
        'server_ip': server_ip,
        'connection_status': status
    }

    # CSV 파일로 저장
    with open('network_stats.csv', 'a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=stats.keys())
        if csv_file.tell() == 0:
            writer.writeheader()
        writer.writerow(stats)

    # JSON 파일로 저장
    with open('network_stats.json', 'a') as json_file:
        json.dump(stats, json_file, indent=2)
        json_file.write('\n')

    # YAML 파일로 저장
    with open('network_stats.yaml', 'a') as yaml_file:
        yaml.dump(stats, yaml_file, default_flow_style=False)
        yaml_file.write('\n')

    # 슬랙 메시지 전송
    read_file_and_send_slack('network_stats.csv', channel_id)
    read_file_and_send_slack('network_stats.json', channel_id)
    read_file_and_send_slack('network_stats.yaml', channel_id)

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(check_network_status, 'interval', minutes=1)
    scheduler.start()
