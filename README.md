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
    
   
#### 2. db_backup.py

: automatically proceed db_backup and send message to slack
  
#### 3. status.py

: check the cron service and send message to slack
