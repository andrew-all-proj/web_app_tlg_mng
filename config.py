from pathlib import Path

BASE_DIR = Path(__file__).parent
NAME_DB = "testdb"
USER_NAME_DB = "postgres"
PASSWORD_DB = 1
PATH_FOR_MEDIA = 'D:\projects\web_site\web_server_spgt-master\static\media'
TIME_REMOVE_EVENT = 1440
USR_NAME = 'admin'
# Секрет ключ для flash сообщенний
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'


class Config:
    SQLALCHEMY_DATABASE = f"postgresql+psycopg2://{USER_NAME_DB}:{PASSWORD_DB}@localhost/{NAME_DB}"
    PATH_LOG_FILE = f"{BASE_DIR}/log_bot.log"
    PATH_FOR_MEDIA = Path(__file__).parent
    SECRET_KEY = SECRET_KEY
    TIME_REMOVE_EVENT = TIME_REMOVE_EVENT
