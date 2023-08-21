import os

A7M4_PATH = 'Y:/A7M4/CLIP'
BACKUP_PATH = 'Y:/A7M4/Video'
VIDEO_BITRATE = '20M'
# VIDEO_CODEC = 'hevc_nvenc -profile:v main10'
VIDEO_CODEC = 'h264_nvenc -profile:v high'

def encode_h265(fromFile, toFile):
    cmd = ('ffmpeg -y -hwaccel cuda '
          '-i "' + fromFile + '" '
          '-vf vidstabdetect=shakiness=10 '
          '-c:v ' + VIDEO_CODEC + ' -b:v ' + VIDEO_BITRATE + ' '  
          '-f null -'
           )
    print(cmd)
    os.system(cmd)

    cmd = ('ffmpeg -y -hwaccel cuda '
          '-i "' + fromFile + '" '
          '-vf vidstabtransform,unsharp=5:5:0.8:3:3:0.4 '
          '-c:v ' + VIDEO_CODEC + ' -b:v ' + VIDEO_BITRATE + ' '  
          '"' + toFile + '"'
           )
    print(cmd)
    os.system(cmd)

def overwriteCreateTime(fromFile, toFile):
	fromDate = os.path.getmtime(fromFile)
	os.utime(toFile, (fromDate, fromDate))

for each in os.listdir(A7M4_PATH):
	if each.startswith("._") == False and each.startswith("C") and each.endswith(".MP4"):
		fromFile = '' + A7M4_PATH + '/' + each
		toFile = '' + BACKUP_PATH + '/' + each
		encode_h265(fromFile, toFile)
		overwriteCreateTime(fromFile, toFile)
        

# encode_h265("GX010152.MP4")