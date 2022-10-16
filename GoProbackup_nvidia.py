import os

GOPRO_PATH = 'J:/DCIM/100GOPRO'
BACKUP_PATH = 'D:/Picture/GoPro/Output2'
VIDEO_BITRATE = '20M'


def encode_h265(filename):
    cmd = ('ffmpeg -y -vsync 0 -hwaccel cuda '
          '-i ' + GOPRO_PATH + '/' + filename + ' '
          '-c:a copy -c:v hevc_nvenc -profile:v 2 -b:v ' + VIDEO_BITRATE + ' '
          '-map_metadata 0 '
          '' + BACKUP_PATH + '/' + filename + ''
           )
    os.system(cmd)

for each in os.listdir(GOPRO_PATH):
	if each.endswith(".MP4"):		
		encode_h265(each)