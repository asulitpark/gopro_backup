import os
import subprocess

FROM_DRIVE="Y:"
TO_DRIVE="Y:"

# SOURCE_PATH = f"{DRIVE}/work/china/A7M4"
SOURCE_PATH = f"{FROM_DRIVE}/X7/X7_Raw"
# h264
# VIDEO_CODEC = '-vf "scale=1920:1080" h264_nvenc -preset p7 -b:v 5M -maxrate 6M -bufsize 10M -rc:v vbr -cq 19 -profile:v high -pix_fmt yuv420p'

# h265 with optimized VBR settings
VIDEO_CODEC = '-c:v hevc_nvenc -preset p6 -b:v 2.5M -maxrate 4M -bufsize 8M -rc vbr_hq -cq 21 -qmin 18 -qmax 28 -profile:v main10 -pix_fmt yuv420p -tune hq'
AUDIO_CODEC = '-c:a aac -b:a 128k -ar 48000'
SUBTITLE_CODEC = '-c:s copy'

def get_subtitle_file(fromFile):
    base_name = os.path.splitext(fromFile)[0]
    subtitle_extensions = ['.smi', '.srt']
    subtitle_file = None
    for ext in subtitle_extensions:
        possible_subtitle = base_name + ext  # dirpath 제거
        if os.path.exists(possible_subtitle):
            subtitle_file = possible_subtitle
            print(f"자막 파일 찾음: {subtitle_file}")
            break
    return subtitle_file

def convert_smi_to_srt(smi_file):
    """Convert SMI subtitle to SRT format"""
    try:
        srt_file = os.path.splitext(smi_file)[0] + '.srt'
        cmd = [
            'ffmpeg', '-y',
            '-sub_charenc', 'cp949',  # Specify input encoding for SMI file
            '-i', smi_file,
            srt_file
        ]
        # Specify UTF-8 for decoding ffmpeg's output to avoid UnicodeDecodeError
        subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8')
        return srt_file
    except subprocess.CalledProcessError as e:
        # Log ffmpeg's stderr for better debugging
        print(f"SMI to SRT 변환 실패: {e}")
        if e.stderr:
            print(f"ffmpeg stderr:\n{e.stderr}")
        return None

def encode(fromFile, toFile):
    # 경로 정규화 (백슬래시를 슬래시로 변환)
    fromFile = os.path.normpath(fromFile).replace('\\', '/')
    toFile = os.path.normpath(toFile).replace('\\', '/')
    
    # 출력 디렉토리 생성
    os.makedirs(os.path.dirname(toFile), exist_ok=True)
    
    subtitle_file = get_subtitle_file(fromFile)
    
    # SMI 파일이면 SRT로 변환
    if subtitle_file and subtitle_file.lower().endswith('.smi'):
        print(f"SMI 자막 파일을 SRT로 변환 중: {subtitle_file}")
        srt_file = convert_smi_to_srt(subtitle_file)
        if srt_file and os.path.exists(srt_file):
            subtitle_file = srt_file
            print(f"SRT로 변환 완료: {srt_file}")
    
    # 출력 파일명에 '_자막포함' 추가
    output_file = toFile
    if subtitle_file:
        file_name, file_ext = os.path.splitext(toFile)
        if not file_name.endswith('_자막포함'):
            output_file = f"{file_name}_자막포함{file_ext}"
    
    # 명령어 구성 (os.system 사용을 위해 파일 경로 등을 수동으로 인용 부호 처리)
    cmd = ['ffmpeg', '-y', '-i', f'"{fromFile}"']
    
    # 비디오 필터 동적 구성
    video_filters = []
    if subtitle_file and os.path.exists(subtitle_file):
        # Windows 경로의 ':' 문자를 이스케이프 처리 (e.g., C:/... -> C\\:/...)
        sub_path = os.path.normpath(subtitle_file).replace('\\', '/')
        sub_path_escaped = sub_path.replace(':', '\\\\:')
        video_filters.append(f"subtitles={sub_path_escaped}:force_style='Fontsize=32'")
        
    video_filters.append("scale=1920:1080")
    
    if video_filters:
        # 쉼표가 포함된 필터 그래프 전체를 인용 부호로 감싸기
        cmd.extend(['-vf', f'"{",".join(video_filters)}"'])

    # 비디오, 오디오 코덱 추가
    cmd.extend(VIDEO_CODEC.split())
    cmd.extend(AUDIO_CODEC.split())
    
    # 출력 파일 추가
    cmd.append(f'"{output_file}"')
    
    # 명령어 실행을 위해 리스트를 문자열로 변환
    cmd_str = ' '.join(cmd)
    print("실행 명령어:", cmd_str)
    
    # 명령어 실행 및 결과 확인 (os.system 사용)
    result = os.system(cmd_str)
    if result == 0:
        print(f"성공: {output_file} 생성 완료")
        return output_file
    else:
        print(f"오류: {output_file} 생성 실패 (에러 코드: {result})")
        return None

def overwriteCreateTime(fromFile, toFile):
    try:
        if os.path.exists(toFile) and os.path.exists(fromFile):
            fromDate = os.path.getmtime(fromFile)
            os.utime(toFile, (fromDate, fromDate))
            print(f"파일 시간 정보 복사 완료: {toFile}")
        else:
            print(f"경고: 파일을 찾을 수 없습니다 - {toFile if not os.path.exists(toFile) else fromFile}")
    except Exception as e:
        print(f"파일 시간 정보 복사 중 오류 발생: {e}")

def traverse_directories(root_dir):
    print("시작:", root_dir)
    for dirpath, dirnames, filenames in os.walk(root_dir):
        print("현재 디렉토리:", dirpath)
        targetDir = dirpath.replace(f"{FROM_DRIVE}/X7/X7_Raw", f"{TO_DRIVE}/X7/X7")
        print("대상 디렉토리:", targetDir)

        # 현재 디렉토리의 파일 출력
        for each in filenames:
            if each.startswith("._") == False and (each.lower().endswith(".mp4") or each.lower().endswith(".mkv")):
                if not os.path.exists(targetDir):
                    os.makedirs(targetDir)

                fromFile = os.path.normpath(os.path.join(dirpath, each)).replace('\\', '/')
                toFile = os.path.normpath(os.path.join(targetDir, each)).replace('\\', '/')
                
                if os.path.exists(toFile):
                    print(f"파일이 이미 존재합니다: {toFile}")
                else:
                    print(f"변환 시작: {fromFile} -> {toFile}")
                    result_file = encode(fromFile, toFile)
                    if result_file and os.path.exists(result_file):
                        overwriteCreateTime(fromFile, result_file)
                    else:
                        print(f"경고: 변환 실패 - {fromFile}")
            else:
                print(F"skip {each}")
                  
        print()

traverse_directories(SOURCE_PATH)