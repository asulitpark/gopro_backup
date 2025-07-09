import os

FROM_DRIVE="C:"
TO_DRIVE="Y:"

# SOURCE_PATH = f"{DRIVE}/work/china/A7M4"
SOURCE_PATH = f"{FROM_DRIVE}/youtube/Top 100 Songs South Korea"
# h264
# VIDEO_CODEC = '-vf "scale=1920:1080" h264_nvenc -preset p7 -b:v 5M -maxrate 6M -bufsize 10M -rc:v vbr -cq 19 -profile:v high -pix_fmt yuv420p'

# h265
VIDEO_CODEC = '-vf "scale=1920:1080" -c:v hevc_nvenc -preset p7 -b:v 5M -maxrate 6M -bufsize 10M -rc vbr -cq 24 -profile:v main10 -pix_fmt yuv420p'
AUDIO_CODEC = '-c:a aac -b:a 128k'

def encode(fromFile, toFile):
    cmd = ('ffmpeg -y '
          '-i "' + fromFile + '" '
          '' + VIDEO_CODEC + ' '  
          '' + AUDIO_CODEC + ' '  
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
        targetDir = dirpath.replace(f"{FROM_DRIVE}/", f"{TO_DRIVE}/X7/")
        print("대상 디렉토리:", targetDir)

        # 현재 디렉토리의 파일 출력
        for each in filenames:
            if each.startswith("._") == False and each.lower().endswith(".mp4"):
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
            else:
                print(F"skip {each}")
                  
        print()
        
traverse_directories(SOURCE_PATH)