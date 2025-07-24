import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from prod_app.HierarchyProdQuery import *
from prod_app.db_config import DbModulee
import pymssql
import os
import warnings

warnings.filterwarnings('ignore')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

class MISProd:
    def __init__(self) -> None:
        self.db_obj = DbModulee()


    def MisProdSignOff(self,ProdWeek, MisDirector,Performance):
        ProdWeek = int(ProdWeek)
        productivity_disc = ProductivityQuery()
        con,cur = self.db_obj.live_db()
        df1 = pd.read_sql(productivity_disc,con)
        self.db_obj.db_close(con,cur)

        con,cur = self.db_obj.live_db()
        DSProd = DSProdQuery()
        DSProdData = pd.read_sql(DSProd,con)
        self.db_obj.db_close(con,cur)
        
        current_date = datetime.now()
        start_date = current_date - timedelta(weeks=ProdWeek)
        start_date = start_date - timedelta(days=(start_date.weekday() + 1) % 7)
        start_date = pd.to_datetime(start_date)
        end_date = start_date + timedelta(days=6)
        end_date = pd.to_datetime(end_date)
        df1['Start_date'] = pd.to_datetime(df1['Start_date'])
        df1['End_date'] = pd.to_datetime(df1['End_date'])
        MIS_Productivity = df1[(df1['Start_date'] >= start_date) & (df1['End_date'] <= end_date)]
        
        if ProdWeek:
            pay_date_from = current_date - timedelta(days=current_date.weekday() + 7*ProdWeek)
            pay_date_from = pay_date_from - timedelta(days=(pay_date_from.weekday() - 5) % 7)
            pay_date_to = pay_date_from + timedelta(days=6)

        print("MIS Week",pay_date_from,'  ',pay_date_to)
        Productivity_path = "path"
        Productivity_folder = f"/{Productivity_path}/{pay_date_from.strftime('%b-%d')}-{pay_date_to.strftime('%b-%d-%Y')}/"
        
        
        MIS_Productivity= MIS_Productivity.rename(columns={'Employee_id':'EMPLOYEEID','ProductivityStatus':'Productivity','DisciplineStatus':'Discipline'})
        MIS_Productivity = MIS_Productivity[['EMPLOYEEID','Productivity']]

        MIS_Data = pd.read_csv(Productivity_folder+'prod_data_for_directors.csv',index_col=None)

        try:
            MIS_Data = MIS_Data.drop(columns = {'Unnamed: 0'})
        except:
            pass

        MIS_Data = MIS_Data.rename(columns = {'EMPLOYEE_ID':'EMPLOYEEID','user_id':'User_ID','user_name':'EmpName',
            'DEDUCTED_RVU':'DeductedRVU', 'PAID_RVU':'PaidRVU','BUCKET_RVU':'BucketRVU',
            'assigned':'Assigned','resolve':'Resolve','rbs_rejected':'RbsRejected','rbs_per':'RbsPer','kpi_rejected':'KpiRejected',
            'kpi_per':'KpiPer','denial':'Denial','denial_per':'DenialPer','adjusted':'Adjusted','adjusted_per':'AdjustedPer',
            'remaining':'Remaining','remaining_per':'RemainingPer','paid_now':'PaidNow','paid_now_per':'PaidNowPer',
            'active_time':'ActiveTime','normalized_rvu':'NormalizedRVU','director':'DO','mo_name':'ADO','lead':'Lead'})

        
        MIS_Data.drop(columns='User_ID',inplace=True)
        # MIS_Data.drop_duplicates(keep='first',inplace=True)

        MIS_Data['EMPLOYEEID'] = MIS_Data['EMPLOYEEID'].apply(int)
        MIS_Productivity['EMPLOYEEID'] = MIS_Productivity['EMPLOYEEID'].apply(int)

        MIS_Data['DO'] = MIS_Data['DO'].replace('NOT ASSIGNED TO ANY LEAD', 'NOT ASSIGNED')

        MISDataFinal = MIS_Data.merge(MIS_Productivity, how='left', on='EMPLOYEEID')
        MISDataFinal = MISDataFinal.sort_values(by=['RVU'], ascending=False).reset_index(drop=True)

        DSProdData['START_DATE'] = pd.to_datetime(DSProdData['START_DATE'])
        DSProdData['END_DATE'] = pd.to_datetime(DSProdData['END_DATE'])
        DSProdData = DSProdData[(DSProdData['START_DATE'] >= start_date) & (DSProdData['END_DATE'] <= end_date)]
        DSProdData.rename(columns={'PRODUCTIVITY':'DSProd'}, inplace=True)
        DSProdData = DSProdData[['EMPLOYEEID','DSProd']]
        DSProdData['EMPLOYEEID'] = DSProdData['EMPLOYEEID'].apply(int)

        MISDataFinal = MISDataFinal.merge(DSProdData, on='EMPLOYEEID', how='left')

        MISDataFinal.rename(columns={'Productivity':'GPProd'}, inplace=True)

        MISDataFinal = MISDataFinal.fillna(0)
        MISDataFinal = MISDataFinal.replace('-',0)
        MISDataFinal.replace([np.inf, -np.inf], 0, inplace=True)

        MISDataFinal = MISDataFinal[['EMPLOYEEID', 'EmpName','Lead','ADO','DO','DSProd','GPProd','RVU', 'DeductedRVU', 
            'PaidRVU','BucketRVU', 'Assigned', 'Resolve', 'RbsRejected', 'RbsPer','KpiRejected', 'KpiPer', 'Denial', 
            'DenialPer', 'Adjusted','AdjustedPer', 'Remaining', 'RemainingPer', 'PaidNow','PaidNowPer','ActiveTime',
                            'NormalizedRVU']]

        MISDataFinal.rename(columns={'EMPLOYEEID':'EmpID'}, inplace=True)
        exclude_columns = ['EmpID', 'EmpName','Lead','ADO','DO','ActiveTime']

        include_round = ['RVU', 'DeductedRVU', 
            'PaidRVU','BucketRVU', 'Assigned', 'Resolve', 'RbsRejected', 'RbsPer','KpiRejected', 'KpiPer', 'Denial', 
            'DenialPer', 'Adjusted','AdjustedPer', 'Remaining', 'RemainingPer', 'PaidNow','PaidNowPer','ActiveTime',
                            'NormalizedRVU']
        
        MISDataFinal[include_round] = MISDataFinal[include_round].round()
        MISDataFinal[exclude_columns] = MISDataFinal[exclude_columns].astype('object')
        
        MISDataFinal.drop_duplicates(subset=['EmpID'], keep='first', inplace=True)

        
        if MisDirector == 'All':
            MISDataFinal = MISDataFinal
        else:
            MISDataFinal = MISDataFinal[MISDataFinal['DO']==MisDirector].reset_index(drop=True)

        if Performance == '1':
            MISDataFinal = MISDataFinal
            # print("Length  if Performance == 1 before route..",len(MISDataFinal))
        elif Performance == '2':
            MISDataFinal = MISDataFinal.loc[MISDataFinal['RVU']>=1000].reset_index(drop=True)
            # print("Length  if Performance == 2 before route..",len(MISDataFinal))
        else:
            MISDataFinal = MISDataFinal.loc[MISDataFinal['RVU']<=300].reset_index(drop=True)
            # print("Length  if Performance == 3 before route..",len(MISDataFinal))
        

        return MISDataFinal
        
