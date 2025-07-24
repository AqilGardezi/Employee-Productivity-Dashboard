import pymssql
import traceback



class DbModulee():
    def __init__(self) -> None:
        pass

    def live_db(self):
        con = pymssql.connect(user='',password = ''
                        ,host='',database='',appname='',autocommit = True)
        cur = con.cursor()
        return con,cur

    def cln_db(self):
        con = pymssql.connect(user='',password = ''
                        ,host='',database='',appname='',autocommit = True)
        cur = con.cursor()
        return con,cur

    def db_close(self,con,cur):
        cur.close()
        con.close()

