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
    start_time = time.time()

    file_size = os.path.getsize(sys.argv[1])

    print('\n[*] Input_file :', sys.argv[1],' ','Size :', size_return(file_size),'\n')

    print(sys.argv[1])

    file_path = sys.argv[1]
    file_lists = os.listdir(file_path)

    Frame_index = 0

    slack_frame = pd.DataFrame(columns=['Frame_index', 'Channel', 'Start_Offset', 'End_Offset', 'Size', 'damage'])    # sps, pps, iframe! (pframe 제외)

    slack_frame.loc[len(slack_frame)] = ['0x00','0x00','0x00','0x00','0x00', '0x00']

    now = datetime.now()
    save_folder_name = f"{now.year}{now.month:02}{now.day:02}_{now.hour:02}{now.minute:02}{now.second:02}"

    os.makedirs(f"./result/{save_folder_name}", exist_ok=True)
    os.makedirs(f"./result/{save_folder_name}/frame/", exist_ok=True)
    # os.makedirs(f"./result/{save_folder_name}/frame/전방", exist_ok=True)
    # os.makedirs(f"./result/{save_folder_name}/frame/후방", exist_ok=True)
    
    for file in file_lists:
        # time.sleep(0.3)
        with open(file_path+"\\"+file, "rb") as media_file:
            data = media_file.read()
        
        iframe_offset = data.find(b"\x00\x00\x00\x01\x65")

        if (iframe_offset != -1):
            sps_offset = data.find(b"\x00\x00\x00\x01\x67")
            
            while(True):
                # print(sps_offset)
                frame_size = int.from_bytes(data[sps_offset-4:sps_offset], 'little')
                # print(hex(frame_size))

                # print(f"\nfile:{file}, sps_offset:{sps_offset}")
                # print(f"frame_size:{frame_size}")
                slack_data = data[sps_offset:sps_offset + frame_size]

                # print(f"pointer:{hex(pointer)}")

                if(slack_data.find(b"\x00\x00\x00\x01\x65") != -1):
                    print(f"\nfile: {file}")
                    print(f"frame_offset: {hex(sps_offset)}")
                    # exit(1)

                    with open(f"./result/{save_folder_name}/frame/{file}", "wb") as frame:
                        frame.write(slack_data)

                    # if(data[sps_offset-8:sps_offset-4] == b'\x30\x30\x64\x63'):   # 전방, 00dc
                    #     append_dataframe = [file, '00', hex(sps_offset), hex((sps_offset + frame_size) - 1), hex(frame_size), 'O']    # 임시
                    #     slack_frame.loc[len(slack_frame)] = append_dataframe

                    # elif(data[sps_offset-8:sps_offset-4] == b'\x30\x31\x64\x63'):   # 후방, 01dc
                    #     append_dataframe = [file, '01', hex(sps_offset), hex((sps_offset + frame_size) - 1), hex(frame_size), 'O']    # 임시
                    #     slack_frame.loc[len(slack_frame)] = append_dataframe

                    # else:
                    #     append_dataframe = [file, 'unknown', hex(sps_offset), hex((sps_offset + frame_size) - 1), hex(frame_size), 'O']    # 임시
                    #     slack_frame.loc[len(slack_frame)] = append_dataframe

                    append_dataframe = [file, 'unknown', hex(sps_offset), hex(len(data) - 1), hex(frame_size), 'O']    # 임시
                    slack_frame.loc[len(slack_frame)] = append_dataframe
                    # print(sps_offset + 1)
                    # print(data.find(b"\x00\x00\x00\x01\x67", sps_offset + 1))
                    # print(hex(len(data)))
                    # print(slack_frame.iloc[len(slack_frame) - 1, 3])
                    if(len(data) >= (sps_offset + frame_size) - 1):
                        slack_frame.iloc[len(slack_frame) - 1, 5] = "X"
                        slack_frame.iloc[len(slack_frame) - 1, 3] = hex((sps_offset + frame_size) - 1)
                    
                if(data.find(b"\x00\x00\x00\x01\x67", sps_offset + 1) == -1):
                    break

                sps_offset = data.find(b"\x00\x00\x00\x01\x67", sps_offset + 1)

                
    slack_frame = slack_frame.drop([0], axis=0)
    print(slack_frame)

    slack_frame.to_csv(f'./result/{save_folder_name}/offset_info.csv', encoding='CP949')

    file_path = f"./result/{save_folder_name}" + "/frame"
    file_lists = os.listdir(file_path)

    for file in file_lists:
        save_path = f"./result/{file}"

        (
            ffmpeg
            .input(f"{file_path}/{file}")
            .output(f"{file_path}/{file}.jpg")
            .run()
        )