# -*- coding: utf-8 -*-
"""
Created on Thu May 11 18:31:01 2023

Last Modified May 25 20:20:02 2023

@author: sanju

"""

import psycopg2
import pandas as pd
# from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor
import multiprocessing
from multiprocessing import Value,Queue,Array
import tkinter as tk
# import socket
import threading
import time
from tkinter import ttk
# from sqlalchemy import create_engine
# import sys
# import os
# import openpyxl 
# from openpyxl import load_workbook
# # from JakePorter_v2 import main 
class App():
    
    def auto_scroll():
        console.see(tk.END)
    
    def Fetch(A,ISA1,queue):
        __name__='__main__'
        print ('multiprocess __name__ is ',__name__)
        ISA=ISA1+','
        start=time.monotonic()
        ISA=tuple(ISA.split(','))
        
        DB_Name='scheduling'
        Host_Name='sc****************redshift.amazonaws.com'
        Port_no=0000
        User_Name='Your username'
        Pass='Your Password'

        
        con = psycopg2.connect(dbname=DB_Name, host=Host_Name, port=Port_no, user=User_Name, password=Pass)
        print('status 1 : ', con.status,'\n',con)
        # con.close()
        
        query='''select appointment_record_version_number as Ver,external_ids as isa, fc,scac,status,reason,defect_type,caused_by from ipex.appointment_defects where external_ids in {}'''.format(ISA)
        # query='''select external_ids as isa, fc,scac,status,reason from ipex.appointment_defects where external_ids in ('10001770982')'''
        
        df = pd.read_sql(query, con)
        
        print('status 3 : ', con.status)
        # print(df)
        print(con)
        
        df.to_excel('TempDisputeData.xlsx',index=False,)
        
        end=time.monotonic()
        print(df)
        print('time taken with multiprocess :',end-start, ' sec')
        # df.columns=['ISA','FC','SCAC','STATUS','REASON']
        # df=df.loc[:,['ISA','FC','SCAC','STATUS','REASON']]
        # data=[df.columns.tolist()] + df.values.tolist()
        while True:
            if con.status==2:
                A.value=100
                queue.put(df)
                con.close()
                print('Multiprocessing 100% complete')
                break
           
        print('Ready for next entry')
            
    def update1(A,status,queue):
        l=0
        while True:
            root.update()
            App.auto_scroll()
            print(status)
            while A.value%10==0 and A.value<90:    
                A.value+=1
                # pl=str(A.value)
                print('l in first while : ',l ,'and A :',A.value)
                # F1ProgressLabel.config(text=(LabelFetch[l]+' :'+ pl +'%'))
                console.insert(tk.END,LabelFetch[l] )
                l+=1
                
            
            if A.value==100:
                print('entered A==100 to update treeview')
                # print(status)
                df=pd.read_excel('TempDisputeData.xlsx')
                print('read temp data')
                df.columns=['VER','ISA','FC','SCAC','STATUS','REASON','DEFECT_TYPE','CAUSED_BY']
                print('df.coloumn read')
                df=df.loc[:,['VER','ISA','FC','SCAC','STATUS','REASON','DEFECT_TYPE','CAUSED_BY']]
                print('read df.loc')
                data=[df.columns.tolist()] + df.values.tolist()
                print ('data from update 1 /n',data)
                
                for col_name in data[0]:
                    print('heading gets printeda ')
                    FetchedDATA.heading(col_name, text=col_name,anchor='w')
                    FetchedDATA.delete(*FetchedDATA.get_children())
                print('out of heading ')
                for values in data[1:]:
                    print('printing row')
                    FetchedDATA.insert('', tk.END, values=values)
            
                    
                submit.config(state='normal',text='Search')
                root.update()
                print('Button,Normal')
                A.value=90
                print('entered A==90 position')
                for i in range (10):
                    A.value+=1
                    time.sleep(0.002)
                    # print(A.value,'%')
                    pl=str(A.value)
                    F1ProgressLabel.config(text=('Fetch Completed : '+ pl +'%'))
                    F1Progress.config(value=A.value)
                    root.update()
                    App.auto_scroll()
                A.value=0
                RES=queue.get()
                console.insert(tk.END,'\n')
                console.insert(tk.END,'\n')
                console.insert(tk.END,RES)
                App.auto_scroll()
                root.update()
                break
            
            elif A.value<=90:  
                time.sleep(0.001)
                A.value+=1
                # print(status)
                # print('progress in percent : ' ,A.value,'%')
                    
            pl=str(A.value)
            F1ProgressLabel.config(text=(LabelFetch1[l]+' :'+ pl +'%'))
            # F1ProgressLabel.config(text=('completed : '+ pl +'%'))
            F1Progress.config(value=A.value)
             
    def CopyFetchData(event):
        select_item=FetchedDATA.focus()
        select_col=FetchedDATA.identify_column(event.x)  
        if select_item and select_col:
            cell_text=FetchedDATA.set(select_item,select_col)
            root.clipboard_clear()
            root.clipboard_append(cell_text)             
            
    def DataToUpload():
        try:
            Insert.config(state='disabled')
            
            Ver=int(Version.get())
            ISA=int(ISAInsert.get())
            Reason=str(REASON.get())
            Defect_Type=str(DEFECTTYPE.get())
            Caused_By=str(CAUSEDBY.get())
            Disposition=str(DISPOSITION.get())
            Comment=str(Comments.get())
            validation= 'validated' if a.get() else 'Not validated' 
    
            row=[(Ver,ISA,Reason,Defect_Type,Caused_By,Disposition,Comment,validation),]
            
            DataNew=pd.DataFrame(row,columns=['Version','ISA','Reason','Defect_Type','Caused_By','Disposition','Comments','VALIDATION'])
            
            try:
                DataOld= pd.read_excel('tempdata.xlsx', sheet_name='data')
            except:
                DataOld=pd.DataFrame()
                
            insertdata=pd.concat([DataOld,DataNew],ignore_index=True)
            insertdata.to_excel('tempdata.xlsx',sheet_name='data',index=False)
            
            #+++++++++++++++++++++++++++++++++++++++++++++++++
            # Tree View Update ###############################
            #+++++++++++++++++++++++++++++++++++++++++++++++++
            sheet= pd.read_excel('tempdata.xlsx', sheet_name='data')
            
            sheet.columns=['VER','ISA','REASON','DEFECT_TYPE','CAUSED_BY','DISPOSITION','COMMENTS','VALIDATION']
            
            data=[sheet.columns.tolist()] + sheet.values.tolist()
            
            InsertDATA.delete(*InsertDATA.get_children())
            
            print(sheet)
            # data = list(sheet.values)
            
            for value in data[0]:
                InsertDATA.heading(value, text=value,anchor='w')
            for value in data[1:]:
                InsertDATA.insert('', tk.END, values=value)
                
            
            console.insert(tk.END,'\n'+ 'Data Injected sucessully')
            App.auto_scroll()
            Insert.config(state='normal')
            root.update()
        except Exception as e:
            console.insert(tk.END,'\n'+ 'Error while Inserting Data'+'\n')
            console.insert(tk.END,e)
            App.auto_scroll()
            Insert.config(state='normal')
            root.update()
                         
    
    def Uploading(A,queue,Error):
        
        # data_type={'ISA':int, 'SCAC':str,'CARRIER':str,'FC_NAME':str,'DEFECT_REASON':str,'SHIPPER':str,'VALIDATION':str}
        sheet= pd.read_excel('tempdata.xlsx', sheet_name='data') #dtype=data_type
        print (sheet)
        print('entered uploading loop multiprocessing.')
        print('Uploading Getting Started:')
        
        DB_Name='scheduling'
        Host_Name='s**********************.redshift.amazonaws.com'
        Port_no=0000
        User_Name='Your username'
        Pass='Your Password'

        
        con = psycopg2.connect(dbname=DB_Name, host=Host_Name, port=Port_no, user=User_Name, password=Pass)
        cur=con.cursor()
        print(con)
        
        try:
            row = sheet.iloc[0]
        
            for index,row in sheet.iterrows():
                sql="INSERT INTO test_defect_dispute_override (VERSION,ISA,REASON,DEFECT_TYPE,CAUSED_BY,DISPOSITION,COMMENTS,VALIDATION) VALUES ( %s,%s,%s,%s,%s,%s,%s,%s)"
                values=(row['Version'],row['ISA'],row['Reason'],row['Defect_Type'],row['Caused_By'],row['Disposition'],row['Comments'],row['VALIDATION'])
                cur.execute(sql,values)
            A.value=100
            print('A value updated to 100')
            con.commit()
            cur.close()
            con.close()
            print('Uploading Done !')
        except Exception as e:
            print('error uploading data !',e)
            # queue.put(e)
            # Error[0]=e
            con.close()
            A.value=101
                        
        
        print('Uploading Done !')
     

        
        
        
                
    def Upload(A,queue,Error):
        
        Upload.config(state='disabled')
        Insert.config(state='disabled')
        root.update()
        p=multiprocessing.Process(target=App.Uploading,args=[A,queue,Error])
        proceed(p)
        # p.start()
        
        
        l=0   
        while True:
            root.update()
            App.auto_scroll()
            
            
            while A.value%10==0 and A.value<91:    
                A.value+=1
                pl=str(A.value)
                print('l in first while : ',l ,'and A :',A.value)
                F3ProgressLabel.config(text=(Label[l]+' :'+ pl +'%'))
                console.insert(tk.END,'\n'+Label[l] )
                App.auto_scroll()
                l+=1
            F3ProgressLabel.config(text=(Label[l]+' :'+ str(A.value) +'%'))
            F3Progress.config(value=A.value)
            
            if A.value==100 :
                A.value=90
                
                for i in range (2):
                    A.value+=1
                    time.sleep(0.002)
                    # print(A.value,'%')
                    pl=str(A.value)
                    F3ProgressLabel.config(text=('clearing data view panel : '+ pl +'%'))
                    console.insert(tk.END,'\n'+ 'Clearing data view panel')
                    F3Progress.config(value=A.value)
                    App.auto_scroll()
                    root.update()
                
                print('entered if A=100 Loop')
                Clear=pd.DataFrame(columns=['Version','ISA','Reason','Defect_Type','Caused_By','Disposition','Comments','VALIDATION'])
                Clear.to_excel('tempdata.xlsx',sheet_name='data',index=False)
                
                A.value+=1
                time.sleep(0.002)
                # print(A.value,'%')
                pl=str(A.value)
                F3ProgressLabel.config(text=('loading empty data frame : '+ pl +'%'))
                console.insert(tk.END,'\n'+ 'Loading empty data frame')
                App.auto_scroll()
                F3Progress.config(value=A.value)
                root.update()
                
                InsertDATA.delete(*InsertDATA.get_children())
                
                A.value+=1
                time.sleep(0.002)
                # print(A.value,'%')
                pl=str(A.value)
                F3ProgressLabel.config(text=('Data panel loading sucessful : '+ pl +'%'))
                console.insert(tk.END,'\n'+ 'Data panel loading sucessful')
                App.auto_scroll()
                F3Progress.config(value=A.value)
                root.update()
                
                sheet= pd.read_excel('tempdata.xlsx', sheet_name='data')
                
                sheet.columns=['VER','ISA','REASON','DEFECT_TYPE','CAUSED_BY','DISPOSITION','COMMENTS','VALIDATION']
                
                data=[sheet.columns.tolist()] + sheet.values.tolist()
                
                for value in data[0]:
                    InsertDATA.heading(value, text=value,anchor='w')
                for value in data[1:]:
                    InsertDATA.insert('', tk.END, values=value)
                A.value+=1
                time.sleep(0.002)
                # print(A.value,'%')
                pl=str(A.value)
                F3ProgressLabel.config(text=('Header is loading : '+ pl +'%'))
                console.insert(tk.END,'\n'+ 'Tabel Header Loaded sucessfully')
                App.auto_scroll()
                F3Progress.config(value=A.value)
                root.update()
                
                for i in range (5):
                    A.value+=1
                    time.sleep(0.002)
                    # print(A.value,'%')
                    pl=str(A.value)
                    F3ProgressLabel.config(text=('thanks for being patient : '+ pl +'%'))
                    console.insert(tk.END,'\n'+ 'Ready for next Upload')
                    F3Progress.config(value=A.value)
                    root.update()
                    
                
                
                F3ProgressLabel.config(text=('data upload succesfully completed : '+ pl +'%'))  
                F3Progress.config(value=A.value)
                print('update upload to normal')
                Upload.config(state='normal')
                print('update insert to normal')
                Insert.config(state='normal')
                root.update()
                print('Button,Normal')
                A.value=0
                break
            
            elif A.value<90 :  
                time.sleep(0.001)
                A.value+=1
            
                
            elif A.value==101 :  
                pl=str(A.value)
                F3ProgressLabel.config(text=('Error '+ pl +': Invalid entry'))
                F3Progress.config(value=A.value-1)
                Upload.config(state='normal')
                Insert.config(state='normal')
                console.insert(tk.END,'\n \n Error Code : \n')
                console.insert(tk.END,"invalid input syntax for type numeric: 'Version' or 'ISA'")
                
                App.auto_scroll()
                root.update()
                A.value=0
                
                break
            
        
    def search(A,queue):
        ISA1=str(ISA.get())
        A.value=0
        # print(A.value,' : from search')
        submit.config(text='Fetching',state='disabled')
        root.update()
        print(__name__)
        
        
        p=multiprocessing.Process(target=App.Fetch,args=[A,ISA1,queue])
        proceed(p)
        # p.start()
        pstatus=p.is_alive()
        
        T1=threading.Thread(target=App.update1(A,pstatus,queue))
        
        T1.start()

        # root.after(10,self.ProgressWork)
        # root.after(10,self.auto_scroll)
        
        print(A.value)
        
    def updatetree():
        try:
            # data_type={'VER':int,'ISA':int,'REASON':str,'DEFECT_TYPE':str,'CAUSED_BY':str,'DISPOSITION':str,'COMMENTS':str,'VALIDATION':str}
            
            sheet= pd.read_excel('tempdata.xlsx', sheet_name='data')
            
            
            sheet.columns=['VER','ISA','REASON','DEFECT_TYPE','CAUSED_BY','DISPOSITION','COMMENTS','VALIDATION']
            
            data=[sheet.columns.tolist()] + sheet.values.tolist()
            
            InsertDATA.delete(*InsertDATA.get_children())
            # time.sleep(5)
            print(sheet)
            # data = list(sheet.values)
            
            for value in data[0]:
                InsertDATA.heading(value, text=value,anchor='w')
            for value in data[1:]:
                InsertDATA.insert('', tk.END, values=value)
            root.update()
        except:
            print('sheet not found')
            
            
    def Delete():
        selected_row=InsertDATA.selection()
        print(selected_row)
        # time.sleep(5)
        for item in selected_row:
            value=InsertDATA.item(item,"values")
            print(value)
            selected_id=value[1]
            console.insert(tk.END,'\n \n Deleted Row with incoorect data :')
            
            try:
                consoledata=int(selected_id)
            except:
                consoledata=str(selected_id)
                
            console.insert(tk.END,consoledata)
            
            print('selected id is :',selected_id)
            
            InsertDATA.delete(item)
            
            df=pd.read_excel('tempdata.xlsx')
            print(df)
            try:
                index=df.index[df['ISA'] == int(selected_id)]
            except:
                index=df.index[df['ISA'] == str(selected_id)]
            # index.tolist()
            print (index)
            df=df.drop(index)
            df.to_excel('tempdata.xlsx',sheet_name='data',index=False)
            print('Data deleted')
            
            
            # root.update()
            App.auto_scroll()
            App.updatetree()
            root.update()

    def Update_Next_Menu_List(*args):
        Selected_Defect_Type= DEFECTTYPE.get()
        REASON['values']=[]
        CAUSEDBY['values']=[]
        DISPOSITION['values']=[]
        
        if Selected_Defect_Type == "NCNS":
            REASON['values']=["Reason_Code","Onboarding Error","Carrier did not arrive per sked ISA","Site Appointment Management Error"]
            CAUSEDBY['values']=["Caused_By","AMAZON","CARRIER"]
            DISPOSITION['values']=["Disposition","Non Defective","NCNS"]
            
        elif Selected_Defect_Type == "RESCHEDULE":
            REASON['values']=["Reason_Code","CARRIER RESCHEDULE","AMAZON CAUSED DEFECT","ONBOARDING ERROR"]
            DISPOSITION['values']=["Disposition","RESCHEDULE","NON DEFECTIVE"]
            CAUSEDBY['values']=["Caused_By","AMAZON","CARRIER"]
            
        elif Selected_Defect_Type == "CANCELLATION":
            REASON['values']=["Reason_Code","CARRIER LATE CANCELLATION"]
            DISPOSITION['values']=["Disposition","CANCELLATION"]
            CAUSEDBY['values']=["Caused_By","CARRIER"]
            
        elif Selected_Defect_Type == "DUPLICATE":
            REASON['values']=["Reason_Code","PO's RECEIVED IN FULL","CARRIER CREATED MULTIPLE ISA's"]
            DISPOSITION['values']=["Disposition","DUPLICATE"]
            CAUSEDBY['values']=["Caused_By","CARRIER"]
            
        elif Selected_Defect_Type == "SAMPLE FREIGHT FAILED":
            REASON['values']=["Reason_Code","NON DEFECTIVE TO CARRIER"]
            DISPOSITION['values']=["Disposition","NON DEFECTIVE"]
            CAUSEDBY['values']=["Caused_By","AMAZON"]
        
        elif Selected_Defect_Type == "REFUSAL":
            REASON['values']=["Reason_Code","VALID SITE REFUSAL"]
            DISPOSITION['values']=["Disposition","REFUSAL"]
            CAUSEDBY['values']=["Caused_By","CARRIER","AMAZON"]
        
        elif Selected_Defect_Type == "REFUSAL DUE TO CAPACITY":
            REASON['values']=["Reason_Code","SITE APPOINTMENT MANAGEMENT ERROR"]
            DISPOSITION['values']=["Disposition","NON DEFECTIVE"]
            CAUSEDBY['values']=["Caused_By","AMAZON"]
            
    # def toggle_mode():
    #     if mode.instate(["selected"]):
    #         style.theme_use("forest-light")
    #         console.configure(background="white")
            
    #         style.configure("Treeview.Heading", padding=(4,0),font=("TkDefaultFont",10,"bold"))
    #     else:
    #         style.theme_use("forest-dark")
    #         console.configure(background="#313131")
            
    #         style.configure("Treeview.Heading", padding=(4,0),font=("TkDefaultFont",10,"bold"))
            
            
