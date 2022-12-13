import sys
import os
import time
import pandas as pd
from datetime import datetime
import ffmpeg
from memory_profiler import memory_usage
from math import ceil 

# python3 avi_extraction.py [복구할 영상] [복구할 영상 frame csv 파일] [복구할 영상 pframe csv 파일] [저장위치]
# 저장위치는 복구할 영상 csv 파일들이 존재하는 영역과 동일

if __name__ == '__main__':

    with open(sys.argv[1], "rb") as media_file:
        data = media_file.read()

    data_frame = pd.read_csv(sys.argv[2])
    data_pframe = pd.read_csv(sys.argv[3])

    data_frame = data_frame.drop(data_frame.columns[[0]], axis = 'columns')
    data_pframe = data_pframe.drop(data_pframe.columns[[0]], axis = 'columns')

    # print(data_frame.iloc[0])
    # print(data_pframe.iloc[0])

    frame_count = data_frame.iloc[len(data_frame)-1, 0]
    cnt = 1
    channel = data_frame['Channel'].max()

    h264_00 = []
    h264_01 = []
    h264_02 = []

    while(True):
        # print(data_frame[data_frame['Frame_index'] == cnt])
        frame = data_frame[data_frame['Frame_index'] == cnt]
        pframe = data_pframe[data_pframe['Frame_index'] == cnt]
        # print(len(frame))

        for i in range(0, len(frame)):
            if(frame.iloc[i, 1] == 1):
                start = frame.iloc[i, 2]
                end = frame.iloc[i, 3]
                h264_01 += data[int(start[2:], 16):int(end[2:], 16) + 1]
                # print("01")
            elif(frame.iloc[i, 1] == 0):
                start = frame.iloc[i, 2]
                end = frame.iloc[i, 3]
                h264_00 += data[int(start[2:], 16):int(end[2:], 16) + 1]
                # print("00")
            elif(frame.iloc[i, 1] == 2):
                start = frame.iloc[i, 2]
                end = frame.iloc[i, 3]
                h264_02 += data[int(start[2:], 16):int(end[2:], 16) + 1]
                # print("02")

        for i in range(0, len(pframe)):
            if(pframe.iloc[i, 1] == 1):
                start = pframe.iloc[i, 2]
                end = pframe.iloc[i, 3]
                h264_01 += data[int(start[2:], 16):int(end[2:], 16) + 1]
                # print("01")
            elif(pframe.iloc[i, 1] == 0):
                start = pframe.iloc[i, 2]
                end = pframe.iloc[i, 3]
                h264_00 += data[int(start[2:], 16):int(end[2:], 16) + 1]
                # print("00")
            elif(pframe.iloc[i, 1] == 2):
                start = pframe.iloc[i, 2]
                end = pframe.iloc[i, 3]
                h264_02 += data[int(start[2:], 16):int(end[2:], 16) + 1]
                # print("02")

        cnt += 1
        if(frame_count < cnt):
            break

    save_folder_name = sys.argv[4]

    with open(f"{save_folder_name}/00.dat", "wb") as file:
        file.write(bytes(h264_00))

    about_media = (
        ffmpeg.probe(f"{save_folder_name}/00.dat")
    )

    time_base = about_media['streams'][0]['time_base']


    save_media = (
        ffmpeg
        .input(f"{save_folder_name}/00.dat")
        .output(f"{save_folder_name}/00.avi", video_bitrate=int(time_base[2:]))
        .run(overwrite_output=True)
    )

    if (channel >= 1):
        with open(f"{save_folder_name}/01.dat", "wb") as file:
            file.write(bytes(h264_01))

        about_media = (
            ffmpeg.probe(f"{save_folder_name}/01.dat")
        )

        time_base = about_media['streams'][0]['time_base']

        save_media = (
            ffmpeg
            .input(f"{save_folder_name}/01.dat")
            .output(f"{save_folder_name}/01.avi", video_bitrate=int(time_base[2:]))
            .run(overwrite_output=True)
        )
    if (channel >= 2):
        with open(f"{save_folder_name}/02.dat", "wb") as file:
            file.write(bytes(h264_02))

        about_media = (
            ffmpeg.probe(f"{save_folder_name}/02.dat")
        )

        time_base = about_media['streams'][0]['time_base']

        save_media = (
            ffmpeg
            .input(f"{save_folder_name}/02.dat")
            .output(f"{save_folder_name}/02.avi", video_bitrate=int(time_base[2:]))
            .run(overwrite_output=True)
        )