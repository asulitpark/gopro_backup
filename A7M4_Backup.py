import os
import win32file

GOPRO_PATH = 'J:/DCIM/100GOPRO'
BACKUP_PATH = 'Y:/GoPro'
VIDEO_BITRATE = '20M'


def encode_h265(filename):
    cmd = ('ffmpeg -y -hwaccel cuda '
          '-i ' + GOPRO_PATH + '/' + filename + ' '
          # audio codec
          '-c:a copy ' 
          # video codec
          '-c:v hevc_nvenc -profile:v main10 -b:v ' + VIDEO_BITRATE + ' '  
          # meta data
          '-map_metadata 0 '
          '' + BACKUP_PATH + '/' + filename + ''
           )
    print(cmd)
    os.system(cmd)
    os.path.

for each in os.listdir(GOPRO_PATH):
	if each.endswith(".MP4"):		
		encode_h265(each)

# encode_h265("GX010152.MP4")