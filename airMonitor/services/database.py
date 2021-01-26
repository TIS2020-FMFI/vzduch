import pymysql
import pandas as pd
from django.conf import settings
from pymysql import DatabaseError

from airMonitor.services.tunnel import Tunnel


class Database:
    _connection = pymysql.connect(host='srv-mondo', user='oko', passwd='', port=3306)

    @staticmethod
    def get_connection():
        return Database._connection

    @staticmethod
    def execute_sql(command):
        username = settings.TUNNEL_CREDENTIALS["username"]
        password = settings.TUNNEL_CREDENTIALS["password"]
        for i in range(settings.RETRY_NUMBER):
            try:
                return pd.read_sql_query(command, Database._connection)
            except DatabaseError:
                Tunnel.initialize(username, password)
