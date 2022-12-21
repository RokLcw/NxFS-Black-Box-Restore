import re
import pandas as pd
from pandas import DataFrame
import time
from time import strftime
from time import gmtime
from datetime import datetime
import pickle
import numpy as np
import sqlite3
import os
import sys
import argparse
#from NxFS_Analyzer import Ui_MainWindow

from pathlib import Path

import time # time 라이브러리 import
start = time.time() # 시작

global target
global NxFS_start
global NxFS_size
global BytesPerSector
global Cluster_size
global DATA_AREA


def convert_byte_to_int(bytes):
    '''byte를 리틀엔디안 형식으로 읽어서 int로 형변환하는 함수'''
    return int.from_bytes(bytes, 'little', signed=False)

def is_mbr(mbr):
    if mbr[-2] == 0x55 and mbr[-1] == 0xAA: # MBR의 Magic ID 판별
        return True
    else:
        return False

def is_NxFS(BR):
    if BR[3:7].decode('ascii') == 'NxFS':
        return True
    else:
        return quit()

def convert_datetime(unixtime):
    '''Convert unixtime to datetime'''
    dt = time.gmtime(unixtime)
    dt = time.strftime('%Y-%m-%d %H:%M:%S', dt)
    return dt

def save_file_at_dir(dir_path, filename, file_content, mode='w'):
    os.makedirs(dir_path, exist_ok=True)
    with open(os.path.join(dir_path, filename), mode) as f:
        f.write(file_content)


def All_export_to_avi(file_df, folder_df):
    file = open(target, 'rb')

    file_df = file_df.reset_index(drop=True)

    if args.dir_path:
        dir_path = args.dir_path
    else:
        for f in folder_df['name'].to_list():
            dir_path = f
            os.makedirs(dir_path, exist_ok=True)

    for i in range(len(file_df)):
        file.seek(file_df.at[i, 'start_offset'], 0)   # start
        now = file.tell()

        if file_df.at[i, 'start_offset'] > file_df.at[i, 'end_offset']:
            folder_df.set_index('name', inplace=True)
            folder = file_df.at[i, 'folder']
            end = folder_df.at[folder, 'end_offset_P']
            size_1 = end - now
            d1 = file.read(size_1)
            size_2 = file_df.at[i, 'size'] - size_1
            d2 = file.read(size_2)
            d = d1 + d2
    
        else:
            file_size = file_df.at[i, 'size']
            d = file.read(file_size)

        
        if isinstance(file_df.at[i, 'name'], str):
            p = re.compile('\w+(?=[.])')   # 파일이름에서 확장자 이전만 출력
            m = p.match(file_df.at[i, 'name'])
            FILENAME = m.group()   # 파일 이름 불러오기
        else:
            FILENAME = str(file_df.at[i, 'name'])


        # 클러스터 단위로 저장
        with open(".\\data.pickle", 'wb') as fw:    
            # pickle.dump(d, fw)
            fw.write(d)
        
        D = open(".\\data.pickle", "rb")

        # 분할된 파일 합쳐서 추출

        DIRPATH = file_df.at[i, 'folder']
        with open(os.path.join(DIRPATH, FILENAME+'.avi'), 'wb') as f:
            n = 1
            while True:
                h = D.read(14)
                s = convert_byte_to_int(h[6:8])
                data = D.read(s)
                if not data:
                    break
                f.write(data)
                D.seek(0)
                D.seek(65536 * n, 1)
                n += 1

        D.close()

    file.close()

    pkle = '.\\data.pickle'

    if os.path.isfile(pkle):
        os.remove(pkle)


# 인덱스 값은 슬랙 이름으로 넘어와야 함
def select_export_slack(name, df):
    df.set_index('name', inplace=True)
    print(df)
    file = open(target, 'rb')

    df = df.loc[name]

    if args.dir_path:
        dir_path = args.dir_path
    else:
        for f in folder_df['name'].to_list():
            dir_path = f
            os.makedirs(dir_path, exist_ok=True)

    DIRPATH = 'slack'
    os.makedirs(DIRPATH, exist_ok=True)

    # 슬랙 추출
    for i in name:
        file.seek(df.at[i, 'start_offset'], 0)
        size = df.at[i, 'size']

        SLACK_NAME = str(i)
        slack = file.read(size)   # 헤더 값과 실제데이터를 뺀 부분 = 슬랙

        with open(os.path.join(DIRPATH, SLACK_NAME), 'wb') as s:
            s.write(slack)

    file.close()


