import os

DRIVE="D:"
A7M4_PATH = f"{DRIVE}/test"
VIDEO_BITRATE = '20M'
VIDEO_CODEC = 'hevc_nvenc -profile:v main10'

def encode(fromFile, toFile):
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

def traverse_directories(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        print("현재 디렉토리:", dirpath)
        targetDir = dirpath.replace(f"{DRIVE}/", f"{DRIVE}/stabilization/")
        print("대상 디렉토리:", targetDir)

        # 현재 디렉토리의 파일 출력
        for each in filenames:
             if each.startswith("._") == False and each.startswith("C") and each.endswith(".MP4"):
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
        
traverse_directories(A7M4_PATH)