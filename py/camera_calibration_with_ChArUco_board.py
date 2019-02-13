import numpy as np
np.set_printoptions(precision=3)

from preference import *

import cv2
aruco = cv2.aruco

def showCalibrationResult(calibret):
    print("####################")
    retval, cameraMatrix, distCoeffs, rvecs, tvecs, stdDeviationsInstrinsics, stdDeviationsExtrinsics, perViewErrors = calibret
    print("Final re-projection error : \n", retval)
    print("Camera matrix : \n", cameraMatrix)
    print("vector of distortion coefficients : \n", distCoeffs)
    print("vector of rotation vectors (see Rodrigues) : \n", rvecs)
    print("vector of translation vectors : \n", tvecs)
    print("vector of standard deviations estimated for intrinsic parameters : \n", stdDeviationsInstrinsics)
    print("vector of standard deviations estimated for extrinsic parameters : \n", stdDeviationsExtrinsics)
    print("vector of average re-projection errors : \n", perViewErrors)

img = board.draw((200*5, 200*8))

# Load all the captured images
import glob, os
image_paths = [os.path.basename(r) for r in glob.glob(calibration_image_path+"*."+image_format)]
# print(image_paths)

calibImages = []

for image_path in image_paths:
    path = calibration_image_path + image_path
    calibImage = cv2.imread(path)
    # print(calibImage)

    if calibImage is None:
        break

    calibImages.append(calibImage)

imgSize = calibImages[0].shape[:2]
print(imgSize)

allCharucoCorners = []
allCharucoIds = []
charucoCorners, charucoIds = [0,0]
# cameraMat, distCoeffs, rvecs, tvecs, stdDeviationsInstrinsics, stdDeviationsExtrinsics, perViewErrors = [0, 0, 0, 0, 0 ,0 ,0]
# Detect intersection of the checker board called ChArUco
for calImg in calibImages:
    # print(calImg)
    # cv2.imshow("read image", calImg)
    # cv2.waitKey(0)
    # Find ArUco markers
    res = aruco.detectMarkers(calImg, dictionary)
    # Find ChArUco corners
    if len(res[0])>0:
        res2 = cv2.aruco.interpolateCornersCharuco(res[0], res[1], calImg, board)
        if res2[1] is not None and res2[2] is not None and len(res2[1])>3:
            allCharucoCorners.append(res2[1])
            allCharucoIds.append(res2[2])

        cv2.aruco.drawDetectedMarkers(calImg,res[0],res[1])
    img = cv2.resize(calImg, None, fx=0.5, fy=0.5)
    cv2.imshow('calibration image',img)
    cv2.waitKey(0)

cv2.destroyAllWindows()
# Calibration and output the errors
try:
    cal = cv2.aruco.calibrateCameraCharucoExtended(allCharucoCorners,allCharucoIds,board,imgSize,None,None)
    # print(cal)
except:
    print("can not calibrate ...")

showCalibrationResult(cal)
retval, cameraMatrix, distCoeffs, rvecs, tvecs, stdDeviationsInstrinsics, stdDeviationsExtrinsics, perViewErrors = cal

tmp = [cameraMatrix, distCoeffs, rvecs, tvecs, stdDeviationsInstrinsics, stdDeviationsExtrinsics]

# Save the camera parameters
import pickle

with open(fname+'.pkl', mode='wb') as f:
    pickle.dump(tmp, f, protocol=2)