if __name__ == "__main__":
    multiprocessing.freeze_support()
    def proceed(p1):
        p1.start()
    manager=multiprocessing.Manager()
    queue=manager.Queue()
    A=Value('i',0)
    Error=multiprocessing.Array('c',500)
    Label=['Connecting Database ','Connection Established ','Creating Data Base Engine ','Data Being Uploaded ','Data Insertion Successful ','Gathering Disputed Data ','Updating User Interface ','Uploading Started ','Uploading Successful ','After Upload Work in Progress ','Entering Final loop ']
    LabelFetch=['\nConnecting SQL DataBase/ Resdshift Cluster .','\nConnection established Sucessfully','\nData being Fetched.','.','.','\nCompiling Data','\nLoading Fetched Data.','.','.','.','.']
    LabelFetch1=['Connecting SQL DadataBase / Resdshift Cluster .','Connection established Sucessfully','Data being Fetched .','Data being Fetched. .','Data being Fetched. . .','Compiling Data','Loading Fetched Data .','Loading Fetched Data . .','Loading Fetched Data . . .','Loading Fetched Data . . . .','Loading Fetched Data . . . . .']
    # search(A,FC)
    root = tk.Tk()
    root.title("Defect Dispute Override Tool By sanju@")
    root.iconbitmap("Network.ico")
    
    # root.update()
    root.option_add("*tearOff", False) # This is always a good idea
    
    # Make the app responsive Effects W1/W2 row and col
    root.columnconfigure(index=0, weight=1)
    # root.columnconfigure(index=1, weight=1)
    root.rowconfigure(index=0, weight=5) 
    root.rowconfigure(index=1, weight=30)
    
    style = ttk.Style(root)
    
    # Import the tcl file
    # root.tk.call("source", "forest-light.tcl")
    root.tk.call("source", "forest-dark.tcl")
    
    
    # Set the theme with the theme_use method
    style.theme_use("forest-dark")
    style.configure("Treeview.Heading", padding=(4,0),font=("TkDefaultFont",10,"bold"))
       
    
    #*******************************************
    W1 = ttk.Frame(root, padding=0)
    W1.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
    
    #effects F1/F2 Row and Col
    W1.columnconfigure(index=0, weight=1)
    W1.columnconfigure(index=1, weight=10)
    W1.rowconfigure(index=0, weight=1)
    #-----------------------------------------#
    W2 = ttk.Frame(root, padding=0)
    W2.grid(row=1, column=0, padx=0, pady=(0), sticky="nsew")
    
    #effects F3/F4 Row and Col
    W2.columnconfigure(index=0, weight=1)
    W2.columnconfigure(index=1, weight=10)
    W2.rowconfigure(index=0, weight=1)
    #*******************************************
    
    # W3 = ttk.Frame(root, padding=(0, 0, 0, 10))
    # W3.grid(row=1, column=0, padx=10, pady=(30, 10), sticky="nsew")
    # W3.columnconfigure(index=0, weight=1)
    # W4 = ttk.Frame(root, padding=(0, 0, 0, 10))
    # W4.grid(row=1, column=1, padx=10, pady=(30, 10), sticky="nsew")
    # W4.columnconfigure(index=0, weight=1)
       
    F1= ttk.LabelFrame(W1, text=" Fetch Disputed ISA's ⬇ ",relief='sunken',width=500)
    F1.grid(row=0,column=0,sticky='nsew',padx=5,pady=5)
    F1.columnconfigure(index=0, weight=1)
    # F1.columnconfigure(index=1, weight=1)
    F1.columnconfigure(index=1, weight=1)
    F1.rowconfigure(index=0, weight=10)
    F1.rowconfigure(index=1, weight=20)
    
    ISALabel=ttk.Label(F1,text='For multiple ISA Separate each ISA with comma.',font=('Arial',9) )
    ISALabel.grid(row=0,column=0,padx=(10,0), pady=(10,2), sticky='ew')
    
    ISA=ttk.Entry(F1, width=58)
    ISA.insert(0,'ISA1, ISA2, ISA3 . . .')
    ISA.bind("<FocusIn>",lambda ie: ISA.delete('0','end'))
    ISA.grid(row=1,column=0,padx=(10,0), pady=5, sticky='ew')
    
    submit=ttk.Button(F1,text="Search", command=lambda:App.search(A,queue))
    submit.grid(row=1, column=1,padx=(5,18), pady=5, sticky='ew')
    
    
    
    F1ProgressLabel=ttk.Label(F1, text="current status",font=("Arial",8))
    F1ProgressLabel.grid(row=2, column=0,padx=10, pady=0,sticky='ew')
    
    F1Progress=ttk.Progressbar(F1,maximum=100,mode="determinate")
    F1Progress.grid(row=3, column=0,padx=10, pady=10, sticky='ew',columnspan=2)
    
    # entry = ttk.Entry(F1,)
    # entry.insert(0, "Entry")
    # entry.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="ew")
    
    F2= ttk.LabelFrame(W1, text=" Feteched Data ✔ ",relief='sunken')
    F2.grid(row=0,column=1,sticky='nsew',padx=5,pady=5)
    F2.columnconfigure(index=0, weight=1)
    
    
    FetchScroll=ttk.Scrollbar(F2)
    FetchScroll.pack(side="right", fill="y",pady=5,padx=(0,5))
    # FetchScroll.grid(row=0, column=1, sticky='ns',pady=(5,5))
    
    cols=('VER','ISA','FC','SCAC','STATUS','REASON','DEFECT_TYPE','CAUSED_BY')
    FetchedDATA=ttk.Treeview(F2, yscrollcommand=FetchScroll.set, show='headings', columns=cols, height=1)
    FetchedDATA.column('VER', width=20)
    FetchedDATA.column('ISA', width=90)
    FetchedDATA.column('FC', width=50)
    FetchedDATA.column('SCAC', width=50)
    FetchedDATA.column('STATUS', width=140)
    FetchedDATA.column('REASON', width=300)
    FetchedDATA.column('DEFECT_TYPE', width=100)
    FetchedDATA.column('CAUSED_BY', width=100)
    # self.FetchedDATA.column('SHIPPER_A/C', width=50)
    FetchScroll.config(command=FetchedDATA.yview)
    FetchedDATA.pack(expand=True, fill="both", padx=(5,0), pady=5)
    FetchedDATA.bind('<Button-3>',App.CopyFetchData)
    # FetchedDATA.grid(row=0, column=0,padx=(5,1), pady=5, sticky='nsew')
       
    
    F3= ttk.LabelFrame(W2, text=" Feed Dispute Data ✅ ",relief='sunken')
    F3.grid(row=0,column=0,sticky='nsew',padx=5,pady=5)
    F3.columnconfigure(index=0, weight=1)
    F3.rowconfigure(index=0, weight=4)
    F3.rowconfigure(index=1, weight=1)
    F3.rowconfigure(index=2, weight=1)
    F3.rowconfigure(index=3, weight=5)
    F3.rowconfigure(index=4, weight=1)
    F3.rowconfigure(index=5, weight=1)
    F3.rowconfigure(index=6, weight=1)
    F3.rowconfigure(index=7, weight=10)
    
    Dframe= ttk.Frame(F3, borderwidth=0  )
    Dframe.grid(row=0,column=0,padx=5,pady=5,sticky='nsew')
    Dframe.columnconfigure(index=0, weight=1)
    Dframe.columnconfigure(index=1, weight=1)
    Dframe.columnconfigure(index=2, weight=1)
    Dframe.rowconfigure(index=0, weight=1)
    Dframe.rowconfigure(index=1, weight=1)
    
    ############################################################################
    #   OPTIONS INPUTS
    ###########################################################################
    
    Version=ttk.Entry(Dframe)
    Version.insert(0,'Version')
    Version.bind("<FocusIn>",lambda ie: Version.delete('0','end'))
    Version.grid(row=0,column=0,padx=5, pady=5, sticky='ew')
    
    ISAInsert=ttk.Entry(Dframe)
    ISAInsert.insert(0,'ISA')
    ISAInsert.bind("<FocusIn>",lambda ie: ISAInsert.delete('0','end'))
    ISAInsert.grid(row=0,column=1,padx=5, pady=5, sticky='ew')
    
    DEFECTTYPE=ttk.Combobox(Dframe,state="readonly",values=["Defect Type","NCNS","RESCHEDULE","CANCELLATION","DUPLICATE","SAMPLE FREIGHT FAILED","REFUSAL","REFUSAL DUE TO CAPACITY"])
    DEFECTTYPE.current(0)
    DEFECTTYPE.grid(row=0,column=2,padx=5, pady=5, sticky='ew')
    DEFECTTYPE.bind("<<ComboboxSelected>>", App.Update_Next_Menu_List)
    
    REASON=ttk.Combobox(Dframe,state="readonly",values=["Reason Code"])
    REASON.current(0)
    REASON.grid(row=1,column=0,padx=5, pady=5, sticky='ew')
    
    
    DISPOSITION=ttk.Combobox(Dframe,state="readonly",values=["Disposition"])
    DISPOSITION.current(0)
    DISPOSITION.grid(row=1, column=1,padx=5, pady=5, sticky='ew')
    
    CAUSEDBY=ttk.Combobox(Dframe,state="readonly",values=["Caused By"])
    CAUSEDBY.current(0)
    CAUSEDBY.grid(row=1, column=2,padx=5, pady=5, sticky='ew')
    
    Comments=ttk.Entry(Dframe)
    Comments.insert(0,'Write down your comments here')
    Comments.bind("<FocusIn>",lambda ie: Comments.delete('0','end'))
    Comments.grid(row=2,columnspan=3,rowspan=2,padx=5, pady=5,sticky='ew')
    
    ##########################################################################
    a=tk.BooleanVar()
    checkbox=ttk.Checkbutton(F3, text="Check the box if the above data is Validated with database.", variable=a)
    checkbox.grid(row=1, column=0,padx=5, pady=5, sticky='nsew')
    
    ################################################################################
    Bframe= ttk.Frame(F3, borderwidth=0 ,width=67 )
    Bframe.grid(row=2,column=0,padx=5,pady=5,sticky='nsew')
    Bframe.columnconfigure(index=0, weight=1)
    Bframe.rowconfigure(index=0, weight=1)
    
    Insert=ttk.Button(Bframe, width= 33,text="Insert Data",command=lambda:App.DataToUpload())
    Insert.grid(row=0, column=0,padx=5, pady=5,sticky='ew')
    
    Deleterow=ttk.Button(Bframe,width= 33,text="Delete Select Row",command=lambda:App.Delete())
    Deleterow.grid(row=0, column=1,padx=5, pady=5,sticky='ew')
    
    Upload=ttk.Button(Bframe,width= 30,text="Upload",command=lambda:App.Upload(A,queue,Error))
    Upload.grid(row=1, column=0,padx=5, pady=5,sticky='ew',columnspan=2)
    
    # mode=ttk.Checkbutton(Bframe,text="Mode",style="Switch",command=App.toggle_mode)
    # mode.grid(row=2, column=0,padx=5, pady=5,sticky='nsew')
    
    #################################################################################
    
    
    seperator=ttk.Separator(F3)
    seperator.grid(row=3, column=0,padx=10, pady=10, sticky='ew')
    
    progresslabel=ttk.Label(F3, text="Progress Bar")
    progresslabel.grid(row=4, column=0,padx=10, pady=(3,0),sticky='ew')
    
    F3ProgressLabel=ttk.Label(F3, text="current status",font=("Arial",8))
    F3ProgressLabel.grid(row=5, column=0,padx=10, pady=0,sticky='ew')
    
    
    
    F3Progress=ttk.Progressbar(F3,maximum=100,mode="determinate")
    F3Progress.grid(row=6, column=0,padx=10, pady=10, sticky='ew')
    
    console=tk.Text(F3,width=50, height=5,font=("Courier New",10),foreground='green',padx=10,pady=10)
    console.grid(row=7, column=0,padx=10, pady=10, sticky='nsew')
    console.bind('<Configure>',lambda event: App.auto_scroll())
    # console.bind('<Configure>',lambda event: self.auto_scroll())
    # entry = ttk.Entry(F3)
    # entry.insert(0, "Entry")
    # entry.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="ew")
    
    F4= ttk.LabelFrame(W2, text=" Data To Be Uploaded ⚡ ",relief='sunken')
    F4.grid(row=0,column=1,sticky='nsew',padx=5,pady=5)
    F4.columnconfigure(index=0, weight=1)
    
    InsertScroll=ttk.Scrollbar(F4)
    InsertScroll.pack(side="right", fill="y",pady=5,padx=(0,5))
    # FetchScroll.grid(row=0, column=1, sticky='ns',pady=5,padx=(0,5))
    
    cols=('VER','ISA','REASON','DEFECT_TYPE','CAUSED_BY','DISPOSITION','COMMENTS','VALIDATION')
    InsertDATA=ttk.Treeview(F4, yscrollcommand=FetchScroll.set, show='headings', columns=cols, height=1)
    InsertDATA.column('VER', width=20)
    InsertDATA.column('ISA', width=120)
    InsertDATA.column('REASON', width=150)
    InsertDATA.column('DEFECT_TYPE', width=150)
    InsertDATA.column('CAUSED_BY', width=200)
    InsertDATA.column('DISPOSITION', width=100)
    InsertDATA.column('COMMENTS', width=220)
    InsertDATA.column('VALIDATION', width=80)
    # self.FetchedDATA.column('SHIPPER_A/C', width=50)
    InsertScroll.config(command=FetchedDATA.yview)
    InsertDATA.pack(expand=True, fill="both", padx=(5,0), pady=5)
    
    App.updatetree()
    
    root.mainloop()