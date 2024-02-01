## How to use this scirpt
#### 1. Download the requirments.txt and scirpt files
#### 2. Run requirments file using `pip install -r requirements.txt`
#### 3. Change the variable
  each file has `slack_token` and `channel`
  
  You have to add your slack app token and channel code at there.

#### 4. Run python script
  `python3 say_hi.py`
  `python3 db_backup.py`
  `python3 status.py`



## Python3 script file description
#### 1. say_hi.py
   
: send hi to your slack channel
    
   
#### 2. network.py

: check the network between localhost and other server.

  Please enther ip address into `server_ip` what you want to cheack
  
#### 3. status.py

: check the cron service and send message to slack

#### 4. db_backup.py

: automatically proceed db_backup and send message to slack

-----------------------------------

## IF YOU WANT TO USE db_backup.py , YOU HAVE TO FLLOW THIS STEP.
#### 1. Make your DB
#### 2. Create your DB user and set permission
#### 3. Enter your DB infornation into environment variables.
: there are list of environment variables.

db_name = "db_name"  # 데이터베이스 이름

db_user = "db_user_name"        # 백업 사용자 이름

db_password = "your_db_password"       # 백업 사용자 비밀번호

backup_path = "backup_local_path"  # 로컬 백업 경로

remote_user = "remote_server_user_name"      # 원격 서버 사용자 이름

remote_ip = "remote_server_ip"         # 원격 서버 IP 주소

remote_path = "your_backup_remote_path"  # 원격 서버 백업 경로

slack_token = "your_app_token"  # Slack 토큰

channel_id = "your_channel_id"    # Slack 채널 ID
