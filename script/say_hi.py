
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from config_reader import read_slack_config

# 설정 읽기
slack_config = read_slack_config()
slack_token = slack_config['token']
channel_id = slack_config['channel_id']

# 슬랙 봇과 연결
client = WebClient(token=slack_token)


try:
    response = client.chat_postMessage(
        channel= channel_id, #채널 id를 입력합니다.
        text="안녕하세요~!"
    )
except SlackApiError as e:
    assert e.response["error"]
