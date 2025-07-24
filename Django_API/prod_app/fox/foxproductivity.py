import pandas as pd
import pymssql
import warnings
from datetime import datetime, timedelta
from prod_app.HierarchyProdQuery import *
from prod_app.db_config import DbModulee

pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)
warnings.filterwarnings('ignore')


class FoxProd:
    def __init__(self) -> None:
        self.db_obj = DbModulee()


    def format_with_commas(self, value):
        return "{:,.0f}".format(value)
    
    def has_saturday(self, employee_id, data):
        employee_data = data[data['EMPLOYEEID'] == employee_id]
        return any(employee_data['SignOffDate'].dt.weekday == 5)

    def adjust_sum(self, row, data):
        employee_id = row['EMPLOYEEID']
        if self.has_saturday(employee_id, data):
            return row['WorkHoursWeek'] / 6  
        else:
            return row['WorkHoursWeek'] / 5  

    def FoxSignOffProd(self,weeks_bef,FoxDirector,Performance):
        weeks_bef = int(weeks_bef)

        # import pdb
        # pdb.set_trace()

        con,cur = self.db_obj.clnj_db()
        Sign_Off = FoxSignOff()
        # print(Sign_Off.head())
        SignOff = pd.read_sql(Sign_Off,con)
        self.db_obj.db_close(con,cur)
        
        con,cur = self.db_obj.clnj_db()
        parameter = db_parameter()
        param = pd.read_sql(parameter,con)
        self.db_obj.db_close(con,cur)
        
        con,cur = self.db_obj.live_db()
        productivity_disc = ProductivityQuery()
        FoxProductivity = pd.read_sql(productivity_disc,con)
        self.db_obj.db_close(con,cur)
        
        con,cur = self.db_obj.live_db()
        HierarchyDataFox = HierarchyQuery()
        FoxHierarchyData = pd.read_sql(HierarchyDataFox,con)
        self.db_obj.db_close(con,cur)

        con,cur = self.db_obj.live_db()
        DSProd = DSProdQuery()
        DSProdData = pd.read_sql(DSProd,con)
        self.db_obj.db_close(con,cur)

        current_date = datetime.now()
        start_date = current_date - timedelta(weeks=weeks_bef)
        start_date = start_date - timedelta(days=(start_date.weekday() + 1) % 7)
        start_date = start_date.date()
        start_date = pd.to_datetime(start_date)
        end_date = start_date + timedelta(days=6)
        end_date = end_date.date()
        end_date = pd.to_datetime(end_date)
        print(start_date, end_date) 
        FoxProductivity['Start_date'] = pd.to_datetime(FoxProductivity['Start_date'])
        FoxProductivity['End_date'] = pd.to_datetime(FoxProductivity['End_date'])
        FoxProductivity = FoxProductivity[(FoxProductivity['Start_date'] >= start_date) & (FoxProductivity['End_date'] <= end_date)]
        
        SignOff['SignOffDate'] = pd.to_datetime(SignOff['SignOffDate'])
        SignOff = SignOff[(SignOff['SignOffDate'] >= start_date) & (SignOff['SignOffDate'] <= end_date)]
        
        
        
        SignOff = SignOff[['EMPLOYEEID','SignOffDate','DemoCreationCount',
        'BillsCreationCount','PaymentLineItemsCount',
        'FollowUPCount','DenialManagementCount',
        'TicketsSalesforceCount','ErrorRejectionsCount',
        'AppealsCount','OtherTasksCount','Referral_Entry_Team',
        'Urgent_Referral_Team','OPPHY_Team','OPAUD_Team',
        'Indexing_Team','Authorization_Team','IV_Team',
        'POC_Team','Billing_correction', 'F_Ticks',
        'Refund','O3COI_TEAM','INTERNAL_AUDIT',
        'SA_INVOICING']]

    
        
        SignOff['D.Time(5)'] = SignOff['DemoCreationCount'] * (param.loc[param['Parameter'] == 'OS_DemoCreationCount', 'Time_Per_Sec'].values / 3600)
        SignOff['B.Time(5)'] = SignOff['BillsCreationCount'] * (param.loc[param['Parameter'] == 'OS_BillsCreationCount', 'Time_Per_Sec'].values / 3600)
        SignOff['P.Time(2)'] = SignOff['PaymentLineItemsCount'] * (param.loc[param['Parameter'] == 'OS_PaymentLineItemsCount', 'Time_Per_Sec'].values / 3600)
        SignOff['F.Time(5)'] = SignOff['FollowUPCount'] * (param.loc[param['Parameter'] == 'OS_FollowUPCount', 'Time_Per_Sec'].values / 3600)
        SignOff['D.Time(7)'] = SignOff['DenialManagementCount'] * (param.loc[param['Parameter'] == 'OS_DenialManagementCount', 'Time_Per_Sec'].values / 3600)
        SignOff['T.Time(5)'] = SignOff['TicketsSalesforceCount'] * (param.loc[param['Parameter'] == 'OS_TicketsSalesforceCount', 'Time_Per_Sec'].values / 3600)
        SignOff['E.Time(3)'] = SignOff['ErrorRejectionsCount'] * (param.loc[param['Parameter'] == 'OS_ErrorRejectionsCount', 'Time_Per_Sec'].values / 3600)
        SignOff['A.Time(5)'] = SignOff['AppealsCount'] * (param.loc[param['Parameter'] == 'OS_AppealsCount', 'Time_Per_Sec'].values / 3600)
        SignOff['O.Time(5)'] = SignOff['OtherTasksCount'] * (param.loc[param['Parameter'] == 'OS_OtherTasksCount', 'Time_Per_Sec'].values / 3600)
        SignOff['R.Time(10)'] = SignOff['Referral_Entry_Team'] * (param.loc[param['Parameter'] == 'Referral_Entry_Team', 'Time_Per_Sec'].values / 3600)
        SignOff['U.Time(15)'] = SignOff['Urgent_Referral_Team'] * (param.loc[param['Parameter'] == 'Urgent_Referral_Team', 'Time_Per_Sec'].values / 3600)
        SignOff['O.Time(10)'] = SignOff['OPPHY_Team'] * (param.loc[param['Parameter'] == 'OPPHY_Team', 'Time_Per_Sec'].values / 3600)
        SignOff['O.Time(13)'] = SignOff['OPAUD_Team'] * (param.loc[param['Parameter'] == 'OPAUD_Team', 'Time_Per_Sec'].values / 3600)
        SignOff['I.Time(8)'] = SignOff['Indexing_Team'] * (param.loc[param['Parameter'] == 'Indexing_Team', 'Time_Per_Sec'].values / 3600)
        SignOff['A.Time(10)'] = SignOff['Authorization_Team'] * (param.loc[param['Parameter'] == 'Authorization_Team', 'Time_Per_Sec'].values / 3600)
        SignOff['I.Time(12)'] = SignOff['IV_Team'] * (param.loc[param['Parameter'] == 'IV_Team', 'Time_Per_Sec'].values / 3600)
        SignOff['P.Time(5)'] = SignOff['POC_Team'] * (param.loc[param['Parameter'] == 'POC_Team', 'Time_Per_Sec'].values / 3600)
        SignOff['B.Time(25)'] = SignOff['Billing_correction'] * (param.loc[param['Parameter'] == 'Billing_correction', 'Time_Per_Sec'].values / 3600)
        SignOff['F.Time(2)'] = SignOff['F_Ticks'] * (param.loc[param['Parameter'] == 'F_Ticks', 'Time_Per_Sec'].values / 3600)
        SignOff['R.Time(15)'] = SignOff['Refund'] * (param.loc[param['Parameter'] == 'Refund', 'Time_Per_Sec'].values / 3600)
        SignOff['O.Time(25)'] = SignOff['O3COI_TEAM'] * (param.loc[param['Parameter'] == 'O3COI', 'Time_Per_Sec'].values / 3600)
        SignOff['IA.Time(5)'] = SignOff['INTERNAL_AUDIT'] * (param.loc[param['Parameter'] == 'Internal_Audit', 'Time_Per_Sec'].values / 3600)
        SignOff['I.Time(30)'] = SignOff['SA_INVOICING'] * (param.loc[param['Parameter'] == 'SA_Invoicing', 'Time_Per_Sec'].values / 3600)

        SignOff['EMPLOYEEID'] = SignOff['EMPLOYEEID'].apply(int)
        SignOff['WorkHoursWeek'] = round((SignOff.filter(like='Time').sum(axis=1)),1)
        SignOff['AdjustedSum'] = SignOff.apply(self.adjust_sum, axis=1, data=SignOff)
        # print(SignOff.columns)
        numerical_cols=['DemoCreationCount', 'BillsCreationCount',
       'PaymentLineItemsCount', 'FollowUPCount', 'DenialManagementCount',
       'TicketsSalesforceCount', 'ErrorRejectionsCount', 'AppealsCount',
       'OtherTasksCount', 'Referral_Entry_Team', 'Urgent_Referral_Team',
       'OPPHY_Team', 'OPAUD_Team', 'Indexing_Team', 'Authorization_Team',
       'IV_Team', 'POC_Team', 'Billing_correction', 'F_Ticks', 'Refund',
       'O3COI_TEAM', 'INTERNAL_AUDIT', 'SA_INVOICING', 'D.Time(5)',
       'B.Time(5)', 'P.Time(2)', 'F.Time(5)', 'D.Time(7)', 'T.Time(5)',
       'E.Time(3)', 'A.Time(5)', 'O.Time(5)', 'R.Time(10)', 'U.Time(15)',
       'O.Time(10)', 'O.Time(13)', 'I.Time(8)', 'A.Time(10)', 'I.Time(12)',
       'P.Time(5)', 'B.Time(25)', 'F.Time(2)', 'R.Time(15)', 'O.Time(25)',
       'IA.Time(5)', 'I.Time(30)','WorkHoursWeek', 'AdjustedSum']

        SignOff = SignOff.groupby('EMPLOYEEID')[numerical_cols].sum().reset_index()
        FoxHierarchyData['EMPLOYEEID'] = FoxHierarchyData['EMPLOYEEID'].apply(int)
        
        SignOff = SignOff.merge(FoxHierarchyData, how='inner', on='EMPLOYEEID')
        SignOff.fillna(0,inplace=True)
        
        
        # SignOff = SignOff[['EMPLOYEEID','Employee_Name', 'Lead', 'ADO', 'DO','DemoCreationCount','D.Time(5)',
        # 'BillsCreationCount','B.Time(5)','PaymentLineItemsCount','P.Time(2)',
        # 'FollowUPCount','F.Time(5)','DenialManagementCount','D.Time(7)',
        # 'TicketsSalesforceCount','T.Time(5)','ErrorRejectionsCount','E.Time(3)',
        # 'AppealsCount','A.Time(5)','OtherTasksCount','O.Time(5)','Referral_Entry_Team','R.Time(10)',
        # 'Urgent_Referral_Team','U.Time(15)','OPPHY_Team','O.Time(10)','OPAUD_Team','O.Time(13)',
        # 'Indexing_Team','I.Time(8)','Authorization_Team','A.Time(10)','IV_Team','I.Time(12)',
        # 'POC_Team','P.Time(5)', 'Billing_correction','B.Time(25)', 'F_Ticks','F.Time(2)',
        # 'Refund','R.Time(15)','O3COI_TEAM','O.Time(25)', 'INTERNAL_AUDIT','I.Time(5)',
        # 'SA_INVOICING','I.Time(30)']]

        

        exclude_columns = ['EMPLOYEEID','Employee_Name', 'Lead', 'ADO', 'DO','WorkHoursWeek']
        SignOff['ClaimsSum'] = SignOff.loc[:, ~SignOff.columns.isin(exclude_columns) & ~SignOff.columns.str.contains('Time')].sum(axis=1)


        FoxProductivity= FoxProductivity.rename(columns={'Employee_id':'EMPLOYEEID','ProductivityStatus':'GPProd','DisciplineStatus':'Discipline'})
        FoxProductivity = FoxProductivity[['EMPLOYEEID','GPProd']]
        FoxProductivity['EMPLOYEEID'] = FoxProductivity['EMPLOYEEID'].apply(int)

        Final_Data = SignOff.merge(FoxProductivity, how='left', on='EMPLOYEEID')
        Final_Data.fillna(0,inplace=True)
        Final_Data = Final_Data.sort_values(by=['AdjustedSum'], ascending=False).reset_index(drop=True)
        # Final_Data.round(exclude = exclude_columns,1, inplace=True)
        Final_Data = Final_Data.round(1)
        Final_Data[exclude_columns] = Final_Data[exclude_columns].astype('object')


        DSProdData['START_DATE'] = pd.to_datetime(DSProdData['START_DATE'])
        DSProdData['END_DATE'] = pd.to_datetime(DSProdData['END_DATE'])
        DSProdData = DSProdData[(DSProdData['START_DATE'] >= start_date) & (DSProdData['END_DATE'] <= end_date)]
        DSProdData.rename(columns={'PRODUCTIVITY':'DSProd'}, inplace=True)
        DSProdData = DSProdData[['EMPLOYEEID','DSProd']]
        DSProdData['EMPLOYEEID'] = DSProdData['EMPLOYEEID'].apply(int)

        Final_Data = Final_Data.merge(DSProdData, on='EMPLOYEEID',how='left')
        # Final_Data.fillna(0,inplace=True)

        Final_Data = Final_Data.rename(columns={'EMPLOYEEID':'EmpID', 'Employee_Name':'EmpName','DemoCreationCount':'Demo','BillsCreationCount':'Bills', 'PaymentLineItemsCount':'Payments','FollowUPCount':'FollowUP','DenialManagementCount':'Denial','TicketsSalesforceCount':'Tickets','ErrorRejectionsCount':'Rejections', 
        'AppealsCount':'Appeals','OtherTasksCount':'OtherTask','Referral_Entry_Team':'Referral','Urgent_Referral_Team':'UrgentReferral','OPPHY_Team':'OPPHY','OPAUD_Team':'OPAUD',
        'Indexing_Team':'Index','Authorization_Team':'Authorization','POC_Team':'POC', 'Billing_correction':'BillCorrect','O3COI_TEAM':'O3COI','INTERNAL_AUDIT':'Audit', 
        'SA_INVOICING':'Invoice'})

        Final_Data = Final_Data[['EmpID','EmpName','Lead', 'ADO', 'DO','DSProd','GPProd','WorkHoursWeek','AdjustedSum','ClaimsSum',
        'Index','I.Time(8)','Demo','D.Time(5)',
        'Invoice','I.Time(30)','IV_Team','I.Time(12)','OPPHY','O.Time(10)','OPAUD','O.Time(13)','Authorization','A.Time(10)',
        'Referral','R.Time(10)','O3COI','O.Time(25)', 'Audit','IA.Time(5)','Bills','B.Time(5)','Payments','P.Time(2)','OtherTask',
        'O.Time(5)','FollowUP','F.Time(5)','Denial','D.Time(7)','Tickets','T.Time(5)','Rejections','E.Time(3)','Appeals','A.Time(5)',
        'UrgentReferral','U.Time(15)','POC','P.Time(5)', 'BillCorrect','B.Time(25)', 'F_Ticks','F.Time(2)','Refund','R.Time(15)']]

        include_round = ['WorkHoursWeek','AdjustedSum','ClaimsSum',
        'Index','I.Time(8)','Demo','D.Time(5)',
        'Invoice','I.Time(30)','IV_Team','I.Time(12)','OPPHY','O.Time(10)','OPAUD','O.Time(13)','Authorization','A.Time(10)',
        'Referral','R.Time(10)','O3COI','O.Time(25)', 'Audit','IA.Time(5)','Bills','B.Time(5)','Payments','P.Time(2)','OtherTask',
        'O.Time(5)','FollowUP','F.Time(5)','Denial','D.Time(7)','Tickets','T.Time(5)','Rejections','E.Time(3)','Appeals','A.Time(5)',
        'UrgentReferral','U.Time(15)','POC','P.Time(5)', 'BillCorrect','B.Time(25)', 'F_Ticks','F.Time(2)','Refund','R.Time(15)']

        Final_Data[include_round] = Final_Data[include_round].applymap(self.format_with_commas)

        Final_Data.drop_duplicates(subset=['EmpID'], keep='first', inplace=True)

        Final_Data['WorkHoursWeek'] = Final_Data['WorkHoursWeek'].apply(int)

        print("FOX DATA", Final_Data.shape[0])

        if FoxDirector == 'All':
            Final_Data = Final_Data
        else:
            Final_Data = Final_Data[Final_Data['DO']==FoxDirector].reset_index(drop=True)

        if Performance == '1':
            Final_Data = Final_Data
            # print("Length  if Performance == 1 before route..",len(Final_Data))
        elif Performance == '2':
            Final_Data = Final_Data.loc[Final_Data['WorkHoursWeek']>=60].reset_index(drop=True)
            # print("Length  if Performance == 2 before route..",len(Final_Data))
        else:
            Final_Data = Final_Data.loc[Final_Data['WorkHoursWeek']<35].reset_index(drop=True)
            # print("Length  if Performance == 3 before route..",len(Final_Data))
        Final_Data=Final_Data.fillna(0)
        # print(Final_Data.head(2))
        return Final_Data
    
        