# unallocated 해석
def unallocated(file_df, folder_df):
    file = open(target, 'rb')
    folder_name = folder_df['name'].tolist()

    for name in folder_name:
        n = file_df.loc[file_df['folder'] == name]
        if n.empty:
            break

        end_A = n.iloc[-1]   # 할당 마지막 데이터 가져오기


        LIST = []
        DF = folder_df.set_index(['name'])
        if  end_A['end_clus'] > end_A['start_clus']:
            
            unallocated_start = DATA_AREA + end_A['end_clus'] + Cluster_size
            unallocated_end = DF.at[name, 'end_offset_P']

            now = file.tell()
            
            n = 0
            
            while now < unallocated_end:
                file.seek(unallocated_start + Cluster_size * n)
                parser = re.compile("RIFF")
                file.seek(14, 1)
                keyword = file.read(4)
                if keyword == b'RIFF':
                    now = file.tell()
                    filename = now
                    file.seek(unallocated_start + Cluster_size * n)
                    H = file.read(14)
                    file.seek(-14, 1)
                    folder_id = convert_byte_to_int(H[2:6])
                    c_size = convert_byte_to_int(H[6:8])
                    LIST.append(folder_id)
                    
                    header = H[0:6]
                    start = file.tell()
                    LIST.append(start)
                    LIST.append(start)
                    count = 0
                    while c_size == 65522:
                        file.seek(Cluster_size, 1)
                        H = file.read(14)
                        file.seek(-14, 1)
                        c_size = convert_byte_to_int(H[6:8])
                        count += 1
                    
                    end = file.tell()
                    LIST.append(end)
                    LIST.append(end + 14 + c_size - start)
                    LIST.append(name)
                
                now = file.tell()
                n += 1

    global filex_avi

    if LIST:
        p = []   # 데이터 나누어 저장
        for j in range(0, len(LIST), 6):
            p.append(LIST[j:j+6])
        filex_avi = pd.DataFrame(p, columns=['folder_index', 'name', 'start_offset', 'end_offset', 'size', 'folder'])
        return filex_avi.to_csv('csv\\unallocated-avi.csv')
    else:
        filex_avi = pd.DataFrame()

    file.close()


# 인덱스 값은 리스트로 넘어와야 함
def select_export_avi(index, df):
    df.set_index('folder_index', inplace=True)

    file = open(target, 'rb')

    df = df.loc[index]

    
    for i in index:
        if isinstance(df.at[i, 'name'], str):
            p = re.compile('\w+(?=[.])')   # 파일이름에서 확장자 이전만 출력
            m = p.match(df.at[i, 'name'])
            FILENAME = m.group()   # 파일 이름 불러오기
        else:
            FILENAME = str(df.loc[i, 'start_offset'])
    
        file.seek(df.at[i, 'start_offset'], 0)
        file_size = df.at[i, 'size']
        d = file.read(file_size)

        # 클러스터 단위로 저장
        with open("data.pickle", 'wb') as fw:    

            fw.write(d)
        
        D = open("data.pickle", "rb")

        DIRPATH = df.at[i, 'folder']

        os.makedirs(DIRPATH, exist_ok=True)

        # 분할된 파일 합쳐서 추출
        with open(os.path.join(DIRPATH, FILENAME+'.avi'), 'wb') as f:
            n = 1
            while True:
                h = D.read(14)
                s = convert_byte_to_int(h[6:8])
                data = D.read(s)
                if not data:
                    break
                f.write(data)
                D.seek(0)
                D.seek(65536 * n, 1)
                n += 1

        D.close()

    file.close()

    pkle = 'data.pickle'

    if os.path.isfile(pkle):
        os.remove(pkle)

import hashlib


