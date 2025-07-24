import pandas as pd
import pymssql
import warnings
from datetime import datetime,date, timedelta
from prod_app.HierarchyProdQuery import *
from prod_app.db_config import DbModulee

pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)
warnings.filterwarnings('ignore')


class GPProductiivty:
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

        
    def GpSignOffProd(self,ProductivtyWeek,Director,Performance):
        ProductivtyWeek = int(ProductivtyWeek)
        con,cur = self.db_obj.clnj_db()
        SignOff = GPSignOff()
        # print("SignOff", SignOff)
        signoff = pd.read_sql(SignOff,con)
        # print(signoff.columns)
        self.db_obj.db_close(con,cur)

        con,cur = self.db_obj.clnj_db()
        parameter = db_parameter()
        param = pd.read_sql(parameter,con)
        self.db_obj.db_close(con,cur)

        con,cur = self.db_obj.live_db()
        productivity_disc = ProductivityQuery()
        prod = pd.read_sql(productivity_disc,con)
        self.db_obj.db_close(con,cur)

        con,cur = self.db_obj.live_db()
        HierarchyDataFox = HierarchyQuery()
        HierarchyDataFinal = pd.read_sql(HierarchyDataFox,con)
        self.db_obj.db_close(con,cur)

        con,cur = self.db_obj.live_db()
        DSProd = DSProdQuery()
        DSProdData = pd.read_sql(DSProd,con)
        self.db_obj.db_close(con,cur)
        
        current_date = datetime.now()
        SignOffWeek = ProductivtyWeek
        

        
        if SignOffWeek:
            current_date = datetime.today().date()
            from_date = current_date - timedelta(days=(current_date.weekday() - 4) % 7 + 7 * (SignOffWeek + 1))
            to_date = from_date + timedelta(days=6)
        else:
            from_date = datetime.today().date()
            to_date = datetime.today().date()

        from_date = pd.to_datetime(from_date)
        to_date = pd.to_datetime(to_date)

        print("from_date", from_date, '     ', "to_date", to_date)


        
        # from_date = from_date.date()
        # to_date = to_date.date()
        # from_date = pd.to_datetime(from_date)
        # to_date = pd.to_datetime(to_date)
        # print("from_date",from_date, '     ',"to_date",to_date )
        
        GPsignoff = signoff[(signoff['SignOffDate'] >= from_date) & (signoff['SignOffDate'] <= to_date)].reset_index(drop=True)
        
        start_date = current_date - timedelta(weeks=ProductivtyWeek)
        start_date = start_date - timedelta(days=(start_date.weekday() + 1) % 7)
        start_date = pd.to_datetime(start_date)
        end_date = start_date + timedelta(days=6)
        end_date = pd.to_datetime(end_date)
        prod['Start_date'] = pd.to_datetime(prod['Start_date'])
        prod['End_date'] = pd.to_datetime(prod['End_date'])
        print("Start date and end date",start_date, '     ',end_date)
        prod = prod[(prod['Start_date'] >= start_date) & (prod['End_date'] <= end_date)].reset_index(drop=True)
        
        
    
    #     GPsignoff = GPsignoff[['ID', 'EMPLOYEEID', 'Practice', 'SignOffDate', 'DemoCreationCount', 'BillsCreationCount',
    #         'PaymentLineItemsCount', 'FollowUPCount', 'DenialManagementCount',
    #         'TicketsSalesforceCount', 'ErrorRejectionsCount', 'AppealsCount','OtherTasksCount', 'IndexingTeamFoxCount',
    #    'ReferralEntryTeamFoxCount', 'UrgentReferralEntryTeamFoxCount',
    #    'OPAUDTeamFOXCount', 'IVTeamFoxCount', 'AuthorizationTeamFOXCount',
    #    'POCTeamFoxCount', 'OPPHYTeamFoxCount', 'BillingCorrectionFoxCount',
    #    'FTicksFoxCount', 'RefundFoxCount']]
        
        GPsignoff = GPsignoff[['ID', 'EMPLOYEEID', 'Practice', 'SignOffDate', 'DemoCreationCount', 'BillsCreationCount',
            'PaymentLineItemsCount', 'FollowUPCount', 'DenialManagementCount',
            'TicketsSalesforceCount', 'ErrorRejectionsCount', 'AppealsCount','OtherTasksCount', 'Indexing_Team',
            'Referral_Entry_Team', 'Urgent_Referral_Team','OPAUD_Team', 'IV_Team',
            'Authorization_Team','POC_Team', 'OPPHY_Team', 'Billing_correction',
            'F_Ticks', 'Refund']]
        
    #     GPsignoff = GPsignoff.rename(columns={
    #     'IndexingTeamFoxCount': 'Indexing_Team',
    #     'ReferralEntryTeamFoxCount': 'Referral_Entry_Team',
    #     'UrgentReferralEntryTeamFoxCount': 'Urgent_Referral_Team',
    #     'OPAUDTeamFOXCount': 'OPAUD_Team',
    #     'IVTeamFoxCount': 'IV_Team',
    #     'AuthorizationTeamFOXCount': 'Authorization_Team',
    #     'POCTeamFoxCount': 'POC_Team',
    #     'OPPHYTeamFoxCount': 'OPPHY_Team',
    #     'BillingCorrectionFoxCount': 'Billing_correction',
    #     'FTicksFoxCount': 'F_Ticks',
    #     'RefundFoxCount': 'Refund'
    # })
        
        GPsignoff['SignOffDate'] = pd.to_datetime(GPsignoff['SignOffDate'])
        GPsignoff = GPsignoff.drop(columns={'ID','Practice'})
        
        # print(GPsignoff.columns)

        GPsignoff['D.Time(5)'] = GPsignoff['DemoCreationCount'] * (param.loc[param['Parameter'] == 'OS_DemoCreationCount', 'Time_Per_Sec'].values / 3600)
        GPsignoff['B.Time(5)'] = GPsignoff['BillsCreationCount'] * (param.loc[param['Parameter'] == 'OS_BillsCreationCount', 'Time_Per_Sec'].values / 3600)
        GPsignoff['P.Time(2)'] = GPsignoff['PaymentLineItemsCount'] * (param.loc[param['Parameter'] == 'OS_PaymentLineItemsCount', 'Time_Per_Sec'].values / 3600)
        GPsignoff['F.Time(5)'] = GPsignoff['FollowUPCount'] * (param.loc[param['Parameter'] == 'OS_FollowUPCount', 'Time_Per_Sec'].values / 3600)
        GPsignoff['D.Time(7)'] = GPsignoff['DenialManagementCount'] * (param.loc[param['Parameter'] == 'OS_DenialManagementCount', 'Time_Per_Sec'].values / 3600)
        GPsignoff['T.Time(5)'] = GPsignoff['TicketsSalesforceCount'] * (param.loc[param['Parameter'] == 'OS_TicketsSalesforceCount', 'Time_Per_Sec'].values / 3600)
        GPsignoff['R.Time(3)'] = GPsignoff['ErrorRejectionsCount'] * (param.loc[param['Parameter'] == 'OS_ErrorRejectionsCount', 'Time_Per_Sec'].values / 3600)
        GPsignoff['A.Time(5)'] = GPsignoff['AppealsCount'] * (param.loc[param['Parameter'] == 'OS_AppealsCount', 'Time_Per_Sec'].values / 3600)
        GPsignoff['O.Time(5)'] = GPsignoff['OtherTasksCount'] * (param.loc[param['Parameter'] == 'OS_OtherTasksCount', 'Time_Per_Sec'].values / 3600)
        GPsignoff['R.Time(10)'] = GPsignoff['Referral_Entry_Team'] * (param.loc[param['Parameter'] == 'Referral_Entry_Team', 'Time_Per_Sec'].values / 3600)
        GPsignoff['U.Time(15)'] = GPsignoff['Urgent_Referral_Team'] * (param.loc[param['Parameter'] == 'Urgent_Referral_Team', 'Time_Per_Sec'].values / 3600)
        GPsignoff['O.Time(10)'] = GPsignoff['OPPHY_Team'] * (param.loc[param['Parameter'] == 'OPPHY_Team', 'Time_Per_Sec'].values / 3600)
        GPsignoff['O.Time(13)'] = GPsignoff['OPAUD_Team'] * (param.loc[param['Parameter'] == 'OPAUD_Team', 'Time_Per_Sec'].values / 3600)
        GPsignoff['I.Time(8)'] = GPsignoff['Indexing_Team'] * (param.loc[param['Parameter'] == 'Indexing_Team', 'Time_Per_Sec'].values / 3600)
        GPsignoff['A.Time(10)'] = GPsignoff['Authorization_Team'] * (param.loc[param['Parameter'] == 'Authorization_Team', 'Time_Per_Sec'].values / 3600)
        GPsignoff['I.Time(12)'] = GPsignoff['IV_Team'] * (param.loc[param['Parameter'] == 'IV_Team', 'Time_Per_Sec'].values / 3600)
        GPsignoff['P.Time(5)'] = GPsignoff['POC_Team'] * (param.loc[param['Parameter'] == 'POC_Team', 'Time_Per_Sec'].values / 3600)
        GPsignoff['B.Time(25)'] = GPsignoff['Billing_correction'] * (param.loc[param['Parameter'] == 'Billing_correction', 'Time_Per_Sec'].values / 3600)
        GPsignoff['F.Time(2)'] = GPsignoff['F_Ticks'] * (param.loc[param['Parameter'] == 'F_Ticks', 'Time_Per_Sec'].values / 3600)
        GPsignoff['R.Time(15)'] = GPsignoff['Refund'] * (param.loc[param['Parameter'] == 'Refund', 'Time_Per_Sec'].values / 3600)


        

        GPsignoff['EMPLOYEEID'] = GPsignoff['EMPLOYEEID'].apply(int)
        GPsignoff['WorkHoursWeek'] = round((GPsignoff.filter(like='Time').sum(axis=1)),1)
        GPsignoff['AdjustedSum'] = GPsignoff.apply(self.adjust_sum, axis=1, data=GPsignoff)
        
        

        numerical_cols=[ 'DemoCreationCount', 'BillsCreationCount',
       'PaymentLineItemsCount', 'FollowUPCount', 'DenialManagementCount',
       'TicketsSalesforceCount', 'ErrorRejectionsCount', 'AppealsCount',
       'OtherTasksCount', 'Indexing_Team', 'Referral_Entry_Team',
       'Urgent_Referral_Team', 'OPAUD_Team', 'IV_Team', 'Authorization_Team',
       'POC_Team', 'OPPHY_Team', 'Billing_correction', 'F_Ticks', 'Refund',
       'D.Time(5)', 'B.Time(5)', 'P.Time(2)', 'F.Time(5)', 'D.Time(7)',
       'T.Time(5)', 'R.Time(3)', 'A.Time(5)', 'O.Time(5)', 'R.Time(10)',
       'U.Time(15)', 'O.Time(10)', 'O.Time(13)', 'I.Time(8)', 'A.Time(10)',
       'I.Time(12)', 'P.Time(5)', 'B.Time(25)', 'F.Time(2)', 'R.Time(15)',
       'WorkHoursWeek','AdjustedSum']
        
        GPsignoff=GPsignoff.groupby('EMPLOYEEID')[numerical_cols].sum().reset_index()
        # print(GPsignoff[GPsignoff["EMPLOYEEID"]==16905])

        HierarchyDataFinal['EMPLOYEEID'] = HierarchyDataFinal['EMPLOYEEID'].apply(int)
        GPsignoff = GPsignoff.merge(HierarchyDataFinal, how='inner', on='EMPLOYEEID')
        GPsignoff.fillna(0, inplace=True)

        # print(GPsignoff[GPsignoff["EMPLOYEEID"]==16905].head())


        exclude_columns = ['SignOffDate','EMPLOYEEID','Employee_Name', 'Lead', 'ADO', 'DO', 'WorkHoursWeek']

        GPsignoff['ClaimsSum'] = GPsignoff.loc[:, ~GPsignoff.columns.isin(exclude_columns) & ~GPsignoff.columns.str.contains('Time')].sum(axis=1)
        prod= prod.rename(columns={'Employee_id':'EMPLOYEEID','ProductivityStatus':'GPProd','DisciplineStatus':'Discipline'})
        prod = prod[['EMPLOYEEID','GPProd']]
        prod['EMPLOYEEID'] = prod['EMPLOYEEID'].apply(int)
        Final_GP_Data = GPsignoff.merge(prod, how='left', on='EMPLOYEEID')
        
        Final_GP_Data.fillna(0,inplace=True)
        # print(Final_GP_Data.columns)
    

        DSProdData['START_DATE'] = pd.to_datetime(DSProdData['START_DATE'])
        DSProdData['END_DATE'] = pd.to_datetime(DSProdData['END_DATE'])
        DSProdData = DSProdData[(DSProdData['START_DATE'] >= start_date) & (DSProdData['END_DATE'] <= end_date)]
        DSProdData.rename(columns={'PRODUCTIVITY':'DSProd'}, inplace=True)
        DSProdData = DSProdData[['EMPLOYEEID','DSProd']]
        DSProdData['EMPLOYEEID'] = DSProdData['EMPLOYEEID'].apply(int)

        Final_GP_Data = Final_GP_Data.merge(DSProdData, on='EMPLOYEEID', how='left')
        Final_GP_Data.fillna(0,inplace=True)
        

        Final_GP_Data = Final_GP_Data.rename(columns={'EMPLOYEEID':'EmpID', 'Employee_Name':'EmpName','DemoCreationCount':'Demo','BillsCreationCount':'Bills', 	'PaymentLineItemsCount':'Payments','FollowUPCount':'FollowUP','DenialManagementCount':'Denial','TicketsSalesforceCount':'Tickets',
            'ErrorRejectionsCount':'Rejections','AppealsCount':'Appeals','OtherTasksCount':'OtherTask',
            'Referral_Entry_Team':'Referral','Urgent_Referral_Team':'UrgentReferral','OPPHY_Team':'OPPHY',
            'OPAUD_Team':'OPAUD','Indexing_Team':'Index','Authorization_Team':'Authorization',
            'POC_Team':'POC','Billing_correction':'BillCorrect'})

        
        Final_GP_Data = Final_GP_Data[['EmpID','EmpName','Lead', 'ADO', 'DO','DSProd','GPProd','WorkHoursWeek','ClaimsSum',
            'Bills','B.Time(5)','Payments','P.Time(2)','FollowUP','F.Time(5)','OtherTask','O.Time(5)',
            'Demo','D.Time(5)','Denial','D.Time(7)','Tickets','T.Time(5)','Rejections','R.Time(3)','Appeals','A.Time(5)',
            'Index','I.Time(8)','Referral','R.Time(10)','UrgentReferral','U.Time(15)',
            'OPPHY','O.Time(10)','OPAUD','O.Time(13)','Authorization','A.Time(10)',
            'POC','P.Time(5)', 'BillCorrect','B.Time(25)','AdjustedSum']]

        include_round = ['WorkHoursWeek','AdjustedSum','ClaimsSum',
            'Index','I.Time(8)','Demo','D.Time(5)',
            'OPPHY','O.Time(10)','OPAUD','O.Time(13)','Authorization','A.Time(10)',
            'Referral','R.Time(10)','Bills','B.Time(5)','Payments','P.Time(2)','OtherTask',
            'O.Time(5)','FollowUP','F.Time(5)','Denial','D.Time(7)','Tickets','T.Time(5)','Rejections','R.Time(3)','Appeals','A.Time(5)',
            'UrgentReferral','U.Time(15)','POC','P.Time(5)', 'BillCorrect','B.Time(25)']
        


        exclude_col = ['EmpID','EmpName', 'Lead', 'ADO', 'DO']

        

        Final_GP_Data = Final_GP_Data.sort_values(by=['AdjustedSum'], ascending=False).reset_index(drop=True)
        Final_GP_Data[include_round] = Final_GP_Data[include_round].applymap(self.format_with_commas)

        Final_GP_Data.drop_duplicates(subset=['EmpID'], keep='first', inplace=True)

        Final_GP_Data.fillna(0, inplace=True)
        
        # print(Final_GP_Data.head(1))

        # data_types = Final_GP_Data.dtypes
        # print(data_types)

        # For columns where values may have commas, we need to clean the data before conversion
        Final_GP_Data[['DSProd','GPProd']] = Final_GP_Data[['DSProd','GPProd']].apply(lambda x: pd.to_numeric(x.replace(',', ''), errors='coerce') if isinstance(x, str) else x)

        # For the 'WorkHoursWeek' column, we do the same to remove commas and then convert to integer
        Final_GP_Data['WorkHoursWeek'] = Final_GP_Data['WorkHoursWeek'].apply(lambda x: pd.to_numeric(str(x).replace(',', ''), errors='coerce') if isinstance(x, str) else x).astype(int)

        
        if Director == 'All':
            Final_GP_Data = Final_GP_Data
        else:
            Final_GP_Data = Final_GP_Data[Final_GP_Data['DO']==Director].reset_index(drop=True)

        if Performance == "1":
            Final_GP_Data = Final_GP_Data
            # print("Length  if Performance == 1 before route..",len(Final_GP_Data))
        elif Performance == "2":
            Final_GP_Data = Final_GP_Data.loc[Final_GP_Data['WorkHoursWeek']>=60].reset_index(drop=True)
            # print("Length  if Performance == 2 before route..",len(Final_GP_Data))
        else:
            Final_GP_Data = Final_GP_Data.loc[Final_GP_Data['WorkHoursWeek']<35].reset_index(drop=True)
            # print("Length  if Performance == 3 before route..",len(Final_GP_Data))

        print("Egp data..",Final_GP_Data.shape[0])
        return Final_GP_Data
        