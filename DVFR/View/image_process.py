from PyQt5.QtCore import *   
import os, csv

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
            os.makedirs(self.path + '/frame_image_front', exist_ok=True)
            os.makedirs(self.path + '/frame_image_back', exist_ok=True)

            for row in reader:
                #print(row)
                output_file=open(self.path + '/frame_offset/'+str(row[3]),"wb")
                output_file.write(data[int(row[3], 16):int(row[4], 16)])

                if(row[2] == '00'):
                    os.system("ffmpeg -i {}/frame_offset/{} {}/frame_image_front/{}.jpg".format(self.path, row[3], self.path, row[3]))
                else:
                    os.system("ffmpeg -i {}/frame_offset/{} {}/frame_image_back/{}.jpg".format(self.path, row[3], self.path, row[3]))

        self.create_image.emit()

