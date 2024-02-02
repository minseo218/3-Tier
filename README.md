## System Info
#### Ubuntu-22.0
#### Python 3.10.12


## How to use this scirpt
#### 1. Download the requirments.txt , variable.conf, config_reader.conf and scirpt files
#### 2. Run requirments file using `pip install -r requirements.txt`
#### 3. Change the variable
  config file has `slack_token` and `channel`.
  
  You have to add your slack app token and channel code at there.

  Also there are other variables. 
  
  You can enter if you need that.

#### 4. Run python script
  `python3 say_hi.py`
  
  `python3 network.py`
  
  `python3 status.py`
  
  `python3 db_backup.py`
  

#### 4-1. If you want to use `db_backup.py`, you must install mariadb-client to usean mysqldump.
  `sudo apt-get update`
  
  `sudo apt-get install mariadb-client`


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




