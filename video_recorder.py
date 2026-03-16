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
plain_font = cv.FONT_HERSHEY_SIMPLEX

is_recording = False
is_paused = False
out = None
is_explained_list = [False, False, False]  # 설명 메시지 표시 여부를 추적하는 리스트
is_explained = True
is_start = False

def PutText_VideoCenter(frame, text, font=plain_font, scale=1, color=(255, 255, 255), thickness=2):
    (height, width) = frame.shape[:2]
    (text_width, text_height), _ = cv.getTextSize(text, font, scale, thickness)
    text_x = (width - text_width) // 2
    text_y = (height + text_height) // 2
    cv.putText(frame, text, (text_x, text_y), font, scale, (0, 0, 0), thickness+1) # 테두리 효과
    cv.putText(frame, text, (text_x, text_y), font, scale, color, thickness)

def PutText_VideoCenter_During(frame, text, start_time, duration=2, font=plain_font, scale=1, color=(255, 255, 255), thickness=2):
    current_time = datetime.datetime.now()
    if duration == -1:  # duration이 -1이면 무한히 표시
        PutText_VideoCenter(frame, text, font, scale, color, thickness)
    elif (current_time - start_time).total_seconds() < duration:
        PutText_VideoCenter(frame, text, font, scale, color, thickness)
        return False  # 메시지 표시 중
    else:
        return True  # 메시지 표시 완료
    

print("--- 시스템 가동 ---")
print("Space: Record/Preview 모드 전환")
print("P: 일시정지/재개, ESC: 프로그램 종료")

out_recorder = cv.VideoWriter("Play_Video_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".avi", fourcc, 120.0, (width, height))

while True:
    valid, frame = video.read()
    if not valid:
        break

    # 화면에 표시할 복사본 생성 (원본은 깨끗하게 녹화하기 위함)
    display_frame = frame.copy()
    out_recorder.write(display_frame)

    if is_explained_list is not [True, True, True]:
        if not is_explained_list[0]:
            if not is_start:
                start_time = datetime.datetime.now()
                is_start = not is_start
            is_explained_list[0] = PutText_VideoCenter_During(display_frame, "--- System Running ---", start_time)
        elif not is_explained_list[1]:
            if is_start:
                start_time = datetime.datetime.now()
                is_start = not is_start
            is_explained_list[1] = PutText_VideoCenter_During(display_frame, "Space: Record/Preview Switch", start_time)
        elif not is_explained_list[2]:
            if not is_start:
                start_time = datetime.datetime.now()
                is_start = not is_start
            is_explained_list[2] = PutText_VideoCenter_During(display_frame, "P: Pause/Resume, ESC: Exit", start_time)
            if is_explained_list[2]:
                is_start = False

    # 2. 모드에 따른 로직 처리
    if is_recording and not is_paused:
        # 녹화 중일 때: 파일에 프레임 쓰기
        if out is not None:
            out.write(frame)
        
        # [필수 기능] Record 모드 시 화면에 표시 (빨간색 원 및 텍스트)
        cv.circle(display_frame, (40, 40), 15, (0, 0, 255), -1)
        cv.putText(display_frame, "RECORDING", (70, 55), 
                   plain_font, 1, (255, 255, 0), 3) # 텍스트에 테두리 효과 추가
        cv.putText(display_frame, "RECORDING", (70, 55), 
                   plain_font, 1, (0, 0, 255), 2)
        if not is_explained:
            if not is_start:
                start_time = datetime.datetime.now()
                is_start = not is_start
            is_explained = PutText_VideoCenter_During(display_frame, "Recording Start", start_time)

    elif is_paused and is_recording:
        # 일시정지 모드 시 표시 (노란색 원 및 텍스트)
        cv.circle(display_frame, (40, 40), 15, (0, 255, 255), -1)
        cv.putText(display_frame, "PAUSED", (70, 55), 
                   plain_font, 1, (255, 0, 0), 3) # 텍스트에 테두리 효과 추가
        cv.putText(display_frame, "PAUSED", (70, 55), 
                   plain_font, 1, (0, 255, 255), 2)
        PutText_VideoCenter_During(display_frame, "Recording Stopped", 0, -1)  # 일시정지 메시지는 무한히 표시


    else:
        # Preview 모드 시 표시
        cv.rectangle(display_frame, (25, 25), (55, 55), (255, 255, 255), -1)
        cv.putText(display_frame, "PREVIEW", (70, 55),
                     plain_font, 1, (0, 0, 0), 3) # 텍스트에 테두리 효과 추가
        cv.putText(display_frame, "PREVIEW", (70, 55), 
                   plain_font, 1, (255, 255, 255), 2)
        if not is_explained:
            if not is_start:
                start_time = datetime.datetime.now()
                is_start = not is_start
            is_explained = PutText_VideoCenter_During(display_frame, "Recording Ended", start_time)
        
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
            is_paused = False
            print("녹화 중지 및 저장 완료")
        is_explained_list = [True, True, True]  # 설명 메시지 초기화
        is_explained = False
        is_start = False
    
    elif key == ord('p'):
        if is_recording:
            is_paused = not is_paused
            if is_paused:
                print("녹화 일시정지")
            else:            
                print("녹화 재개")
            is_explained_list = [True, True, True]  # 설명 메시지 초기화
            is_explained = False
            is_start = False

    # [필수 기능] ESC 키로 종료 (ASCII code 27)
    elif key == 27:
        break

# 자원 해제
if out_recorder is not None:
    out_recorder.release()
if out is not None:
    out.release()
video.release()
cv.destroyAllWindows()