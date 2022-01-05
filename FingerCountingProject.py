import cv2
import time
import os
import HandTrackingModule as htm

wCam, hCam = 640, 480

cap = cv2.VideoCapture(1)
cap.set(3, wCam) #3은 너비를 의미
cap.set(4, hCam) #4는 높이를 의미

folderPath = "FingerImages" #폴더 경로
myList = os.listdir(folderPath) #폴더 안의 리스르틑 가져옴
print(myList)
overlayList = []
for imPath in myList: #이미지 목록
    image = cv2.imread(f'{folderPath}/{imPath}') #이미지를 쓸 수 있도록 함
    print(f'{folderPath}/{imPath}')
    overlayList.append(image)
pTime = 0

detecteor = htm.handDetector(detectionCon=0.75) #핸드트레킹 모듈 사용
#0.75검출 감도를 높힘

tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = detecteor.findHands(img) #손가락 이미지 반환
    lmlist = detecteor.findPosition(img, draw=False) #손가락 특정 좌표를 출력

    if len(lmlist) != 0: #좌표가 있다면
        fingers = []
        #엄지
        if lmlist[tipIds[0]][1] < lmlist[tipIds[0] - 1][1]: #1은 x좌표를 뜻하고 2는 y좌표를 뜻함
            fingers.append(1) #엄지의 구조상 좌표가 엄지 끝좌표보다 아래로 위치하기 힘들기 때문에 x축 기준으로 왼쪽 오른쪽으로 판단
        else:
            fingers.append(0)
        #나머지 손가락
        for id in range(1, 5):
            if lmlist[tipIds[id]][2] < lmlist[tipIds[id]-2][2]: #8번 좌표가 6보다 작으면 손가락이 펴져있다. 위의 값이 더 낮음
                fingers.append(1) #손가락이 펼쳐있으면 1 아니면 0
            else:
                fingers.append(0)

        print(fingers)
        totalFingers = fingers.count(1) #fingers안에 숫자 1이 몇개인지 새줌

        h, w, c = overlayList[totalFingers-1].shape
        img[0:h, 0:w] = overlayList[totalFingers-1] #사진 크기 픽셀수가 맞아야함 앞의 0은 위치정보
        #totalFingers를 해도 6.jpg가 출력되는 이유는 파이썬에서 값이 0에서 또 빼지면 마지막 요소를 가리킨다.

        cv2.rectangle(img,(20, 255), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (255,0,0), 25)
        #손가락을 갑지할때마다 출력됨

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400,70), cv2.FONT_HERSHEY_PLAIN,
                3,(255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1) #1밀리초 지연