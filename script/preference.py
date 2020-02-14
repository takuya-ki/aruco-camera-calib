import cv2
aruco = cv2.aruco

# Generation of checker board #
parameters = aruco.DetectorParameters_create()
dictionary = aruco.getPredefinedDictionary(aruco.DICT_5X5_100)
board = aruco.CharucoBoard_create(10, 10, 0.06, 0.04, dictionary) # squaresX, squaresY, squareLength, markerLength, dictionary
# board = aruco.CharucoBoard_create(5, 4, 0.06, 0.04, dictionary) # squaresX, squaresY, squareLength, markerLength, dictionary

calibration_image_path = "./calibration/iphone/"
# calibration_image_path = "./../../EvaluateImages/forLearningWithCircleAR/bmp/calibration/"
image_format = "jpg"