def select_hash_avi(index, df):
    df.set_index('folder_index', inplace=True)
    df = df.loc[index]

    file = open(target, 'rb')
    
    for i in index:
        if isinstance(df.at[i, 'name'], str):
            p = re.compile('\w+(?=[.])')   # 파일이름에서 확장자 이전만 출력
            m = p.match(df.at[i, 'name'])
            FILENAME = m.group()   # 파일 이름 불러오기
        else:
            FILENAME = str(df.loc[i, 'start_offset'])
    
        file.seek(df.at[i, 'start_offset'], 0)
        file_size = df.at[i, 'size']
        d = file.read(file_size)

        # 클러스터 단위로 저장
        with open("data.pickle", 'wb') as fw:    

            fw.write(d)
        
        D = open("data.pickle", "rb")

        # 해시값 계산
        md5 = hashlib.md5()
        sha_1 = hashlib.sha1()
        sha_256 = hashlib.sha256()
    
        n = 1
        while True:
            h = D.read(14)
            s = convert_byte_to_int(h[6:8])
            data = D.read(s)
            if not data:
                break
            md5.update(data)
            sha_1.update(data)
            sha_256.update(data)
            
            D.seek(0)
            D.seek(65536 * n, 1)
            n += 1

        D.close()
        
        print(md5.hexdigest())   # return
        print(sha_1.hexdigest())
        print(sha_256.hexdigest())

    file.close()

    pkle = 'data.pickle'

    if os.path.isfile(pkle):
        os.remove(pkle)
        

# 인덱스 값은 슬랙 이름으로 넘어와야 함
def select_hash_slack(name, df):
    df.set_index('name', inplace=True)
    file = open(target, 'rb')

    df = df.loc[name]

    # 슬랙 추출
    for i in name:
        file.seek(df.at[i, 'start_offset'], 0)
        size = df.at[i, 'size']

        SLACK_NAME = str(i)
        slack = file.read(size)   # 헤더 값과 실제데이터를 뺀 부분 = 슬랙

        print(hashlib.md5(slack).hexdigest())   # return
        print(hashlib.sha1(slack).hexdigest())
        print(hashlib.sha256(slack).hexdigest())

    file.close()


#print(sys.argv)
#print(os.path.dirname(os.path.abspath(__file__)))


#코드 맞음. 안될 경우, db change commit 이 안됐거나, 파이썬 실행경로가 문제있거나, 다른 코드가 안바뀌어서 그렇거나.
#이코드는 .exe로 만들었을때 돌아가는 경로가 맞음..
print(os.path.realpath('./'))
#conn = sqlite3.connect(os.path.realpath('../../NxFS_12.db'),isolation_level=None)


#print(os.path.realpath('../../NxFS_12.db'))

#input()


#conn = sqlite3.connect(os.path.realpath('./NxFS_12.db'))
#main.py 상에서 결과 확인용으로 돌아가게는 이코드.. 엥...
#cur = conn.cursor()

#print(sys.argv)
#print(os.path.dirname(os.path.abspath(__file__)))

#cur.execute("SELECT path FROM PATH")
#sqlpath = cur.fetchone()
#print(target)
#print(dirpath+"\\NxFS_12.db")

#print(dirpath)

print(sys.argv)


parser = argparse.ArgumentParser()
parser.add_argument('-p', dest='path', help='file system analysis')
parser.add_argument('-all', help='all avi export', action='store_true')
parser.add_argument('-e', dest='export', nargs='+', help='export avi (allocated)', type=int)
parser.add_argument('-u', dest='export_u', nargs='+', help='export avi (unallocated)', type=int)
parser.add_argument('-s', dest='slack', nargs='+', help='export slack', type=int)
parser.add_argument('-ha', dest='hashavi', nargs='+', help='hash avi', type=int)
parser.add_argument('-hs', dest='hashslack', nargs='+', help='hash slack', type=int)
parser.add_argument('-dir', dest='dir_path')
#parser.add_argument('--save_dir', dest='save', default='./result/', help='avi save directory path')


args = parser.parse_args()
print(args.path)
print(args.export)


target = args.path

#target = 'H:\\bob11기 프로젝트\\urive\\urive image.001'

file = open(target, 'rb')


'''BR 탐색 및 이동'''
file.seek(446)
MBR = file.read(66)
is_mbr(MBR)

info = MBR[16:32]

NxFS_start = convert_byte_to_int(info[8:12])   # NxFS 파티션 시작 위치 읽고 변환
NxFS_size = convert_byte_to_int(info[12:16])   # NxFS 파티션 크기 읽고 변환


file.seek(NxFS_start * 512)   # NxFS 파티션 시작 위치로 이동

NxFS_header = file.read(14)

is_NxFS(NxFS_header)   # 헤더 확인

BytesPerSector = convert_byte_to_int(NxFS_header[11:13])
SP = NxFS_header[13]

Cluster_size = SP * BytesPerSector


print('NxFS Partition start(sector/offset) : {} / {}'.format(NxFS_start, NxFS_start * SP))
print('NxFS Partition size(sector/offset) : {} / {}'.format(NxFS_size, NxFS_size * SP))
print('Cluster size(byte) :', Cluster_size)


