import sys
import os
import time
from memory_profiler import memory_usage
from math import ceil 

def size_return(bytes):
    size_result = str(bytes) + 'Byte'
    if (bytes > 1024*1024*1024*1024):
        size_result = str(int(ceil(bytes/(1024*1024*1024*1024)))) + 'TB'
    elif (bytes > 1024*1024*1024):	
        size_result = str(int(ceil(bytes/(1024*1024*1024)))) + 'GB'
    elif (bytes > 1024*1024):	
        size_result = str(int(ceil(bytes/(1024*1024)))) + 'MB'
    elif (bytes > 1024):	
        size_result = str(int(ceil(bytes/(1024)))) + 'KB'
    return size_result

if __name__ == '__main__':
    start_time = time.time()

    file_size = os.path.getsize(sys.argv[1])

    print('\n[*] Input_file :', sys.argv[1],' ','Size :', size_return(file_size),'\n')

    if(sys.argv[1][-3:] != "avi"):
        print("Not AVI, check file")
        exit(1)

    with open(sys.argv[1], "rb") as media_file:
        data = media_file.read()
    
    # with open("result.avi", "ab") as f:
    #     f.write(data)

    if(data[0:4] != b"\x52\x49\x46\x46"):
        print("No Signature(Magic Number)")

    # -------------------hdrl-------------------
    # print(data[16:20])
    # print(int.from_bytes(data[16:20], 'little'))

    hdrl_size = int.from_bytes(data[16:20], 'little')
    hdrl = data[12:20 + hdrl_size]
    # print(hdrl)

    # -------------------avih-------------------
    # print(hdrl[16:20])
    avih_size = int.from_bytes(hdrl[16:20], 'little')
    # print(avih_size)
    avih = hdrl[12:16 + avih_size]

    # -------------------strl-------------------
    strl_size = []
    strl = []
    strl_key = []
    check_list_size = 20 + avih_size
    # print(size)
    cnt = 0
    # print("hdrl_size: ", hdrl_size)
    while(True):
        # print(hdrl[size:size+4])
        # print(hdrl[size+4:size+8])
        # -------------------strl size-------------------
        # print("List Size: ", int.from_bytes(hdrl[check_list_size+4:check_list_size+8], 'little'))
        strl_size.append(int.from_bytes(hdrl[check_list_size+4:check_list_size+8], 'little'))
        # print("누적 size: ", check_list_size - 8)

        # -------------------strl input-------------------
        strl.append(hdrl[check_list_size:check_list_size + 8 + strl_size[cnt]])

        # -------------------strl key-------------------
        strl_key.append(hdrl[check_list_size + 20:check_list_size + 24])
        # strl.append()
        check_list_size += (strl_size[cnt] + 8)
        cnt += 1

        if ((hdrl_size) == check_list_size - 8):  # 마지막에 발생하는 +8을 제외시킴
            break

    # print(strl_size)
    # print(strl)
    print("strl list: ", strl_key)

    # -------------------Junk-------------------
    check_list_size -= 8
    Junk_Start_offset = 20 + hdrl_size
    junk_size = 0
    # print("Junk: ", data[Junk_Start_offset:Junk_Start_offset+4])

    if(data[Junk_Start_offset:Junk_Start_offset+4] == b"\x4A\x55\x4E\x4B"):
        print("Junk start offset: ", hex(Junk_Start_offset))
        junk_size = int.from_bytes(data[check_list_size + 24:check_list_size + 28], 'little')
        # print(check_list_size+20)
        # print(junk_size)
        Junk = data[check_list_size + 20:((check_list_size + 20) + 8) + junk_size]
        # print(Junk)
        # print(int.from_bytes(data[check_list_size + 24:check_list_size + 28], 'little'))
        junk_size += 8  # junk가 있는경우 movi start offset을 계산하기 위함.

    # -------------------movi list -------------------
    movi_list_start_offset = 20 + hdrl_size + junk_size
    print("movi list start offset: ", hex(movi_list_start_offset))
    movi_list_size = int.from_bytes(data[movi_list_start_offset+4:movi_list_start_offset+8], 'little')
    # print(movi_list_size)
    movi = data[movi_list_start_offset:movi_list_start_offset+8+movi_list_size]
        
    # with open("movi", "ab") as f:
    #     f.write(movi)

    # print(movi_list_start_offset+movi_list_size)

    # -------------------movi list frame extraction-------------------
    

    # -------------------idx-------------------
    idx1_start_offset = 20 + hdrl_size + 8 + junk_size + movi_list_size
    print("idx1 start offset: ", hex(idx1_start_offset))
    idx1_size = int.from_bytes(data[idx1_start_offset+4:idx1_start_offset+8], 'little')
    # print(idx1_size)
    idx = data[idx1_start_offset:idx1_start_offset+8+idx1_size]
    # print(idx)
    
    end_time = time.time()
    print("\nrun time: ", end_time - start_time)
    print(f"memory use: {memory_usage()[0]:.2f} MiB")