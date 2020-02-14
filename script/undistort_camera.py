import cv2
from preference import *

# カメラパラメータの読み込み
import pickle
with open('./camera_params/camera_param.pkl', 'rb') as f:
    camera_param = pickle.load(f)

cameraMatrix, distCoeffs, rvecs, tvecs, stdDeviationsInstrinsics, stdDeviationsExtrinsics = camera_param

# 全画像をロード #
# 入力画像 #
import glob, os
image_paths = [os.path.basename(r) for r in sorted(glob.glob('calibration/*.bmp'))]
# print(image_paths)

calibImages = []

for image_path in image_paths:
    path = 'calibration/' + image_path
    calibImage = cv2.imread(path)
    # print(calibImage)

    if calibImage is None:
        break

    calibImages.append(calibImage)

# 画像サイズの書き出し
imgSize = calibImages[0].shape[:2]
h,  w = imgSize
print(imgSize)

newcameramtx, roi=cv2.getOptimalNewCameraMatrix(cameraMatrix,distCoeffs,(w,h),1,(w,h))
print(newcameramtx, roi)

for i, before_undistortImg in enumerate(calibImages):
    # undistort
    dst = cv2.undistort(before_undistortImg, cameraMatrix, distCoeffs, None, newcameramtx)

    # crop the image
    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]
    cv2.imwrite('./result/calibresult'+ str(i+1) +'.png',dst)