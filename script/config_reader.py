import configparser

def load_config(config_file='variable.conf'):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def read_slack_config():
    """Slack 설정 읽기"""
    config = load_config()
    return {
        'token': config.get('common', 'slack_token'),
        'channel_id': config.get('common', 'channel_id')
    }

def read_database_config():
    """데이터베이스 설정 읽기"""
    config = load_config()
    return {
        'db_name': config.get('database', 'db_name'),
        'db_user': config.get('database', 'db_user'),
        'db_password': config.get('database', 'db_password'),
        'db_port': config.get('database', 'db_port'),
        'db_ip' : config.get('database', 'db_ip')
    }

def read_remote_config():
    """원격 서버 설정 읽기"""
    config = load_config()
    return {
        'remote_user': config.get('remote', 'remote_user'),
        'remote_ip': config.get('remote', 'remote_ip'),
        'remote_path': config.get('remote', 'remote_path')
    }

def read_local_config():
    """로컬 설정 읽기"""
    config = load_config()
    return {
        'backup_path': config.get('local', 'backup_path')
    }

if __name__ == "__main__":
    config = load_config()
    slack_config = read_slack_config()
    database_config = read_database_config()
    remote_config = read_remote_config()
    local_config = read_local_config()

