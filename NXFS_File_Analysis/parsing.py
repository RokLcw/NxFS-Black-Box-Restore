import re
import pandas as pd
from pandas import DataFrame
import time
from datetime import datetime
import pickle
import numpy as np

import time # time 라이브러리 import
start = time.time() # 시작

global target
global NxFS_start
global NxFS_size
global BytesPerSector
global Cluster_size


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
    date = datetime.fromtimestamp(int(unixtime))
    return date


def df_to_sql(folder, file, filename):
    '''데이터프레임을 SQL로 저장'''
    import sqlite3
    import pandas as pd
    from pandas import Series, DataFrame


    conn = sqlite3.connect("D:\\NxFS.db",isolation_level=None)
    global c
    c = conn.cursor()

    s = folder
    q = file
    l = filename

    A = s.to_sql('FOLDER',conn, if_exists='replace', index=False)
    B = q.to_sql('FILE', conn, if_exists='replace', index=False)
    C = l.to_sql('FILENAME', conn, if_exists='replace')




target = 'D:/Urive.001'

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
        folder[i].append(convert_byte_to_int(Dir_data[14:18]) * SP * BytesPerSector)   # 실제 데이터에서 시작 클러스터 (오프셋)
        folder[i].append(convert_byte_to_int(Dir_data[18:22]) * SP * BytesPerSector)   # 실제 데이터에서 끝 클러스터 (오프셋)
    else:
        break   # 폴더명 위치에 값이 0일 경우 break
    

    file.seek(128, 1)
    
folder_df = pd.DataFrame(folder, columns=['name','start index', 'end index', 'start_offset', 'end_offset'])

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

print(count)

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
    print(now)  


p = []   # 데이터 나누어 저장
for j in range(0, len(idx), 4):
    p.append(idx[j:j+4])
file_df = pd.DataFrame(p, columns = ['file_index','start_offset','end_offset','size'])
file_df = file_df.drop_duplicates()   # 중복 제거

file_df_sorted = file_df.sort_values(by='start_offset')   # start offset이 적은 순으로 정렬
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
            fName_list[i].append(fDate)   # 유닉스 시간
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
    conditions.append((df['folder_index'] >= folder_df['start index'][i]) & (df['folder_index'] <= folder_df['end index'][i]))
    vals.append(folder_df['name'][i])

df['folder'] = np.select(conditions, vals)

filename_df = df.dropna()   # 결치값 삭제
filename_df.set_index('folder_index', inplace=True) 

print(filename_df)

# filename_df.to_csv('D:/filename.csv')


'''실제 데이터'''
offset = (NxFS_start + 128148) * BytesPerSector
file.seek(offset, 0)   # 실제 데이터 위치
print('Data area offset :', file.tell())
print('Data area offset :', hex(file.tell()))

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

    file_df.loc[file_df['start_offset'] == now - offset, 'folder_index'] = folder_id
    file_size = file_df_sorted.iat[i, -1]   # size


    # 할당 영역 파일 데이터프레임 정리
    p = re.compile('\w+(?=[.])')   # 파일이름에서 확장자 이전만 출력
    m = p.match(filename_df.at[folder_id, 'name'])
    FILENAME = m.group()   # 파일 이름 불러오기

    # file_df.loc[file_df['folder_index'] == folder_id, 'file_name'] = FILENAME


'''누락 데이터 추가하기'''
print(file_df_sorted.loc[omit])

file.seek(offset + file_df_sorted.at[omit, 'start_offset'])
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

print("count =", count)

    
file_df.loc[file_df['folder_index'] == folder_id, 'end_offset'] = (count - 1) * 65536 + file_df_sorted.at[omit, 'start_offset']

file.seek(offset + file_df_sorted.at[omit, 'end_offset'] + 6)
s = convert_byte_to_int(file.read(4)) + 14   # 헤더 사이즈 포함

file_df.loc[file_df['folder_index'] == folder_id, 'size'] = (count - 1) * 65536 + s


file_df_sorted.to_csv('D:/sorted.csv')
file_df.to_csv('D:/file_df.csv')


allocated = pd.merge(file_df, filename_df, on='folder_index')
# a = a.set_index('folder_index')

# df_to_sql(folder_df, file_df, filename_df)


print(allocated)   # 할당 영역 확정

allocated.to_csv('D:/allowcated.csv')
 
print(f"{time.time()-start:.4f} sec") # 종료와 함께 수행시간 출력



folder_name = folder_df['name'].tolist()

for name in folder_name:
    n = allocated.loc[allocated['folder'] == name]
    if n.empty:
        break
    print(n.iloc[-1])   # 할당 마지막 데이터 가져오기
        


# 미할당 오프셋

filex_list = []

for i in range(len(file_df)):
    file.seek((NxFS_start + 128148) * BytesPerSector + file_df.at[i, 'end_offset'], 0)   # end
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

print(filex_df)

file.close()




def All_export_to_avi(df):
    file = open(target, 'rb')

    for i in range(len(df)):
        file.seek((NxFS_start + 128148) * BytesPerSector + df.at[i, 'start_offset'], 0)   # start
        now = file.tell()

        if df.at[i, 'start_offset'] > df.at[i, 'end_offset']:
            print(df.at[i, 'file_index'])
            print(now)
            
            
        
        file_size = df.at[i, 'size']
        d = file.read(file_size)

        # 할당 영역 파일 추출
        p = re.compile('\w+(?=[.])')   # 파일이름에서 확장자 이전만 출력
        m = p.match(df.at[i, 'name'])
        FILENAME = m.group()   # 파일 이름 불러오기

        # 클러스터 단위로 저장
        with open("data.pickle", 'wb') as fw:    
            # pickle.dump(d, fw)
            fw.write(d)
        
        D = open("data.pickle", "rb")

        # 분할된 파일 합쳐서 추출
        with open(FILENAME+'.avi', 'wb') as f:
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


def export_slack(df):
    file = open(target, 'rb')

    # 슬랙 공간 추출
    file.seek((NxFS_start + 128148) * BytesPerSector + df.at[i, 'end_offset'], 0)   # end
    file.seek(6, 1)
    size = convert_byte_to_int(file.read(4))   # 사이즈 위치 읽기
    file.seek(4, 1)
    file.seek(size, 1)

    SLACK_NAME = file.tell()
    slack = file.read(Cluster_size - 14 - size)   # 헤더 값과 실제데이터를 뺀 부분 = 슬랙

    with open(str(SLACK_NAME), 'wb') as s:
        s.write(slack)

    file.close()

def unallocated(df):
    print(df)


# All_export_to_avi(a)

print(f"{time.time()-start:.4f} sec")