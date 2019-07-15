import cv2
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore', category=matplotlib.MatplotlibDeprecationWarning)
import numpy as np
import glob, os
import csv
import pickle
import json
import pandas as pd

plt.rcParams['figure.figsize'] = (20.0, 10.0)
aruco = cv2.aruco

# Create checker board #
parameters = aruco.DetectorParameters_create()
dictionaryID = aruco.DICT_5X5_100
# dictionaryID = aruco.DICT_4X4_250
dictionary = aruco.getPredefinedDictionary(dictionaryID)
squareL = 0.028
markerL = 0.024
pixels_per_mm = 10 # for checker board image
A4size = (210, 297)
tb, lr = [5,5] # minimul margin (height, width) when printing in mm

def max_within_upper(num, upper):
    i = 1
    while True:
        if num*i > upper:
            return ([i-1, int(num*(i-1))])
        else:
            i += 1

squareNumX, boardSizeX = max_within_upper(squareL*1000, A4size[0]- lr*2 ) # in mm
squareNumY, boardSizeY = max_within_upper(squareL*1000, A4size[1]- tb*2 ) # in mm

# Calibration #
calibration_image_path = "./calib_pictures_hiro3/"
image_format = "JPG"
save_format = "json"

def imshow_inline(img_name="", img=None):
    if img is None:
        if not img_name:
            print("Give imshow_inline an image name or an image.")
            return -1
        else:
            img = cv2.imread(img_name)
    plt.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))

def get_board_image():
    board = aruco.CharucoBoard_create(squareNumX, squareNumY, squareL, markerL, dictionary)
    
    # The third parameter is the (optional) margin in pixels, so none of the markers are touching the image border.
    # Finally, the size of the marker border, similarly to drawMarker() function. The default value is 1.
    boardImage = board.draw((boardSizeX*pixels_per_mm, boardSizeY*pixels_per_mm), None, 0, 1) # 10 pixels/mm
    return(board, boardImage)

def add_margin(pil_img, tb_pixels, lr_pixels):
    width, height = pil_img.size
    new_width = width + lr_pixels
    new_height = height + tb_pixels
    result = Image.new(pil_img.mode, (new_width,new_height), (255))
    result.paste(pil_img, (int(lr_pixels/2), int(tb_pixels/2)))
    return result      

def output_board_configparams_to_csv(output_filename):
    with open(output_filename, 'w', newline='') as csvfile:
        config_writer = csv.writer(csvfile, lineterminator='\n')
        config_writer.writerow(['dictionary ID', dictionaryID])
        config_writer.writerow(['square length', squareL])
        config_writer.writerow(['marker length', markerL])
        config_writer.writerow(['number of squares (x and y)', squareNumX, squareNumY])
        config_writer.writerow(['minimul margin (tb and lr)', tb, lr])

def create_ChArUco_board_in_A4size(board_name, outcsv=True):
    board, boardImage, = get_board_image()
    
    # Add the margin to the image
    tb_pixels = (A4size[1] - boardSizeY) * pixels_per_mm
    lr_pixels = (A4size[0] - boardSizeX) * pixels_per_mm
    boardImage_margin = np.asarray( add_margin(Image.fromarray(boardImage), tb_pixels, lr_pixels) )
    
    dirpath_board = "./board/"
    if not os.path.isdir(dirpath_board):
        os.mkdir(dirpath_board)
    cv2.imwrite(dirpath_board+board_name, boardImage_margin)
    imshow_inline(img_name=dirpath_board+board_name)
    
    if outcsv:
        filename_without_ext = os.path.splitext(board_name)[0]
        output_board_configparams_to_csv(dirpath_board+filename_without_ext+'.csv')

def get_file_paths(file_dir, file_ext):
    path = file_dir + '*.' + file_ext
    file_names = [os.path.basename(r) for r in glob.glob(path)]
    file_paths = [file_dir+fs for fs in file_names]
    print(file_names)
    print(file_paths)
    return file_paths, file_names