'''폴더명 탐색'''
file.seek(NxFS_start * BytesPerSector)
file.seek(1569 * BytesPerSector, 1)   # 1569 sector = 폴더명 저장 위치

folder = []

for i in range(4):        
    Dir_data = file.read(32)
    file.seek(-32, 1)

    Name = Dir_data[22:33]
    n = convert_byte_to_int(Name)

    if n:
        folder.append(re.findall("[A-Za-z]+", Name.decode('ascii')))
        folder[i].append(convert_byte_to_int(Dir_data[4:8]))   # 파일 인덱스 시작
        folder[i].append(convert_byte_to_int(Dir_data[8:12]))   # 파일 인덱스 끝
        folder[i].append(convert_byte_to_int(Dir_data[14:18]))   # 실제 데이터에서 시작 클러스터
        folder[i].append(convert_byte_to_int(Dir_data[18:22]))   # 실제 데이터에서 끝 클러스터
        folder[i].append((convert_byte_to_int(Dir_data[14:18]) * SP + NxFS_start + 128148) * BytesPerSector)
        folder[i].append((convert_byte_to_int(Dir_data[18:22]) * SP + NxFS_start + 128148) * BytesPerSector + Cluster_size)
    else:
        break   # 폴더명 위치에 값이 0일 경우 break
    

    file.seek(128, 1)
    
folder_df = pd.DataFrame(folder, columns=['name','start_index', 'end_index', 'start_cluster_L', 'end_cluster_L', 'start_offset_P', 'end_offset_P'])

print(folder_df)

# folder_df.to_csv('D:/folder.csv', index=False)



'''파일 메타데이터 탐색'''
file.seek(NxFS_start * BytesPerSector)
file.seek(1582 * BytesPerSector, 1)   # 1582 sector 부터 시작


data = convert_byte_to_int(file.read(4))   # 섹터의 첫 4 바이트 읽고 해석
file.seek(-4, 1)


'''파일 메타데이터 시작 위치 탐색'''
count = 0
while True:
    if data == 0:
        file.seek(BytesPerSector, 1)   # 한 섹터 씩 이동
        data = convert_byte_to_int(file.read(4))
        file.seek(-4, 1)
        count += 1
    else:
        file.seek(-BytesPerSector, 1)
        # 첫 바이트가 데이터가 있는 전 섹터부터 한 줄 씩 탐색
        data = convert_byte_to_int(file.read(4))
        file.seek(-4, 1)
        break        

count -= 1

METADATA_AREA = NxFS_start + 1582 + count

print("file metadata area(sector) :", METADATA_AREA)


'''메타데이터 읽고 저장'''
file.seek(METADATA_AREA * BytesPerSector)   # 메타데이터 위치로 이동

idx = []

now = file.tell()

while now < ((METADATA_AREA + 4688) * BytesPerSector):
    now = file.tell()
    data = convert_byte_to_int(file.read(4))   # 섹터의 첫 4 바이트 읽고 해석
    file.seek(-4, 1)
    
    while True:
        if data == 0:
            file.seek(16, 1)   # 파일 인덱스 0이면 계속 이동
            data = convert_byte_to_int(file.read(4))
            file.seek(-4, 1)
        else:
            data = convert_byte_to_int(file.read(4))   # 실제 데이터 파일 인덱스
            idx.append(data)
            
            idx.append(convert_byte_to_int(file.read(4)) * SP * BytesPerSector)   # 실제 데이터 시작 위치
            idx.append(convert_byte_to_int(file.read(4)) * SP * BytesPerSector)   # 실제 데이터 끝 위치 (클러스터 헤더 위치)
            idx.append(convert_byte_to_int(file.read(4)))   # 파일 사이즈

            if data == 0:
                del idx[-4:]
                now = file.tell()
                break
        
    now = file.tell()  



p = []   # 데이터 나누어 저장
for j in range(0, len(idx), 4):
    p.append(idx[j:j+4])
file_df = pd.DataFrame(p, columns = ['file_index','start_clus','end_clus','size'])
file_df = file_df.drop_duplicates()   # 중복 제거

file_df_sorted = file_df.sort_values(by='start_clus')   # start offset이 적은 순으로 정렬
file_df_sorted.set_index('file_index', inplace=True)   # 파일 인덱스 새로 지정 (loc 유용)


# 파일 인덱스 탐색
file.seek((NxFS_start + 15647) * BytesPerSector)

now = file.tell()   # 현재 위치

i = 0

