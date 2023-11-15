import pymysql
from dbutils.pooled_db import PooledDB

host = 'localhost'
port = 3306
user = 'root'
password = ''
database = ''

class db:

    def __init__(self):
        self.pool = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            mincached=10,  # 初始化时，链接池中至少创建的链接，0表示不创建
            maxconnections=200,  # 连接池允许的最大连接数，0和None表示不限制连接数
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )

    def open(self):
        self.conn = self.pool.connection()
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)  # 表示读取的数据为字典类型
        return self.conn, self.cursor

    def close(self, cursor, conn):
        cursor.close()
        conn.close()

    def select_one(self, sql, *args):
        """查询单条数据"""
        conn, cursor = self.open()
        cursor.execute(sql, args)
        result = cursor.fetchone()
        self.close(conn, cursor)
        return result

    def select_all(self, sql, args):
        """查询多条数据"""
        conn, cursor = self.open()
        cursor.execute(sql, args)
        result = cursor.fetchall()
        self.close(conn, cursor)
        return result

    def insert_one(self, sql, args):
        """插入单条数据"""
        self.execute(sql, args, isNeed=True)

    def insert_all(self, sql, datas):
        """插入多条批量插入"""
        conn, cursor = self.open()
        try:
            cursor.executemany(sql, datas)
            conn.commit()
            return {'result': True, 'id': int(cursor.lastrowid)}
        except Exception as err:
            conn.rollback()
            return {'result': False, 'err': err}

    def update_one(self, sql, args):
        """更新数据"""
        self.execute(sql, args, isNeed=True)

    def delete_one(self, sql, *args):
        """删除数据"""
        self.execute(sql, args, isNeed=True)

    def execute(self, sql, args, isNeed=False):
        """
        执行
        :param isNeed 是否需要回滚
        """
        conn, cursor = self.open()
        if isNeed:
            try:
                cursor.execute(sql, args)
                conn.commit()
            except:
                conn.rollback()
        else:
            cursor.execute(sql, args)
            conn.commit()
        self.close(conn, cursor)