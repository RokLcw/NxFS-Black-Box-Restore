import sys
import os
import time
import pandas as pd
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
        print("Junk Size: ", hex(junk_size))
        # print(check_list_size+20)
        # print(junk_size)
        Junk = data[check_list_size + 20:((check_list_size + 20) + 8) + junk_size]
        # print("Junk: ", Junk)
        # print(Junk)
        # print(int.from_bytes(data[check_list_size + 24:check_list_size + 28], 'little'))
        junk_size += 8  # junk가 있는경우 movi start offset을 계산하기 위함.
        print("Junk Size: ", hex(junk_size))

    # -------------------movi list -------------------
    movi_list_start_offset = 20 + hdrl_size + junk_size
    print("movi list start offset: ", hex(movi_list_start_offset))
    movi_list_size = int.from_bytes(data[movi_list_start_offset+4:movi_list_start_offset+8], 'little')
    # print(movi_list_size)
    movi = data[movi_list_start_offset:movi_list_start_offset+8+movi_list_size]
    
    # with open("movi", "ab") as f:
    #     f.write(movi)

    # print(movi_list_start_offset+movi_list_size)

    # -------------------idx-------------------
    movi_list_magic_number = []
    idx1_start_offset = 20 + hdrl_size + 8 + junk_size + movi_list_size
    idx1_list_pointer = idx1_start_offset + 8
    print("\nidx1 start offset: ", hex(idx1_start_offset))
    idx1_size = int.from_bytes(data[idx1_start_offset+4:idx1_start_offset+8], 'little')
    # print("idx1_size: ", idx1_size)
    idx = data[idx1_start_offset:idx1_start_offset+8+idx1_size]
    # print("idx1_list_pointer: ", hex(idx1_list_pointer))
    # print(hex((idx1_start_offset + 8) + idx1_size))
    while((idx1_start_offset + 8) + idx1_size != idx1_list_pointer):
        # print(data[idx1_list_pointer:idx1_list_pointer+4])
        # print(hex(idx1_list_pointer))
        movi_list_magic_number.append(data[idx1_list_pointer:idx1_list_pointer+4])
        # print(data[idx1_list_pointer:idx1_list_pointer+4])
        idx1_list_pointer += (12 + 4)   # 14: 간격, 4: magic number
        # print("idx1_list_pointer: ", hex(idx1_list_pointer))
    # print(movi_list_magic_number)
    movi_list_magic_number.append("\x00\x00\x00\x00")
    print("idx1_start_offset: ", hex((idx1_start_offset + 8) + idx1_size))
    print("idx1_list_pointer: ", hex(idx1_list_pointer))
    # print(idx)
    # -------------------movi list frame extraction-------------------

    # -------------------movi list header-------------------
    movi_list_head = []
    movi_list_head_len = 0
    move_loc = 0
    while(1):
        if(movi[move_loc:move_loc+4] == b'\x30\x30\x64\x63' or movi[move_loc:move_loc+4] == b'\x30\x31\x64\x63'
        or movi[move_loc:move_loc+4] == b'\x30\x33\x73\x74' or movi[move_loc:move_loc+4] == b'\x30\x34\x73\x74'):
            break
        movi_list_head_len += len(movi[move_loc:move_loc+4])
        if (move_loc >= 16):
            movi_list_head[3] = movi_list_head[3] + movi[move_loc:move_loc+4]
            move_loc += 4
            continue
        movi_list_head.append(movi[move_loc:move_loc+4])
        move_loc += 4
    print("\nmovi_list_head: ", movi_list_head)

    # -------------------media(video, sound etc)-------------------
    media_start_offset = movi_list_start_offset + movi_list_head_len
    movi_list_pointer = media_start_offset
    print("\nmedia_start_offset: ", hex(media_start_offset))

    cnt = 0
    h264_front = []
    h264_back = []
    h264_frame = pd.DataFrame(columns=['Channel', 'Start_Offset', 'End_Offset', 'Size'])    # sps, pps, iframe! (pframe 제외)

    while(movi_list_pointer != idx1_start_offset):
        # if(cnt == 4):
        #     break
        
        if(data[movi_list_pointer:movi_list_pointer+4] == b'\x30\x30\x64\x63'):
            print("\n전방")
            frame_size = int.from_bytes(data[movi_list_pointer+4:movi_list_pointer+8], 'little')
            print(data[movi_list_pointer+4:movi_list_pointer+8], hex(frame_size))
            # h264_front.append(data[movi_list_pointer+8:movi_list_pointer+(frame_size + 8)])
            h264_front += data[movi_list_pointer+8:movi_list_pointer+(frame_size + 8)]
            # append_dataframe = ['전방', hex(movi_list_pointer+8), hex((movi_list_pointer + (frame_size + 8)) - 1), hex(frame_size)]    # 임시
            append_dataframe = ['전방', movi_list_pointer+8, (movi_list_pointer + (frame_size + 8)) - 1, frame_size]    # 임시
            print(append_dataframe)
            h264_frame.loc[len(h264_frame)] = append_dataframe

        elif(data[movi_list_pointer:movi_list_pointer+4] == b'\x30\x31\x64\x63'):
            print("\n후방")
            frame_size = int.from_bytes(data[movi_list_pointer+4:movi_list_pointer+8], 'little')
            print(data[movi_list_pointer+4:movi_list_pointer+8], hex(frame_size))
            # h264_back.append(data[movi_list_pointer+8:movi_list_pointer+(frame_size + 8)])
            h264_back += data[movi_list_pointer+8:movi_list_pointer+(frame_size + 8)]
            # append_dataframe = ['후방', hex(movi_list_pointer+8), hex((movi_list_pointer + (frame_size + 8)) - 1), hex(frame_size)]    # 임시
            append_dataframe = ['후방', movi_list_pointer+8, (movi_list_pointer + (frame_size + 8)) - 1, frame_size]    # 임시
            print(append_dataframe)
            h264_frame.loc[len(h264_frame)] = append_dataframe
            

        elif(data[movi_list_pointer:movi_list_pointer+4] == b'\x30\x33\x74\x78'):
            print("\n텍스트")
            frame_size = int.from_bytes(data[movi_list_pointer+4:movi_list_pointer+8], 'little')
            print(data[movi_list_pointer+4:movi_list_pointer+8], hex(frame_size))

        elif(data[movi_list_pointer:movi_list_pointer+4] == b'\x30\x31\x77\x62'):
            print("\n음성")
            frame_size = int.from_bytes(data[movi_list_pointer+4:movi_list_pointer+8], 'little')
            print(data[movi_list_pointer+4:movi_list_pointer+8], hex(frame_size))

        elif(data[movi_list_pointer:movi_list_pointer+4] == b'\x30\x33\x73\x74' or data[movi_list_pointer:movi_list_pointer+4] == b'\x30\x34\x73\x74'): # 03st, 04st
            print("\n뭔데 이거~")
            frame_size = int.from_bytes(data[movi_list_pointer+4:movi_list_pointer+8], 'little')
            print(data[movi_list_pointer+4:movi_list_pointer+8], hex(frame_size))
            
        elif(data[movi_list_pointer:movi_list_pointer+4] == b'\x30\x32\x77\x62'):
            print("\n뭔데 이거~2")
            frame_size = int.from_bytes(data[movi_list_pointer+4:movi_list_pointer+8], 'little')
            print(data[movi_list_pointer+4:movi_list_pointer+8], hex(frame_size))
        
        # idx1 list에 있는 값들과 모두 일치할 경우
        # idx1 에서 값 파싱 -> 그걸로 data 영역에서 비교하면서 진행
        # 하다가 다른거 있으면 -> 뻑나는거임
        if(movi_list_magic_number[cnt] != data[movi_list_pointer:movi_list_pointer+4]):
            print("\nLast movi_list_pointer: ", hex(movi_list_pointer))
            unknown_movi_list_data = data[movi_list_pointer:idx1_start_offset-1]
            unknown_movi_list_data_size = idx1_start_offset - movi_list_pointer
            print("\nunknown_movi_list_data_offset: ", hex(movi_list_pointer), " ~ ", hex((movi_list_pointer + unknown_movi_list_data_size)-1))
            break

        # if(movi_list_pointer > idx1_start_offset):
        #     print("Last movi_list_pointer: ", hex(movi_list_pointer))
        #     break
        
        print("movi_list_magic_number: ", movi_list_magic_number[cnt])
        print("now: ", data[movi_list_pointer:movi_list_pointer+4])

        movi_list_pointer += (frame_size + 8)
        print("movi_list_pointer: ", hex(movi_list_pointer))

            
        # if(data)
        # h264_frame.append()
        cnt+=1
    
    print(type(h264_front))
    print(h264_frame)

    with open("./result/front.dat", "wb") as frame:
        frame.write(bytes(h264_front))
        # print(h264_front)

    with open("./result/back.dat", "wb") as frame:
        frame.write(bytes(h264_back))
        # print(h264_back)

    h264_frame.to_csv('./result/offset_info.csv', encoding='CP949')

    print(h264_frame.iloc[0, 1])

    cnt_front = 0
    cnt_back = 0
    for i in range (0,len(h264_frame)):
        print("start offset: ", hex(int(h264_frame.iloc[0, 1])), "\nend offset: ", int(h264_frame.iloc[0, 2]+1))
        print("\n")

        if '전방' in h264_frame.iloc[i, 0]:
            save_path = f"./result/frame/전방/"
            cnt_front += 1
            with open(f"{save_path}/frame{cnt_front}.dat", "wb") as frame:
                frame.write(bytes(data[int(h264_frame.iloc[i, 1]):int(h264_frame.iloc[i, 2]+1)]))
                
        if '후방' in h264_frame.iloc[i, 0]:
            save_path = f"./result/frame/후방/"
            cnt_back += 1
            with open(f"{save_path}/frame{cnt_back}.dat", "wb") as frame:
                frame.write(bytes(data[int(h264_frame.iloc[i, 1]):int(h264_frame.iloc[i, 2]+1)]))
    
    # with open("./result/unknown.dat", "wb") as frame:
    #     frame.write(bytes(unknown_movi_list_data))
    #     # print(h264_back)

    end_time = time.time()
    print("\nrun time: ", end_time - start_time)
    print(f"memory use: {memory_usage()[0]:.2f} MiB")