import os

GOPRO_PATH = 'J:/DCIM/100GOPRO'
BACKUP_PATH = 'D:/Picture/GoPro/Output2'
VIDEO_BITRATE = '20M'


def encode_h265(filename):
    cmd = ('ffmpeg -y -hwaccel cuda '
          '-i ' + GOPRO_PATH + '/' + filename + ' '
          # audio codec
          '-c:a copy ' 
          # video codec
          '-c:v hevc_nvenc -profile:v main10 -b:v ' + VIDEO_BITRATE + ' '  
          '-map_metadata 0 ' # meta data
          '' + BACKUP_PATH + '/' + filename + ''
           )
    print(cmd)
    os.system(cmd)

for each in os.listdir(GOPRO_PATH):
	if each.endswith(".MP4"):		
		encode_h265(each)

# encode_h265("GX010152.MP4")