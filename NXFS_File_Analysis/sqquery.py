import sqlite3
import csv
import main
import os

print(os.path.realpath('.\\NxFS_final.db'))

conn = sqlite3.connect("NxFS_final.db",isolation_level=None)        #exe니까 exe에 맞게 조정해봄. 맞는듯..
c = conn.cursor()

# 테이블 만들기
def Create():
    #conn = sqlite3.connect(".\\NxFS_12.db",isolation_level=None)
    #c = conn.cursor()

    c.execute("Select count(*) From sqlite_master Where name='ALLOCATION'")
    check = c.fetchone()
    #c.execute("Select count(*) From sqlite_master Where name='PATH'")
    #check1 = c.fetchone()
    c.execute("Select count(*) From sqlite_master Where name='UNALLOCATION'")
    check2 = c.fetchone()
    c.execute("Select count(*) From sqlite_master Where name='SLACK'")
    check3 = c.fetchone()

    if check[0] == 0:
        c.execute("Create Table ALLOCATION(FILE_INDEX text, START_CLUSTER text, END_CLUSTER text, SIZE text, FOLDER_INDEX text, NAME text, DATETIME text, FOLDER text,start_OFFSET text, END_OFFSET text)")

    
    
    #if check1[0] == 0:
    #    c.execute("Create Table PATH(path text)")
    if check2[0] == 0:
        c.execute("Create Table UNALLOCATION(FOLDER_INDEX text,START_OFFSET text,END_OFFSET text,SIZE text,FOLDER text)")
    if check3[0] == 0:
        c.execute("Create Table SLACK(NAME text,START_OFFSET text,END_OFFSET text,SIZE text,FOLDER text)")

#csv파일의 데이터 db에 저장
def csv_db(): #--------> 조건 미할당 파일이 있는지 없는지
    if os.path.isfile('csv\\allocated.csv'): 
        allocation = csv.reader(open('csv\\allocated.csv','r'))
        next(allocation,None)#csv를 읽을 때 헤더 없애기
    else:
        pass
    
    if os.path.isfile('csv\\unallocated-avi.csv'): 
        unallocation = csv.reader(open('csv\\unallocated-avi.csv','r'))
        next(unallocation,None)
    else:
        pass
    
    if os.path.isfile('csv\\slack.csv'):
        slack = csv.reader(open('csv\\slack.csv','r'))
        next(slack,None)
        
    Create()

    try:
        c.execute("select count(*) from ALLOCATION")
        reset = c.fetchone()
    except:
        pass
    
    try:
        c.execute("Select count(*) from UNALLOCATION")
        reset2= c.fetchone()
    except:
        pass
    
    try:
        c.execute("Select count(*) from SLACK")
        reset3 = c.fetchone()
    except:
        pass
    
    try:
        if reset[0] > 1:
            c.execute("delete from ALLOCATION")
            for row in allocation:
                index = row[0]
                allocation_data = c.execute("insert into ALLOCATION VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10]))
        else :
            for row in allocation:
                allocation_data = c.execute("insert into ALLOCATION VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10]))
                print(row)
    except:
        pass            
    
    
    try:            
        if reset2[0] > 1:
            c.execute("delete from UNALLOCATION")
            for row in unallocation:
                index = row[0]
                unallocation_data = c.execute("insert into UNALLOCATION VALUES(?, ?, ?, ?, ?)",(row[1],row[2],row[3],row[4],row[5]))
        else :
            for row in unallocation: 
                unallocation_data = c.execute("insert into UNALLOCATION VALUES(?, ?, ?, ?, ?)",(row[1],row[2],row[3],row[4],row[5]))
    except:
        pass

    try:
        if reset3[0] > 1:
            c.execute("delete from SLACK")
            for row in slack:
                index = row[0]
                slack_data = c.execute("insert into SLACK VALUES(?, ?, ?, ?, ?)",(row[1],row[2],row[3],row[4],row[5]))
        else :
            for row in slack:
                slack_data = c.execute("insert into SLACK VALUES(?, ?, ?, ?, ?)",(row[1],row[2],row[3],row[4],row[5]))
    except:
        pass
    c.connection.commit()
    #c.connection.close()
    

#결과값에 대한 탭
def result_tab(): # result 탭에 들어갈 결과값
    result_tab_ALLOCATION = "select name,start_offset,end_offset,size,datetime,folder,folder_index from ALLOCATION"
    c.execute(result_tab_ALLOCATION)
    ALLOCTION= c.fetchall()
    result_tab_UNALLOCATION = "select start_offset,end_offset,size,folder,folder_index from UNALLOCATION"
    c.execute(result_tab_UNALLOCATION)
    UNALLOCTION = c.fetchall()
    result_tab_SLACK = "select * from slack"
    c.execute(result_tab_SLACK)
    UNALLOCTION = c.fetchall()
    c.connection.commit()

# 파일 이름에서 시간을 뺴오는 함수
def time(): # 트리위젯 하위폴더 시간값
    time_sql = "select distinct replace(substring(datetime,0,11),'-','') from ALLOCATION group by datetime"
    c.execute(time_sql)
    s = c.fetchall()
    for line in s:
        for a in line:
           print(a)

'''
# 폴더 이름을 찾는 함수
def Foldername(): # 트리위젯 최상위 폴더 리스트
    fname = newcore.folder
    foldername = []
    for i in fname:
        foldername.append(i[0])
    print(foldername)
'''

#csv_db()


