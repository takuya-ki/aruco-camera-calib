import cv2
from preference import *
aruco = cv2.aruco

# 入力画像 #
import glob, os
path = "./result/*.png"
image_paths = [os.path.basename(r) for r in sorted(glob.glob('glob.glob(path)')]

for image_path in image_paths:
    path = './result/' + image_path
    checkerBoardImage = cv2.imread(path)
    
    # ChArUco マーカーを検出 #
    markerCorners, markerIds  = [0,0]
    markerCorners, markerIds, rejectedImgPoints = aruco.detectMarkers(checkerBoardImage, dictionary)

    # 検出されたマーカーをもとに，チェッカーボードを検出して，結果を描画 #
    outputImage = checkerBoardImage.copy();
    if markerIds is None:
        break
    if markerIds.size > 0:
        charucoCorners, charucoIds = [0,0]
        cv2.aruco.drawDetectedMarkers(outputImage, markerCorners, markerIds)
        # charucoCorners, charucoIds = aruco.interpolateCornersCharuco(markerCorners, markerIds, checkerBoardImage, board)
        # outputImage = aruco.drawDetectedCornersCharuco(outputImage, charucoCorners, charucoIds)

    orgHeight, orgWidth = outputImage.shape[:2]
    size = (int(orgWidth/2), int(orgHeight/2))
    halfImg = cv2.resize(outputImage, size)
    cv2.imshow("test detected image", halfImg)
    cv2.waitKey(0)