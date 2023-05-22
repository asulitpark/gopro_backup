import os
import win32file
from pywintypes import Time

A7M4_PATH = 'Y:/test from'
BACKUP_PATH = 'Y:/test to'
VIDEO_BITRATE = '20M'

def encode_h265(fromFile, toFile):
    cmd = ('ffmpeg -y -hwaccel cuda '
          '-i "' + fromFile + '" '
          '-vf vidstabdetect=shakiness=10 '
          '-c:v hevc_nvenc -profile:v main10 -b:v ' + VIDEO_BITRATE + ' '  
          '"' + toFile + '"'
           )
    print(cmd)
    os.system(cmd)

    cmd = ('ffmpeg -y -hwaccel cuda '
          '-i "' + fromFile + '" '
          '-vf vidstabtransform,unsharp=5:5:0.8:3:3:0.4 '
          '-c:v hevc_nvenc -profile:v main10 -b:v ' + VIDEO_BITRATE + ' '  
          '"' + toFile + '"'
           )
    print(cmd)
    os.system(cmd)

def overwriteCreateTime(fromFile, toFile):
	fromDate = os.path.getmtime(fromFile)
	os.utime(toFile, (fromDate, fromDate))

for each in os.listdir(A7M4_PATH):
	if each.endswith(".MP4"):
		fromFile = '' + A7M4_PATH + '/' + each
		toFile = '' + BACKUP_PATH + '/' + each
		encode_h265(fromFile, toFile)
		overwriteCreateTime(fromFile, toFile)
        

# encode_h265("GX010152.MP4")