import os

DRIVE="Y:"

DIR_NAME="DJIAction5"
SOURCE_PATH = f"{DRIVE}/work/{DIR_NAME}"
VIDEO_BITRATE = '20M'
VIDEO_CODEC = 'hevc_nvenc -profile:v main10'

def encode(fromFile, toFile):
    cmd = ('ffmpeg -y -hwaccel cuda '
          '-i "' + fromFile + '" '
          # audio codec
          '-c:a copy ' 
          # video codec
          '-c:v hevc_nvenc '  
          '-pix_fmt p010le -profile:v main10 '
          '-preset p7 -tune hq '
          # '-rc vbr_hq -b:v ' + VIDEO_BITRATE + ' -maxrate ' + MAX_VIDEO_BITRATE + ' -bufsize ' + MAX_VIDEO_BITRATE + ' '
          '-rc vbr_hq -cq 17 -b:v 0 -maxrate 0 '
          '-g 300 -keyint_min 60 '
          '-spatial_aq 1 -aq-strength 10 '
          '-rc-lookahead 32 '
          # meta data
          '-map_metadata 0 '
          '"' + toFile + '"'
           )
    print(cmd)
    os.system(cmd)

def overwriteCreateTime(fromFile, toFile):
	fromDate = os.path.getmtime(fromFile)
	os.utime(toFile, (fromDate, fromDate))

def traverse_directories(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirpath = dirpath.replace("\\", "/")
        print("현재 디렉토리:", dirpath)
        targetDir = dirpath.replace(f"{DRIVE}/", f"{DRIVE}/{DIR_NAME}/")
        print("대상 디렉토리:", targetDir)

        # 현재 디렉토리의 파일 출력
        for each in filenames:
             if each.startswith("._") == False and each.startswith("D") and each.endswith(".MP4"):
                if not os.path.exists(targetDir):
                    os.makedirs(targetDir)

                fromFile = '' + dirpath + '/' + each
                toFile = '' + targetDir + '/' + each
                if os.path.exists(toFile):
                     print('' + toFile + '이 존재합니다.')
                else:
                    print("from: " + fromFile + ", to:" + toFile)
                    encode(fromFile, toFile)
                    overwriteCreateTime(fromFile, toFile)
                  
        print()
        
traverse_directories(SOURCE_PATH)