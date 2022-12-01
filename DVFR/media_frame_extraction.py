import sys
import os
import time
import pandas as pd
from datetime import datetime
import ffmpeg
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
    check = 1   # 0: 손상, 1: 미손상
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

    # 손상 유무 판단
    if(data[0:4] != b"\x52\x49\x46\x46"):
        # 헤더, idx1 값만 날아간 경우
        print("No Signature(Magic Number)")
        movi_list_start_offset = int(data.find(b"\x6D\x6F\x76\x69")) - 8
        movi_list_size = int.from_bytes(data[movi_list_start_offset+4:movi_list_start_offset+8], 'little')
        movi = data[movi_list_start_offset:movi_list_start_offset+8+movi_list_size]
        print(hex(movi_list_start_offset))
        print(hex(movi_list_size))
        check = 0
    else:
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
    idx1_start_offset = movi_list_start_offset+8+movi_list_size
    movi_list_magic_number = []
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
    # print("idx1_start_offset: ", hex((idx1_start_offset + 8) + idx1_size))
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

    # -------------------About binary-------------------
    # about_binary = pd.DataFrame(columns=[''])

    cnt = 0
    Frame_index = 0
    h264_front = []
    h264_back = []
    h264_frame = pd.DataFrame(columns=['Frame_index', 'Channel', 'Start_Offset', 'End_Offset', 'Size'])    # sps, pps, iframe! (pframe 제외)
    h264_frame_pframe = pd.DataFrame(columns=['Frame_index', 'Channel', 'Start_offset', "End_Offset", "Size"])

    h264_frame.loc[len(h264_frame)] = ['0x00','0x00','0x00','0x00','0x00']
    h264_frame_pframe.loc[len(h264_frame_pframe)] = ['0x00','0x00','0x00','0x00','0x00']
    # print(h264_frame_pframe)


    while(1):
        # Pframe
        if(data[movi_list_pointer+8:movi_list_pointer+13] == b'\x00\x00\x00\x01\x41'):
            # pframe 데이터프레임 Endoffset 값이 sps 데이터프레임 StartOffset 값보다 작아지면 index+1
            pframe_index_check_sps = h264_frame.iloc[len(h264_frame)-1, 2]
            pframe_index_check_pframe = h264_frame_pframe.iloc[len(h264_frame_pframe)-1, 3]
            # print(int(pframe_index_check[2:], 16))
            # print(movi_list_pointer+8)
            # print(int(pframe_index_check[2:], 16))
            # print(int(pframe_index_check2[2:], 16))
            if(int(pframe_index_check_sps[2:], 16) > int(pframe_index_check_pframe[2:], 16)):
                Frame_index += 1

            frame_size = int.from_bytes(data[movi_list_pointer+4:movi_list_pointer+8], 'little')
            # print(data[movi_list_pointer+8:movi_list_pointer+13])
            if(data[movi_list_pointer:movi_list_pointer+4] == b'\x30\x30\x64\x63'): # 전방
                h264_front += data[movi_list_pointer+8:movi_list_pointer+(frame_size + 8)]
                append_dataframe = [Frame_index, '00', hex(movi_list_pointer+8), hex((movi_list_pointer + (frame_size + 8)) - 1), hex(frame_size)]    # 임시
                h264_frame_pframe.loc[len(h264_frame_pframe)] = append_dataframe

            elif(data[movi_list_pointer:movi_list_pointer+4] == b'\x30\x31\x64\x63'):   # 후방
                h264_back += data[movi_list_pointer+8:movi_list_pointer+(frame_size + 8)]
                append_dataframe = [Frame_index, '01', hex(movi_list_pointer+8), hex((movi_list_pointer + (frame_size + 8)) - 1), hex(frame_size)]    # 임시
                h264_frame_pframe.loc[len(h264_frame_pframe)] = append_dataframe

            movi_list_pointer += (frame_size + 8)
            cnt += 1
            # print(data[movi_list_pointer+8:movi_list_pointer+13])
            # time.sleep(0.5)

            continue

        elif(data[movi_list_pointer+9:movi_list_pointer+14] == b'\x00\x00\x00\x01\x41'):
            movi_list_pointer += 1
            # pframe 데이터프레임 Endoffset 값이 sps 데이터프레임 StartOffset 값보다 작아지면 index+1
            pframe_index_check_sps = h264_frame.iloc[len(h264_frame)-1, 2]
            pframe_index_check_pframe = h264_frame_pframe.iloc[len(h264_frame_pframe)-1, 3]
            # print(int(pframe_index_check[2:], 16))
            # print(movi_list_pointer+8)
            # print(int(pframe_index_check[2:], 16))
            # print(int(pframe_index_check2[2:], 16))
            if(int(pframe_index_check_sps[2:], 16) > int(pframe_index_check_pframe[2:], 16)):
                Frame_index += 1

            frame_size = int.from_bytes(data[movi_list_pointer+4:movi_list_pointer+8], 'little')
            # print(data[movi_list_pointer+8:movi_list_pointer+13])
            if(data[movi_list_pointer:movi_list_pointer+4] == b'\x30\x30\x64\x63'): # 전방
                h264_front += data[movi_list_pointer+8:movi_list_pointer+(frame_size + 8)]
                append_dataframe = [Frame_index, '00', hex(movi_list_pointer+8), hex((movi_list_pointer + (frame_size + 8)) - 1), hex(frame_size)]    # 임시
                h264_frame_pframe.loc[len(h264_frame_pframe)] = append_dataframe

            elif(data[movi_list_pointer:movi_list_pointer+4] == b'\x30\x31\x64\x63'):   # 후방
                h264_back += data[movi_list_pointer+8:movi_list_pointer+(frame_size + 8)]
                append_dataframe = [Frame_index, '01', hex(movi_list_pointer+8), hex((movi_list_pointer + (frame_size + 8)) - 1), hex(frame_size)]    # 임시
                h264_frame_pframe.loc[len(h264_frame_pframe)] = append_dataframe


            movi_list_pointer += (frame_size + 8)
            cnt += 1
            # print(data[movi_list_pointer+8:movi_list_pointer+13])
            # time.sleep(0.5)

            continue
        
        # SPS, PPS, Iframe
        if(data[movi_list_pointer:movi_list_pointer+4] == b'\x30\x30\x64\x63'):
            # print("\n전방")
            frame_size = int.from_bytes(data[movi_list_pointer+4:movi_list_pointer+8], 'little')
            # print(data[movi_list_pointer+4:movi_list_pointer+8], hex(frame_size))
            # h264_front.append(data[movi_list_pointer+8:movi_list_pointer+(frame_size + 8)])
            h264_front += data[movi_list_pointer+8:movi_list_pointer+(frame_size + 8)]
            append_dataframe = [Frame_index+1, '00', hex(movi_list_pointer+8), hex((movi_list_pointer + (frame_size + 8)) - 1), hex(frame_size)]    # 임시
            # append_dataframe = ['전방', movi_list_pointer+8, (movi_list_pointer + (frame_size + 8)) - 1, frame_size]    # 임시
            # print(append_dataframe)
            h264_frame.loc[len(h264_frame)] = append_dataframe

        elif(data[movi_list_pointer+1:movi_list_pointer+5] == b'\x30\x30\x64\x63'): # 파인뷰 전방
            movi_list_pointer += 1
            # print("\n전방")
            frame_size = int.from_bytes(data[movi_list_pointer+4:movi_list_pointer+8], 'little')
            # print(data[movi_list_pointer+4:movi_list_pointer+8], hex(frame_size))
            # h264_front.append(data[movi_list_pointer+8:movi_list_pointer+(frame_size + 8)])
            h264_front += data[movi_list_pointer+8:movi_list_pointer+(frame_size + 8)]
            append_dataframe = [Frame_index+1, '00', hex(movi_list_pointer+8), hex((movi_list_pointer + (frame_size + 8)) - 1), hex(frame_size)]    # 임시
            # append_dataframe = ['전방', movi_list_pointer+8, (movi_list_pointer + (frame_size + 8)) - 1, frame_size]    # 임시
            # print(append_dataframe)
            h264_frame.loc[len(h264_frame)] = append_dataframe

        elif(data[movi_list_pointer:movi_list_pointer+4] == b'\x30\x31\x64\x63'):
            # print("\n후방")
            frame_size = int.from_bytes(data[movi_list_pointer+4:movi_list_pointer+8], 'little')
            # print(data[movi_list_pointer+4:movi_list_pointer+8], hex(frame_size))
            # h264_back.append(data[movi_list_pointer+8:movi_list_pointer+(frame_size + 8)])
            h264_back += data[movi_list_pointer+8:movi_list_pointer+(frame_size + 8)]
            append_dataframe = [Frame_index+1, '01', hex(movi_list_pointer+8), hex((movi_list_pointer + (frame_size + 8)) - 1), hex(frame_size)]    # 임시
            # append_dataframe = ['01', movi_list_pointer+8, (movi_list_pointer + (frame_size + 8)) - 1, frame_size]    # 임시
            # print(append_dataframe)
            h264_frame.loc[len(h264_frame)] = append_dataframe

        elif(data[movi_list_pointer+1:movi_list_pointer+5] == b'\x30\x31\x64\x63'): # 파인뷰 후방
            movi_list_pointer += 1
            # print("\n후방")
            frame_size = int.from_bytes(data[movi_list_pointer+4:movi_list_pointer+8], 'little')
            # print(data[movi_list_pointer+4:movi_list_pointer+8], hex(frame_size))
            # h264_back.append(data[movi_list_pointer+8:movi_list_pointer+(frame_size + 8)])
            h264_back += data[movi_list_pointer+8:movi_list_pointer+(frame_size + 8)]
            append_dataframe = [Frame_index+1, '01', hex(movi_list_pointer+8), hex((movi_list_pointer + (frame_size + 8)) - 1), hex(frame_size)]    # 임시
            # append_dataframe = ['01', movi_list_pointer+8, (movi_list_pointer + (frame_size + 8)) - 1, frame_size]    # 임시
            # print(append_dataframe)
            h264_frame.loc[len(h264_frame)] = append_dataframe

        elif(data[movi_list_pointer:movi_list_pointer+4] == b'\x30\x33\x74\x78'):
            # print("\n텍스트")
            frame_size = int.from_bytes(data[movi_list_pointer+4:movi_list_pointer+8], 'little')
            # print(data[movi_list_pointer+4:movi_list_pointer+8], hex(frame_size))
        
        elif(data[movi_list_pointer+1:movi_list_pointer+5] == b'\x30\x33\x74\x78'): # 파인뷰 텍스트
            movi_list_pointer += 1
            # print("\n텍스트")
            frame_size = int.from_bytes(data[movi_list_pointer+4:movi_list_pointer+8], 'little')
            # print(data[movi_list_pointer+4:movi_list_pointer+8], hex(frame_size))

        elif(data[movi_list_pointer:movi_list_pointer+4] == b'\x30\x31\x77\x62'):
            # print("\n음성")
            frame_size = int.from_bytes(data[movi_list_pointer+4:movi_list_pointer+8], 'little')
            # print(data[movi_list_pointer+4:movi_list_pointer+8], hex(frame_size))

        elif(data[movi_list_pointer:movi_list_pointer+4] == b'\x30\x33\x73\x74' or data[movi_list_pointer:movi_list_pointer+4] == b'\x30\x34\x73\x74'): # 03st, 04st
            # print("\n뭔데 이거~")
            frame_size = int.from_bytes(data[movi_list_pointer+4:movi_list_pointer+8], 'little')
            # print(data[movi_list_pointer+4:movi_list_pointer+8], hex(frame_size))
            
        elif(data[movi_list_pointer:movi_list_pointer+4] == b'\x30\x32\x77\x62'):
            # print("\n뭔데 이거~2")
            frame_size = int.from_bytes(data[movi_list_pointer+4:movi_list_pointer+8], 'little')
            # print(data[movi_list_pointer+4:movi_list_pointer+8], hex(frame_size))
        
        elif(data[movi_list_pointer+1:movi_list_pointer+5] == b'\x30\x32\x77\x62'):
            movi_list_pointer += 1
            # print("\n뭔데 이거~2")
            frame_size = int.from_bytes(data[movi_list_pointer+4:movi_list_pointer+8], 'little')
            # print(data[movi_list_pointer+4:movi_list_pointer+8], hex(frame_size))
        
        # idx1 list에 있는 값들과 모두 일치할 경우
        # idx1 에서 값 파싱 -> 그걸로 data 영역에서 비교하면서 진행
        # 하다가 다른거 있으면 -> 뻑나는거임
        if(check == 0):
            if(movi_list_pointer >= idx1_start_offset):
                break
            
        else:
            if(movi_list_magic_number[cnt] != data[movi_list_pointer:movi_list_pointer+4]):
                print("\nLast movi_list_pointer: ", hex(movi_list_pointer))
                unknown_movi_list_data = data[movi_list_pointer:idx1_start_offset-1]
                unknown_movi_list_data_size = idx1_start_offset - movi_list_pointer
                if(movi_list_pointer == movi_list_pointer + unknown_movi_list_data_size-1 or movi_list_pointer == movi_list_pointer + unknown_movi_list_data_size):
                    print("\nunknown_movi_list none")
                else:
                    print("\nunknown_movi_list_data_offset: ", hex(movi_list_pointer), " ~ ", hex((movi_list_pointer + unknown_movi_list_data_size)-1))
                break

        # if(movi_list_pointer > idx1_start_offset):
        #     print("Last movi_list_pointer: ", hex(movi_list_pointer))
        #     break
        
        # print("movi_list_magic_number: ", movi_list_magic_number[cnt])
        # print("now: ", data[movi_list_pointer:movi_list_pointer+4])

        movi_list_pointer += (frame_size + 8)
        # print("movi_list_pointer: ", hex(movi_list_pointer))

        
        # if(data)
        # h264_frame.append()
        cnt+=1

    # print(len(h264_frame))
    # print(h264_frame.iloc[len(h264_frame)-1, 1])
    
    # print(type(h264_front))

    h264_frame = h264_frame.drop([0], axis=0)
    h264_frame_pframe = h264_frame_pframe.drop([0], axis=0)

    print(h264_frame)
    print(h264_frame_pframe)

    now = datetime.now()
    save_folder_name = f"{now.year}{now.month:02}{now.day:02}_{now.hour:02}{now.minute:02}{now.second:02}"

    os.makedirs(f"./result/{save_folder_name}", exist_ok=True)
    os.makedirs(f"./result/{save_folder_name}/frame/전방", exist_ok=True)
    os.makedirs(f"./result/{save_folder_name}/frame/후방", exist_ok=True)

    # 전방, 후방 영상 추출
    with open(f"./result/{save_folder_name}/front.dat", "wb") as frame:
        frame.write(bytes(h264_front))
        # print(h264_front)

    about_media = (
        ffmpeg.probe(f"./result/{save_folder_name}/front.dat")
    )

    # print(about_media)
    # print(type(about_media))
    # print(about_media['streams'][0]['time_base'])
    time_base = about_media['streams'][0]['time_base']

    save_media = (
        ffmpeg
        .input(f"./result/{save_folder_name}/front.dat")
        .output(f"./result/{save_folder_name}/front.avi", video_bitrate=int(time_base[2:])/1000)
        .run()
    )

    with open(f"./result/{save_folder_name}/back.dat", "wb") as frame:
        frame.write(bytes(h264_back))
        # print(h264_back)

    about_media = (
        ffmpeg.probe(f"./result/{save_folder_name}/back.dat")
    )

    # print(about_media)
    # print(type(about_media))
    # print(about_media['streams'][0]['time_base'])
    time_base = about_media['streams'][0]['time_base']

    save_media = (
        ffmpeg
        .input(f"./result/{save_folder_name}/back.dat")
        .output(f"./result/{save_folder_name}/back.avi", video_bitrate=int(time_base[2:])/1000)
        .run()
    )
        
    # offset csv 저장
    h264_frame.to_csv(f'./result/{save_folder_name}/offset_info.csv', encoding='CP949')
    h264_frame_pframe.to_csv(f'./result/{save_folder_name}/offset_info_pframe.csv', encoding='CP949')

    # frame 단위로 저장
    cnt_front = 0
    cnt_back = 0

    for i in range (0,len(h264_frame)):
        # print("start offset: ", hex(int(h264_frame.iloc[0, 1])), "\nend offset: ", int(h264_frame.iloc[0, 2]+1))
        # print("\n")

        if '00' in h264_frame.iloc[i, 1]:
            save_path = f"./result/{save_folder_name}/frame/전방/"
            cnt_front += 1
            with open(f"{save_path}/frame{cnt_front}.dat", "wb") as frame:
                start = h264_frame.iloc[i, 2]
                # print(start[2:])
                # print(type(start))
                end = h264_frame.iloc[i, 3]
                # bytes(data[int(start[2:], 16):int(end[2:], 16)+1])
                frame.write(bytes(data[int(start[2:], 16):int(end[2:], 16)+1]))

                (
                    ffmpeg
                    .input(f"{save_path}/frame{cnt_front}.dat")
                    .output(f"{save_path}/frame{cnt_front}.jpg")
                    .run()
                )
                
        if '01' in h264_frame.iloc[i, 1]:
            save_path = f"./result/{save_folder_name}/frame/후방/"
            cnt_back += 1
            with open(f"{save_path}/frame{cnt_back}.dat", "wb") as frame:
                start = h264_frame.iloc[i, 2]
                # print(start[2:])
                end = h264_frame.iloc[i, 3]
                # print(end[2:])
                # print(int(end[2:], 16))
                # print(int(start[2:], 16), int(end[2:], 16))
                # bytes(data[int(start[2:], 16):int(end[2:], 16)+1])
                frame.write(bytes(data[int(start[2:], 16):int(end[2:], 16)+1]))

                (
                    ffmpeg
                    .input(f"{save_path}/frame{cnt_back}.dat")
                    .output(f"{save_path}/frame{cnt_back}.jpg")
                    .run()
                )
                
    
    with open(f"./result/{save_folder_name}/unknown.dat", "wb") as frame:
        frame.write(bytes(unknown_movi_list_data))
        # print(h264_back)

    # sps, pps, iframe, pframe 파싱
    # frame_index = int(input("원하는 프레임 정보: "))
    # h264_frame_Detail = pd.DataFrame(columns=['Frame', 'Start_Offset', 'End_Offset', 'Size']) # sps, pps, iframe, pframe, size

    # start = h264_frame.iloc[frame_index, 1]
    # end = h264_frame.iloc[frame_index, 2]

    # print(bytes(data[int(start[2:], 16):int(start[2:], 16)+5]))

    # if(bytes(data[int(start[2:], 16):int(start[2:], 16)+5]) == b'\x00\x00\x00\x01\x67'):
        
    end_time = time.time()
    print("\nrun time: ", end_time - start_time)
    print(f"memory use: {memory_usage()[0]:.2f} MiB")