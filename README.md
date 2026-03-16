# Video Recorder
OpenCV를 이용하여 영상을 녹화하는 Video Recorder
## 기능
1. 화면에 현재 카메라 영상 표시
   - 본 recorder는 "충청남도 천안시 동남구 신부동 433-4"에 위치한 천안로사거리 cctv를 사용
2. 동영상 파일 저장
   - OpenCV의 cv.VideoWriter를 이용
   - 깔끔한 카메라 영상만을 저장 ("record_날짜_시간.avi"로 저장)
   - recorder 시작부터 종료까지의 출력 화면을 저장 ("Play_Video_날짜_시간.avi"로 저장)
3. Preview, Record, Pause 모드
   - Preview 모드 시 화면에 하얀색 정사각형 표시</br>
     녹화 대기 상태
   - Record 모드 시 화면에 빨간색 원 표시</br>
     현재 카메라 영상 녹화
   - Pause 모드 시 화면에 노란색 원 표시</br>
     이후 녹화하는 영상을 지금까지 녹화한 영상 마지막에 추가
   - Space 키 입력 시 Preview/Record 모드, Preview/Pause 모드 전환
   - 'P' 키 입력 시 Record/Pause 모드 전환
   - ESC 키 입력 시 프로그램 종료
4. 화면에 recorder 설명 표시
   - recoder 시작 시 조작 방법 각 '2'초간 출력</br>
     설명 무시하고 녹화 시작 시 설명 제거
   - Record 모드 시작 : "Recording Start" '2'초간 출력
   - Pause 모드 시작 : Pause 모드 종료 전까지 "Recording Stopped" 출력
   - 다른 모드에서 Preview 모드로 전환 시 : "Recording ended" '2'초간 출력
