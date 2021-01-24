import pymysql


class Database:
    _connection = pymysql.connect(host='srv-mondo', user='oko', passwd='', port=3306)

    @staticmethod
    def get_connection():
        return Database._connection

