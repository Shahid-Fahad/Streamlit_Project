import yaml
import mysql.connector as mysql
from mysql.connector.constants import ClientFlag
from sqlalchemy import create_engine


# with open('credintials.yml', 'r') as f:
#     credintials = yaml.load(f, Loader=yaml.FullLoader)
#     db_credintials = credintials['db']
#     system_pass = credintials['system_pass']['admin']
#     email_sender = credintials['email_sender']


def get_database_connection():
    db = mysql.connect(host="localhost",
                       user="root",
                       passwd="4@89kts5",
                       database="Diploma",
                       auth_plugin='mysql_native_password')
    cursor = db.cursor()

    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    print(databases)

    return cursor, db