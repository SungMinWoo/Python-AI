#핸드트레킹 모듈 사용 예쩨
import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm

pTime = 0  # 이전시간
cTime = 0  # 현재시간
cap = cv2.VideoCapture(1)
detector = htm.handDetector()

while True:
    success, img = cap.read()
    img = detector.findHands(img, draw = False)#여기서 img는 손을 찾는거, draw = False를 하면 손가락 마디마다의 좌표 그리기 중단
    lmlist = detector.findPosition(img, draw=False)#draw=False여기서 하면 화면상 모든 좌표 표시를 지움
    if len(lmlist) != 0:
        print(lmlist[4])#뒤에 번호는 손가락의 랜드마크를 의미함 4번에 대한 렌드마크의 좌표값만 출력
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    # 현재시간에서 이전시간을 뺀 값
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    # fps표시, 좌표, 폰트설정, 3의 크기. 색 설정, 3의 두께

    cv2.imshow("image", img)
    cv2.waitKey(1)