while now < ((NxFS_start + 15647 + 37500) * BytesPerSector): 
    fName_list = []
    now = file.tell()
    file.seek(96 + 2, 1)
    fIndex = convert_byte_to_int(file.read(4))   # 폴더 인덱스 값 읽기
    file.seek(-102 , 1)

    while now < ((NxFS_start + 15647 + 37500) * BytesPerSector):
        if fIndex:
            if fIndex == 0:
                now = file.tell()
                break

            fName = file.read(32)
            p = re.compile("[A-Za-z0-9_.]+")   
            m = p.findall(fName.decode('ascii'))   # 파일 이름 값
            fName_list.append(m)
            file.seek(64 + 2, 1)

            fIndex = convert_byte_to_int(file.read(4))
            fName_list[i].append(fIndex)   # 파일 인덱스
            file.seek(4, 1)
            
            fDate = convert_byte_to_int(file.read(4))
            fName_list[i].append(fDate)    # 유닉스 시간
            file.seek(2 + 16, 1)

            i += 1
            
        else:    
            file.seek(128 ,1)
            file.seek(96 + 2, 1)
            fIndex = convert_byte_to_int(file.read(4))   # 폴더 인덱스 값 읽기
            file.seek(-102 , 1)

            now = file.tell()
            
    now = file.tell()


df = pd.DataFrame(fName_list, columns=['name','folder_index', 'datetime'])   # 파일 이름 및 폴더 인덱스, 생성 시간


conditions = []
vals = []
for i in range(len(folder_df)):
    conditions.append((df['folder_index'] >= folder_df['start_index'][i]) & (df['folder_index'] <= folder_df['end_index'][i]))
    vals.append(folder_df['name'][i])


df['folder'] = np.select(conditions, vals)


filename_df = df.dropna()   # 결치값 삭제
filename_df.set_index('folder_index', inplace=True) 


# filename_df.to_csv('filename.csv')


'''실제 데이터'''
offset = (NxFS_start + 128148) * BytesPerSector
file.seek(offset, 0)   # 실제 데이터 위치
DATA_AREA = file.tell()

print('Data area offset :', DATA_AREA)
print('Data area offset :', hex(DATA_AREA))

file.seek((NxFS_start + 128148) * BytesPerSector)

header = file.read(14)   # 실제데이터의 클러스터 헤더 읽기

folder_id = convert_byte_to_int(header[2:6])
file_id = convert_byte_to_int(header[10:14])



file_df['folder_index'] = 0

'''파일 메타데이터 저장'''
for i in range(len(file_df_sorted)):
    if file_df_sorted.iat[i, 1] == 0:
        file.seek(offset + file_df_sorted.iat[i, 0], 0)   # start
        omit = file_df_sorted.index[i]   # end offset이 0일 때
        
    else:
        file.seek(offset + file_df_sorted.iat[i, 1], 0)   # end (overwrite 고려)
    
    now = file.tell()
    
    header = file.read(14)
    file.seek(-14, 1)
    
    folder_id = convert_byte_to_int(header[2:6])
    file_id = convert_byte_to_int(header[10:14])
    
    file.seek(offset + file_df_sorted.iat[i, 0], 0)   # start
    now = file.tell()

    file_df.loc[file_df['start_clus'] == now - offset, 'folder_index'] = folder_id
    file_size = file_df_sorted.iat[i, -1]   # size


    # 할당 영역 파일 데이터프레임 정리
    p = re.compile('\w+(?=[.])')   # 파일이름에서 확장자 이전만 출력
    m = p.match(filename_df.at[folder_id, 'name'])
    FILENAME = m.group()   # 파일 이름 불러오기

    # file_df.loc[file_df['folder_index'] == folder_id, 'file_name'] = FILENAME


    '''누락 데이터 추가하기'''
    # file_df_sorted.loc[omit]

    try: 
        print(file_df_sorted.loc[omit])
        file.seek(offset + file_df_sorted.at[omit, 'start_clus'])
        N = file.read(14)
        file.seek(-14, 1)
        folder_id = convert_byte_to_int(N[2:6])

        count = 0
        while True:
            H = file.read(14)
            file.seek(65522, 1)
            if convert_byte_to_int(H[10:14]) != omit:
                break
            count += 1
    except NameError:
        continue
        
    file_df.loc[file_df['folder_index'] == folder_id, 'end_clus'] = (count - 1) * 65536 + file_df_sorted.at[omit, 'start_clus']

    file.seek(offset + file_df_sorted.at[omit, 'end_clus'] + 6)
    s = convert_byte_to_int(file.read(4)) + 14   # 헤더 사이즈 포함

    file_df.loc[file_df['folder_index'] == folder_id, 'size'] = (count - 1) * 65536 + s


