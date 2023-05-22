import os

GOPRO_PATH = 'J:/DCIM/100GOPRO'
BACKUP_PATH = 'Y:/GoPro'
VIDEO_BITRATE = '20M'


def encode_h265(fromFile, toFile):
    cmd = ('ffmpeg -y -hwaccel cuda '
          '-i "' + fromFile + '" '
          # audio codec
          '-c:a copy ' 
          # video codec
          '-c:v hevc_nvenc -profile:v main10 -b:v ' + VIDEO_BITRATE + ' '  
          # meta data
          '-map_metadata 0 '
          '"' + toFile + '"'
           )
    print(cmd)
    os.system(cmd)

def overwriteCreateTime(fromFile, toFile):
	fromDate = os.path.getmtime(fromFile)
	os.utime(toFile, (fromDate, fromDate))
	
for each in os.listdir(GOPRO_PATH):
	if each.endswith(".MP4"):
		fromFile = '' + GOPRO_PATH + '/' + each
		toFile = '' + BACKUP_PATH + '/' + each
		encode_h265(fromFile, toFile)
		overwriteCreateTime(fromFile, toFile)

# encode_h265("GX010152.MP4")