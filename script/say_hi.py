
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

slack_token = "your_app_token"
# 슬랙 봇과 연결
client = WebClient(token=slack_token)


try:
    response = client.chat_postMessage(
        channel="your_channel_id", #채널 id를 입력합니다.
        text="안녕하세요~!"
    )
except SlackApiError as e:
    assert e.response["error"]
