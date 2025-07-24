import pandas as pd
from datetime import datetime, date, timedelta
from prod_app.HierarchyProdQuery import *
from prod_app.db_config import DbModulee
import pymssql
import os
import warnings
import glob

warnings.filterwarnings('ignore')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


class CareCloud:
    def __init__(self) -> None:
        self.db_obj = DbModulee()

    def format_with_commas(self, value):
        return "{:,.0f}".format(value)

    def CareCloudData(self,FolderWeek, CcDirector, Performance):
        try:
            HierarchyDataCC = HierarchyQuery()
            con,cur =  self.db_obj.live_db()
            CCHierarchyData = pd.read_sql(HierarchyDataCC,con)
            self.db_obj.db_close(con,cur)

            FolderWeek = int(FolderWeek)

            con,cur = self.db_obj.live_db()
            productivity_disc = ProductivityQuery()
            Productivity = pd.read_sql(productivity_disc,con)
            self.db_obj.db_close(con,cur)
            # print("Productivity",Productivity.head(1))

            con,cur = self.db_obj.live_db()
            DSProd = DSProdQuery()
            DSProdData = pd.read_sql(DSProd,con)
            self.db_obj.db_close(con,cur)

            current_date = datetime.now()
            if FolderWeek:
                pay_date_from = current_date - timedelta(days=current_date.weekday() + 7*FolderWeek)
                pay_date_from = pay_date_from - timedelta(days=(pay_date_from.weekday() - 5) % 7)
                pay_date_to = pay_date_from + timedelta(days=6)
            # print("CC Week",pay_date_from,'  ',pay_date_to)

            start_date = current_date - timedelta(weeks=FolderWeek)
            start_date = start_date - timedelta(days=(start_date.weekday() + 1) % 7)
            start_date = start_date.date()
            start_date = pd.to_datetime(start_date)
            end_date = start_date + timedelta(days=6)
            end_date = end_date.date()
            end_date = pd.to_datetime(end_date)

            Productivity['Start_date'] = pd.to_datetime(Productivity['Start_date'])
            Productivity['End_date'] = pd.to_datetime(Productivity['End_date'])
            Productivity = Productivity[(Productivity['Start_date'] >= start_date) & (Productivity['End_date'] <= end_date)]
            Productivity.rename(columns={'Employee_id':'EMPLOYEEID','ProductivityStatus':'GPProd'}, inplace=True)
            Productivity = Productivity[['EMPLOYEEID','GPProd']]
            # print("GP PROD", Productivity.head(2))

            Productivity_path = "path"
            Productivity_folder = f"{Productivity_path}/{pay_date_from.strftime('%b-%d')}-{pay_date_to.strftime('%b-%d-%Y')}/"
            
            file_name = glob.glob(f"{Productivity_folder}/CARECLOUD PRODUCTIVITY REPORT*")
            
            # import pdb

            # pdb.set_trace() 

            if file_name:
                file_name = file_name[0]

            CC_PROD = pd.read_excel(file_name)

            CC_PROD = CC_PROD.rename(columns = {'EMPLOYEE ID':'EMPLOYEEID','OLD RVU SCORE':'Old_RVU_Score',
                'CALCULATED RVU SCORE':'Calculated_RVU_Score','TOTAL':'Total','PENDING':'Pending','PAID':'Paid',
                'PREVIOUSLY PAID':'Previously_Paid', 'TOTAL REJECTIONS':'Total_Rejections','TOTAL DENIALS':'Total_Denials',
                'CORRECT PAYMENTS':'Correct_Payments','INCORRECT PAYMENTS':'Incorrect_Payments',})
            
            CC_PROD.drop(columns={'PRODUCTIVITY'}, inplace=True)

            CC_PROD[['Old_RVU_Score','Calculated_RVU_Score','Total','Pending','Paid', 'Previously_Paid', 'Total_Rejections','Total_Denials', 'Correct_Payments', 
                'Incorrect_Payments']] = round(CC_PROD[['Old_RVU_Score','Calculated_RVU_Score','Total','Pending','Paid', 'Previously_Paid', 'Total_Rejections','Total_Denials', 'Correct_Payments', 
                'Incorrect_Payments']],1)
            
            CC_PROD['EMPLOYEEID'] = CC_PROD['EMPLOYEEID'].apply(int)
            CCHierarchyData['EMPLOYEEID'] = CCHierarchyData['EMPLOYEEID'].apply(int)
            
            CcFinalData = CC_PROD.merge(CCHierarchyData, how='inner',on='EMPLOYEEID')
            
            Productivity['EMPLOYEEID'] = Productivity['EMPLOYEEID'].apply(int)
            CcFinalData = CcFinalData.merge(Productivity,on='EMPLOYEEID',how='left')
            CcFinalData.fillna(0,inplace=True)
            
            DSProdData['START_DATE'] = pd.to_datetime(DSProdData['START_DATE'])
            DSProdData['END_DATE'] = pd.to_datetime(DSProdData['END_DATE'])
            DSProdData = DSProdData[(DSProdData['START_DATE'] >= start_date) & (DSProdData['END_DATE'] <= end_date)]
            DSProdData.rename(columns={'PRODUCTIVITY':'DSProd'}, inplace=True)
            DSProdData = DSProdData[['EMPLOYEEID','DSProd']]
            DSProdData['EMPLOYEEID'] = DSProdData['EMPLOYEEID'].apply(int)

            

            CcFinalData = CcFinalData.merge(DSProdData, on='EMPLOYEEID', how='left')

            CcFinalData = CcFinalData[['EMPLOYEEID', 'Employee_Name', 'Lead', 'ADO', 'DO','DSProd','GPProd', 'Old_RVU_Score', 'Calculated_RVU_Score', 'Total',
            'Pending', 'Paid', 'Previously_Paid', 'Total_Rejections','Total_Denials', 'Correct_Payments', 
                'Incorrect_Payments']]
            
            include_round = ['Old_RVU_Score', 'Calculated_RVU_Score', 'Total',
            'Pending', 'Paid', 'Previously_Paid', 'Total_Rejections','Total_Denials', 'Correct_Payments', 'Incorrect_Payments']
            
            CcFinalData[include_round] = CcFinalData[include_round].applymap(self.format_with_commas)

            CcFinalData.drop_duplicates(subset=['EMPLOYEEID'], keep='first', inplace=True)
            CcFinalData.fillna(0,inplace=True)

            CcFinalData['Old_RVU_Score'] = CcFinalData['Old_RVU_Score'].str.replace(',', '').astype(int)

            # print("Length before route..",len(CcFinalData))

            if CcDirector == 'All':
                CcFinalData = CcFinalData
            else:
                CcFinalData = CcFinalData[CcFinalData['DO']==CcDirector].reset_index(drop=True)
            
            if Performance == '1':
                CcFinalData = CcFinalData
                # print("Length  if Performance == 1 before route..",len(CcFinalData))
            elif Performance == '2':
                CcFinalData = CcFinalData.loc[CcFinalData['Old_RVU_Score']>=1000].reset_index(drop=True)
                print(len(CcFinalData))
                # print("Length  if Performance == 2 before route..",len(CcFinalData))
            else:
                CcFinalData = CcFinalData.loc[CcFinalData['Old_RVU_Score']<=300].reset_index(drop=True)
                print(len(CcFinalData))
                # print("Length  if Performance == 3 before route..",len(CcFinalData))
            
            return CcFinalData
        
        except Exception as e:
             return {"Data":"No Data"}

  
        
