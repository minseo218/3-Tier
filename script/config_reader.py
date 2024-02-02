import configparser

def load_config(config_file='config.ini'):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

if __name__ == "__main__":
    config = load_config()

    # common 섹션
    slack_token = config.get('common', 'slack_token')
    channel_id = config.get('common', 'channel_id')

    # database 섹션
    db_name = config.get('database', 'db_name')
    db_user = config.get('database', 'db_user')
    db_password = config.get('database', 'db_password')

    # remote 섹션
    remote_user = config.get('remote', 'remote_user')
    remote_ip = config.get('remote', 'remote_ip')
    remote_path = config.get('remote', 'remote_path')

    # local 섹션
    backup_path = config.get('local', 'backup_path')