allocated = pd.merge(file_df, filename_df, on='folder_index')
allocated = allocated.sort_values(by='start_clus')


p_offset = []

for o in allocated['start_clus'].tolist():
    p_offset.append((128148 + NxFS_start) * BytesPerSector + o)

p_offset_end = []

i = 0
for k in allocated['size'].tolist():
    p_offset_end.append(k + p_offset[i])
    i += 1

allocated['start_offset'] = p_offset
allocated['end_offset'] = p_offset_end

t = []
for j in allocated.datetime:
    t.append(convert_datetime(j))

allocated['datetime'] = t


print(allocated)   # 할당 영역 확정

os.makedirs('csv', exist_ok=True)
 
print(f"{time.time()-start:.4f} sec") # 종료와 함께 수행시간 출력

allocated.to_csv('csv\\allocated.csv')


# 미할당 오프셋

filex_list = []

for i in range(len(allocated)):
    file.seek((NxFS_start + 128148) * BytesPerSector + allocated.at[i, 'end_clus'], 0)   # end
    file.seek(6, 1)
    size = convert_byte_to_int(file.read(4))   # 사이즈 위치 읽기
    file.seek(4, 1)
    file.seek(size, 1)

    SLACK_NAME = file.tell()
    slack_size = Cluster_size - 14 - size
    filex_list.append([SLACK_NAME])
    filex_list[i].append(SLACK_NAME)
    filex_list[i].append(SLACK_NAME + slack_size)
    filex_list[i].append(slack_size)


filex_df = pd.DataFrame(filex_list, columns=['name', 'start_offset', 'end_offset', 'size'])


SLACK_DF = filex_df.drop(filex_df[filex_df['size'] == 0].index)

unallocated(allocated, folder_df) # 미할당 정의 함수 출력

# 슬랙 추가
if not filex_avi.empty:
    slack_list = []
    for i in range(len(filex_avi)):
        file.seek(filex_avi.at[i, 'end_offset'], 0)   # end
        file.seek(6, 1)
        size = convert_byte_to_int(file.read(4))   # 사이즈 위치 읽기
        file.seek(4, 1)
        file.seek(size, 1)

        SLACK_NAME = file.tell()
        slack_size = Cluster_size - 14 - size
        slack_list.append([SLACK_NAME])
        slack_list[i].append(SLACK_NAME)
        slack_list[i].append(SLACK_NAME + slack_size)
        slack_list[i].append(slack_size)
        
    unallocated_slack = pd.DataFrame(slack_list, columns=['name', 'start_offset', 'end_offset', 'size'])
    SLACK_DF = pd.concat([filex_df, unallocated_slack])

    avi_df = pd.concat([allocated, filex_avi])
else:
    avi_df = allocated

conditions = []
vals = []
for i in range(len(folder_df)):
    conditions.append((SLACK_DF['start_offset'] >= folder_df['start_offset_P'][i]) & (SLACK_DF['start_offset'] <= folder_df['end_offset_P'][i]))
    vals.append(folder_df['name'][i])

SLACK_DF['folder'] = np.select(conditions, vals)

SLACK_DF = SLACK_DF.drop(SLACK_DF[SLACK_DF['size'] == 0].index)
SLACK_DF.sort_values(by='start_offset')
SLACK_DF = SLACK_DF.reset_index(drop=True)

file.close()

SLACK_DF.to_csv('csv\\slack.csv')

avi_df.to_csv('csv\\avi.csv')





try:
    if args.all:
        All_export_to_avi(avi_df, folder_df)

    if args.export:
        select_export_avi(args.export, allocated)
        
    if args.export_u:
        select_export_avi(args.export_u, filex_avi)

    if args.slack:
        select_export_slack(args.slack, SLACK_DF)

    if args.hashavi:
        select_hash_avi(args.hashavi, avi_df)

    if args.hashslack:
        select_hash_slack(args.hashslack, SLACK_DF)

except Exception as e:
    print(e)



'''avi 및 슬랙 추출 호출 함수'''
# select_export_slack(list(range(10,30)), SLACK_DF)
# select_export_avi([4299], allocated)
# All_export_to_avi(allocated, folder_df)

print(f"{time.time()-start:.4f} sec")


#input()
