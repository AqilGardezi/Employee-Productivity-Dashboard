import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from prod_app.HierarchyProdQuery import *
from prod_app.db_config import DbModulee
import pymssql
import os
import warnings


pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)
warnings.filterwarnings('ignore')


class GetDirectors:
    def __init__(self) -> None:
        self.db_obj = DbModulee()

    def directorsData(self):
        con,cur = self.db_obj.live_db()
        do = directors1()
        directors = pd.read_sql(do,con)
        self.db_obj.db_close(con,cur)
        

        return directors



