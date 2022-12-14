from PyQt5.QtCore import *   
import os, csv, ffmpeg

class image_process(QThread): 
    create_image = pyqtSignal()

   
    def __init__(self, input_data, path):
        # main에서 받은 self 인자를 parent로 생성
        super().__init__()
        self.input_data = input_data
        self.path = path

    @pyqtSlot()
    def run(self):  

        file = open(self.input_data, 'rb')
        data = file.read() 
        
        with open(self.path + '/offset_info.csv', 'rt') as f:
            reader = csv.reader(f)
            next(reader, None)  # skip the header

            os.makedirs(self.path + '/frame_offset', exist_ok=True)

            for row in reader:
                output_file=open(self.path + '/frame_offset/'+str(row[3]),"wb")
                output_file.write(data[int(row[3], 16):int(row[4], 16)])

                if(row[2] == '00'):
                    os.makedirs(self.path + '/frame_image_00', exist_ok=True) 
                    #os.system("ffmpeg -loglevel quiet -i {}/frame_offset/{} {}/frame_image_front/{}.jpg".format(self.path, row[3], self.path, row[3]))
                    (
                        ffmpeg
                        .input(f"{self.path}/frame_offset/{row[3]}")
                        .output(f"{self.path}/frame_image_00/{row[3]}.jpg")
                        .run()
                    )

                elif(row[2] == '01'):
                    os.makedirs(self.path + '/frame_image_01', exist_ok=True)
                    #os.system("ffmpeg -loglevel quiet -i {}/frame_offset/{} {}/frame_image_back/{}.jpg".format(self.path, row[3], self.path, row[3]))
                    (
                        ffmpeg
                        .input(f"{self.path}/frame_offset/{row[3]}")
                        .output(f"{self.path}/frame_image_01/{row[3]}.jpg")
                        .run()
                    )
                else:
                    os.makedirs(self.path + '/frame_image_02', exist_ok=True) 
                    #os.system("ffmpeg -loglevel quiet -i {}/frame_offset/{} {}/frame_image_back/{}.jpg".format(self.path, row[3], self.path, row[3]))
                    (
                        ffmpeg
                        .input(f"{self.path}/frame_offset/{row[3]}")
                        .output(f"{self.path}/frame_image_02/{row[3]}.jpg")
                        .run()
                    )

        self.create_image.emit()