def detect_ChArUco_board(image_paths, outimg=True):
    for image_path in image_paths:
        checkerBoardImage = cv2.imread(image_path)

        # Detect ChArUco markers #
        markerCorners, markerIds  = [0,0]
        markerCorners, markerIds, rejectedImgPoints = aruco.detectMarkers(checkerBoardImage, dictionary)

        # Detect the checker board based on the detected marker, and draw the result #
        outputImage = checkerBoardImage.copy()
        if markerIds is None:
            break
        if markerIds.size > 0:
            charucoCorners, charucoIds = [0,0]
            cv2.aruco.drawDetectedMarkers(outputImage, markerCorners, markerIds)
            # charucoCorners, charucoIds = aruco.interpolateCornersCharuco(markerCorners, markerIds, checkerBoardImage, board)
            # outputImage = aruco.drawDetectedCornersCharuco(outputImage, charucoCorners, charucoIds)

        dirpath, file = os.path.split(image_path)
        dirpath_results = dirpath+"/det_results/"
        if not os.path.isdir(dirpath_results):
            os.mkdir(dirpath_results)
        imshow_inline(img=outputImage)
        if outimg:
            cv2.imwrite(dirpath_results+file, outputImage)

def get_calibration_images(calib_img_paths):
    calibImages = []
    for calib_img_path in calib_img_paths:
        calibImage = cv2.imread(calib_img_path)
        if calibImage is None:
            break
        calibImages.append(calibImage)
    return calibImages

def show_calibration_result(calibrate_params):
    print("####################")
    retval, cameraMatrix, distCoeffs, rvecs, tvecs, stdDeviationsInstrinsics, stdDeviationsExtrinsics, perViewErrors = calibrate_params
    print("Final re-projection error : \n", retval)
    print("Camera matrix : \n", cameraMatrix)
    print("Vector of distortion coefficients : \n", distCoeffs)
    print("Vector of rotation vectors (see Rodrigues) : \n", rvecs)
    print("Vector of translation vectors : \n", tvecs)
    print("Vector of standard deviations estimated for intrinsic parameters : \n", stdDeviationsInstrinsics)
    print("Vector of standard deviations estimated for extrinsic parameters : \n", stdDeviationsExtrinsics)
    print("Vector of average re-projection errors : \n", perViewErrors)

def calibrate_with_ChArUco_board(calibImages, param_file_ex='.pkl'):
    board, boardImg = get_board_image()

    # Detect checker board intersection of ChArUco #
    allCharucoCorners = []
    allCharucoIds = []
    charucoCorners, charucoIds = [0,0]
    for calImg in calibImages:
        # Find ArUco markers #
        res = aruco.detectMarkers(calImg, dictionary)
        # Find ChArUco corners #
        if len(res[0])>0:
            res2 = cv2.aruco.interpolateCornersCharuco(res[0], res[1], calImg, board)
            if res2[1] is not None and res2[2] is not None and len(res2[1])>3:
                allCharucoCorners.append(res2[1])
                allCharucoIds.append(res2[2])

            cv2.aruco.drawDetectedMarkers(calImg,res[0],res[1])
        img = cv2.resize(calImg, None, fx=0.5, fy=0.5)
        # cv2.imshow('calibration image',img)
        # cv2.waitKey(0)
        
    cv2.destroyAllWindows()
    
    # Calibration and output errors #
    cal = []
    try:
        imgSize = calibImages[0].shape[:2]
        cal = cv2.aruco.calibrateCameraCharucoExtended(allCharucoCorners,allCharucoIds,board,imgSize,None,None)
    except:
        print("can not calibrate ...")

    # show_calibration_result(cal)
    retval, cameraMatrix, distCoeffs, rvecs, tvecs, stdDeviationsInstrinsics, stdDeviationsExtrinsics, perViewErrors = cal
    tmp = [cameraMatrix, distCoeffs, rvecs, tvecs, stdDeviationsInstrinsics, stdDeviationsExtrinsics]

    # Save the camera parameters #
    class MyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            else:
                return super(MyEncoder, self).default(obj)
    
    fname = "camera_param"
    if save_format == 'json':
        with open(fname+'.json', mode='w') as f:
            data = {"camera_matrix": cameraMatrix.tolist(), "dist_coeff": distCoeffs.tolist(), "rvecs": rvecs, "tvecs": tvecs}
            json.dump(data,f,sort_keys=True,indent=4,cls=MyEncoder)
    else:
        with open(fname+'.pkl', mode='wb') as f:
            pickle.dump(tmp, f, protocol=-1)
    
    print("Saved.")

