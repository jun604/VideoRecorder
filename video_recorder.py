import cv2 as cv
import datetime

# 1. 카메라 또는 RTSP 스트림 연결 (0은 기본 웹캠, RTSP 주소 입력 가능)
# 예: video = cv.VideoCapture('rtsp://...')
video = cv.VideoCapture('rtsp://210.99.70.120:1935/live/cctv004.stream') 

if not video.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

# 비디오 설정을 위한 정보 가져오기
fps = 30.0  # 일반적인 웹캠 FPS
width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
fourcc = cv.VideoWriter_fourcc(*'XVID') # AVI 저장을 위한 코덱

is_recording = False
out = None

print("--- 시스템 가동 ---")
print("Space: Record/Preview 모드 전환")
print("ESC: 프로그램 종료")

while True:
    valid, frame = video.read()
    if not valid:
        break

    # 화면에 표시할 복사본 생성 (원본은 깨끗하게 녹화하기 위함)
    display_frame = frame.copy()

    # 2. 모드에 따른 로직 처리
    if is_recording:
        # 녹화 중일 때: 파일에 프레임 쓰기
        if out is not None:
            out.write(frame)
        
        # [필수 기능] Record 모드 시 화면에 표시 (빨간색 원 및 텍스트)
        cv.circle(display_frame, (40, 40), 15, (0, 0, 255), -1)
        cv.putText(display_frame, "RECORDING", (70, 55), 
                   cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        # Preview 모드 시 표시
        cv.putText(display_frame, "PREVIEW", (20, 55), 
                   cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # 3. 화면에 현재 카메라 영상 표시
    cv.imshow('Camera System', display_frame)

    # 4. 키 입력 처리
    key = cv.waitKey(1)
    
    # [필수 기능] Space 키로 모드 변환 (ASCII code 32)
    if key == 32: 
        is_recording = not is_recording
        if is_recording:
            # 녹화 시작: 현재 시간을 파일명으로 생성
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'record_{timestamp}.avi'
            out = cv.VideoWriter(filename, fourcc, fps, (width, height))
            print(f"녹화 시작: {filename}")
        else:
            # 녹화 중지: VideoWriter 해제
            if out is not None:
                out.release()
                out = None
            print("녹화 중지 및 저장 완료")

    # [필수 기능] ESC 키로 종료 (ASCII code 27)
    elif key == 27:
        break

# 자원 해제
if out is not None:
    out.release()
video.release()
cv.destroyAllWindows()