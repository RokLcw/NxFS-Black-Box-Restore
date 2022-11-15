import re
import pandas as pd
import time
from datetime import datetime


def convert_byte_to_int(bytes):
    '''byte를 리틀엔디안 형식으로 읽어서 int로 형변환하는 함수'''
    return int.from_bytes(bytes, 'little', signed=False)

def is_NxFS(BR):
    if BR[3:7].decode('ascii') == 'NxFS':
        return True
    else:
        return quit()

def convert_datetime(unixtime):
    '''Convert unixtime to datetime'''
    date = datetime.fromtimestamp(int(unixtime))
    return date



target = 'D:/Urive.001'

file = open(target, 'rb')


'''BR 탐색 및 이동'''
file.seek(470)

NxFS_start = convert_byte_to_int(file.read(4))   # NxFS 파티션 시작 위치 읽고 변환
NxFS_size = convert_byte_to_int(file.read(4))   # NxFS 파티션 크기 읽고 변환

print('NxFS Partition start(sector) :', NxFS_start)
print('NxFS Partition size(sector) :', NxFS_size)

file.seek(NxFS_start * 512)   # NxFS 파티션 시작 위치로 이동

NxFS_header = file.read(14)

# print(NxFS_header)

is_NxFS(NxFS_header)   # 헤더 확인

BytesPerSector = convert_byte_to_int(NxFS_header[11:13])
SP = NxFS_header[13]

Cluster_size = SP * BytesPerSector

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
        folder[i].append(convert_byte_to_int(Dir_data[14:18]) * SP)   # 실제 데이터에서 오프셋 시작 (섹터 단위)
        folder[i].append(convert_byte_to_int(Dir_data[18:22]) * SP)   # 실제 데이터에서 오프셋 끝 (섹터 단위)
    else:
        break   # 폴더명 위치에 값이 0일 경우 break
    

    file.seek(128, 1)
    
folder_df = pd.DataFrame(folder, columns=['name','start index', 'end index', 'start sector', 'end sector'])

print(folder_df)


'''파일 메타데이터 탐색'''
file.seek(NxFS_start * BytesPerSector)
file.seek(1582 * BytesPerSector, 1)   # 1582 sector 부터 시작


data = convert_byte_to_int(file.read(4))   # 섹터의 첫 4 바이트 읽고 해석
file.seek(-4, 1)



'''NORMAL 폴더 데이터'''
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

print("file metadata area(sector) :", NxFS_start + 1582 + count)
idx = []

while True:
    if data == 0:
        file.seek(16, 1)   # 파일 인덱스 0이면 계속 이동
        data = convert_byte_to_int(file.read(4))
        file.seek(-4, 1)
    else:
        data = convert_byte_to_int(file.read(4))   # 실제 데이터 파일 인덱스
        idx.append(data)
        
        idx.append(convert_byte_to_int(file.read(4)) * SP)   # 실제 데이터 시작 섹터 위치
        idx.append(convert_byte_to_int(file.read(4)) * SP)   # 실제 데이터 끝 섹터 위치 (클러스터 헤더 위치)
        idx.append(convert_byte_to_int(file.read(4)))   # 파일 사이즈
        
        if data == 0:
            del idx[-4:]
            break

p = []   # 데이터 나누어 저장
for j in range(0, len(idx), 4):
    p.append(idx[j:j+4])

file_df = pd.DataFrame(p, columns = ['index','start sector','end sector','size'])
print(file_df)




'''파일 인덱스 탐색'''
file.seek((NxFS_start + 15647) * BytesPerSector)
print(file.tell())



fName_list = []

file.seek(96 + 2, 1)
fIndex = convert_byte_to_int(file.read(4))   # 파일 인덱스 값 읽기
file.seek(-102, 1)

for i in range(len(folder_df)):
    filelist_count = folder_df['end index'][i] - folder_df['start index'][i]

    print(filelist_count)
    
    for j in range(filelist_count):
        if fIndex:
            fName = file.read(32)
            fName_list.append(re.findall("[A-Za-z0-9_.]+", fName.decode('ascii')))
            file.seek(64 + 2, 1)
            fIndex = convert_byte_to_int(file.read(4))
            fName_list[j].append(fIndex)   # 파일 인덱스
            file.seek(4, 1)
            fDate = convert_byte_to_int(file.read(4))
            fName_list[j].append(fDate)   # 유닉스 시간
            file.seek(2 + 16, 1)

        else:
            break

    

filename_df = pd.DataFrame(fName_list, columns=['name','file index', 'datetime'])

print(filename_df)


file.close()