def weak_undistort(cam_param_path, images):
    # Read camera parameters as a pkl file #
    with open(cam_param_path, 'rb') as f:
        camera_params = pickle.load(f)

    cameraMatrix, distCoeffs, rvecs, tvecs, stdDeviationsInstrinsics, stdDeviationsExtrinsics = camera_params

    # Writing the camera matrix #
    imgSize = images[0].shape[:2]
    h,  w = imgSize
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix,distCoeffs,(w,h),1,(w,h))
    print(newcameramtx, roi)

    for i, before_undistortImg in enumerate(images):
        # Undistort #
        dst = cv2.undistort(before_undistortImg, cameraMatrix, distCoeffs, None, newcameramtx)
        
        # Crop the image #
        x,y,w,h = roi
        dst = dst[y:y+h, x:x+w]
        dirpath = "./undistort_result/"
        if not os.path.isdir(dirpath):
            os.mkdir(dirpath)
        cv2.imwrite(dirpath+"undistorted"+ str(i+1) +'.'+image_format,dst)

def undistort(cam_param_path, images):
    # Read camera parameters as a pkl file #
    with open(cam_param_path, 'rb') as f:
        camera_params = pickle.load(f)

    cameraMatrix, distCoeffs, rvecs, tvecs, stdDeviationsInstrinsics, stdDeviationsExtrinsics = camera_params

    # Display the corresponding points before/after correction #
    w, h = np.meshgrid(range(0, images[0].shape[1], 10), range(0, images[0].shape[0], 10))
    pts = (np.vstack((w.flatten(), h.flatten())).T).astype('float32')
    pts_new = cv2.undistortPoints(np.array([pts]), cameraMatrix, distCoeffs, P=cameraMatrix)[0]

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(pts[:,0], pts[:,1], 2, 'r', alpha=.5)
    ax.scatter(pts_new[:,0], pts_new[:,1], 2, 'b', alpha=.5)
    plt.xlim([0,3000])
    plt.ylim([0,2250])
    plt.show()

    # Writing the camera matrix #
    new_cammat = cv2.getOptimalNewCameraMatrix(cameraMatrix, distCoeffs, (images[0].shape[1], images[0].shape[0]), 1)[0]
    map = cv2.initUndistortRectifyMap(cameraMatrix, distCoeffs, np.eye(3), new_cammat, (images[0].shape[1], images[0].shape[0]), cv2.CV_32FC1)

    for i, before_undistortImg in enumerate(images):
        # Undistort #
        img_und = cv2.remap(before_undistortImg, map[0], map[1], cv2.INTER_AREA)
        plt.subplot(1,2,1)
        plt.imshow(cv2.cvtColor(before_undistortImg,cv2.COLOR_BGR2RGB))
        plt.subplot(1,2,2)
        plt.imshow(cv2.cvtColor(img_und,cv2.COLOR_BGR2RGB))
        # plt.show()

        img_und = cv2.undistort(before_undistortImg, cameraMatrix, distCoeffs)
        plt.subplot(1,2,1)
        plt.imshow(cv2.cvtColor(before_undistortImg,cv2.COLOR_BGR2RGB))
        plt.subplot(1,2,2)
        plt.imshow(cv2.cvtColor(img_und,cv2.COLOR_BGR2RGB))
        # plt.show()

        # save the image #
        dirpath = "./undistort_result/"
        if not os.path.isdir(dirpath):
            os.mkdir(dirpath)
        cv2.imwrite(dirpath+"undistorted"+ str(i+1) +'.'+image_format, img_und)

def main():
    calib_img_paths, calib_img_names = get_file_paths(calibration_image_path, image_format)
    
    ## Create a borad ##
    # board_name = "sample_board_"
    # create_ChArUco_board_in_A4size(board_name+'.png')
    
    ## Detect a board ##
    # detect_test_dir = "./detect_test/" 
    # pic_paths, pic_names = get_file_paths(detect_test_dir, 'png')
    # detect_ChArUco_board(pic_paths)
    
    ## Calibration ##
    calibrate_with_ChArUco_board(get_calibration_images(calib_img_paths))
    
    ## Undistort ##
    # cam_param_path = "./camera_param.pkl"
    # weak_undistort(cam_param_path, get_calibration_images(calib_img_paths))
    # undistort(cam_param_path, get_calibration_images(calib_img_paths))

if __name__ == '__main__':
    main()
