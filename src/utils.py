#!/usr/bin/env python3

import os
import cv2
import glob
import pickle
import argparse
import numpy as np
from PIL import Image
import os.path as osp

aruco = cv2.aruco
np.set_printoptions(precision=3)


ARUCO_DICT = {
    "DICT_4X4_50": aruco.DICT_4X4_50,
    "DICT_4X4_100": aruco.DICT_4X4_100,
    "DICT_4X4_250": aruco.DICT_4X4_250,
    "DICT_4X4_1000": aruco.DICT_4X4_1000,
    "DICT_5X5_50": aruco.DICT_5X5_50,
    "DICT_5X5_100": aruco.DICT_5X5_100,
    "DICT_5X5_250": aruco.DICT_5X5_250,
    "DICT_5X5_1000": aruco.DICT_5X5_1000,
    "DICT_6X6_50": aruco.DICT_6X6_50,
    "DICT_6X6_100": aruco.DICT_6X6_100,
    "DICT_6X6_250": aruco.DICT_6X6_250,
    "DICT_6X6_1000": aruco.DICT_6X6_1000,
    "DICT_7X7_50": aruco.DICT_7X7_50,
    "DICT_7X7_100": aruco.DICT_7X7_100,
    "DICT_7X7_250": aruco.DICT_7X7_250,
    "DICT_7X7_1000": aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": aruco.DICT_ARUCO_ORIGINAL,
    "DICT_APRILTAG_16h5": aruco.DICT_APRILTAG_16h5,
    "DICT_APRILTAG_25h9": aruco.DICT_APRILTAG_25h9,
    "DICT_APRILTAG_36h10": aruco.DICT_APRILTAG_36h10,
    "DICT_APRILTAG_36h11": aruco.DICT_APRILTAG_36h11
}


def get_options():
    """Returns user-specific options."""
    parser = argparse.ArgumentParser(description='Set options.')
    parser.add_argument(
        '--dict', dest='aruco_dict', type=str,
        default="DICT_4X4_250", choices=ARUCO_DICT.keys(),
        help='set aruco dictionaly type')
    parser.add_argument(
        '--num_pixels', dest='num_pixels', type=int, default=64,
        help="set number of pixels for generated markers")
    parser.add_argument(
        '--num_markers', dest='num_markers', type=int, default=5,
        help='set number of markers for creation')
    parser.add_argument(
        '--in_dir', dest='in_dir',
        type=str, default="../data/pictures/sample/",
        help='set input directory path')
    parser.add_argument(
        '--out_dir', dest='out_dir', type=str, default="../data/markers/",
        help='set output directory path')
    parser.add_argument(
        '--camera_param', dest='camera_param_path',
        type=str, default="../data/result/camera_param.pkl",
        help='set camera parameter file path')
    parser.add_argument(
        '--board_name', dest='board_name', type=str, default="sample_board",
        help='set output board image file name')
    parser.add_argument(
        '--input_board_cfg_pkl', dest='input_board_cfg_pkl',
        action='store_true',
        help='input board configuration pkl file?')
    parser.add_argument(
        '--board_cfg_pkl_path', dest='board_cfg_pkl_path',
        type=str, default="../data/board/sample_board.pkl",
        help='set input board configuration pickle file path')
    parser.add_argument(
        '--square_length', dest='square_length', type=float, default=0.028,
        help="set length value of square")
    parser.add_argument(
        '--marker_length', dest='marker_length', type=float, default=0.024,
        help='set length value of marker')
    parser.add_argument(
        '--pixels_per_mm', dest='pixels_per_mm', type=int, default=10,
        help="set pixels per mm")
    parser.add_argument(
        '--h_margin', dest='h_margin', type=int, default=5,
        help='set horizontal margin')
    parser.add_argument(
        '--v_margin', dest='v_margin', type=int, default=5,
        help='set vertical margin')
    parser.add_argument(
        '--save_pkl', dest='save_pkl', action='store_true',
        help='output board configuration info in a pkl file?')
    parser.add_argument(
        '--calib_result_format', dest='calib_result_format',
        type=str, default='pkl', choices=['json', 'pkl'],
        help='set save file format for calibration result , json or pkl')
    parser.add_argument(
        '--is_print_calib_result', dest='is_print_calib_result',
        action='store_true',
        help='print calibration results?')
    parser.add_argument(
        '--is_undistort', dest='is_undistort', action='store_true',
        help='apply undistortion with calibration results?')
    return parser.parse_args()


def get_file_paths(file_dirpath, file_ext):
    """Get file names and paths."""
    path = osp.join(file_dirpath, '*.'+file_ext)
    file_names = [osp.basename(r) for r in glob.glob(path)]
    file_paths = [osp.join(file_dirpath, fs) for fs in file_names]
    print(file_names)
    return file_paths, file_names


def get_aruco_dict(dict_label):
    """Returns one of the dictionaries defined in ARUCO_DICT[dict_label]."""
    return aruco.getPredefinedDictionary(ARUCO_DICT[dict_label])


def read_pickle(pkl_path):
    """Returns loaded data from a pickle file."""
    with open(pkl_path, 'rb') as f:
        data = pickle.load(f)
    return data


def scale_to_width(img, width):
    """Returns resized OpenCV image data with a specified image width."""
    scale = width / img.shape[1]
    return cv2.resize(img, dsize=None, fx=scale, fy=scale)


def imshow(img_path="", img=None, wn='image', wsec=3000, width=None):
    """Show an OpenCV image with a certain manner."""
    if img is None:
        img = cv2.imread(img_path)
    if width is not None:
        img = scale_to_width(img, width)
    cv2.startWindowThread()
    cv2.namedWindow(wn, cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow(wn, 50, 100)
    cv2.imshow(wn, img)
    cv2.waitKey(wsec)


def max_within_upper(num, upper):
    """Calculate ChArUco board size to spread as many markers as possible."""
    i = 1
    while True:
        if num*i > upper:
            return ([i-1, int(num*(i-1))])
        else:
            i += 1


def add_margin(pil_img, tb_pixels, lr_pixels):
    """Returns ChArUco board image with specified margin added."""
    width, height = pil_img.size
    new_width = width + lr_pixels
    new_height = height + tb_pixels
    result = Image.new(pil_img.mode, (new_width, new_height), (255))
    result.paste(pil_img, (int(lr_pixels/2), int(tb_pixels/2)))
    return result


def get_A4_board(dictionary,
                 squareL,
                 markerL,
                 tb,
                 lr,
                 pixels_per_mm):
    """Returns ChArUco board and final image."""

    # calculate parameters for board [mm]
    A4size = (210, 297)
    squareNumX, boardSizeX = max_within_upper(
        squareL*1000, A4size[0] - lr*2)
    squareNumY, boardSizeY = max_within_upper(
        squareL*1000, A4size[1] - tb*2)
    boardPixX = boardSizeX*pixels_per_mm
    boardPixY = boardSizeY*pixels_per_mm
    tb_pixels = A4size[1]*pixels_per_mm - boardPixY
    lr_pixels = A4size[0]*pixels_per_mm - boardPixX

    # create board image
    board = aruco.CharucoBoard_create(
        squareNumX,
        squareNumY,
        squareL,
        markerL,
        dictionary)

    # third parameter is the (optional) margin in pixels
    # if it is set as 0, none of the markers are touching the image border
    # the last parameter is the size of the marker border
    boardImage = board.draw((boardPixX, boardPixY), None, 0, 1)
    # add the margin to the image
    boardImage_margin = np.asarray(
        add_margin(Image.fromarray(boardImage), tb_pixels, lr_pixels))

    return board, boardImage_margin


def show_calibration_params(calib_params):
    """Prints all the calibration parameters."""
    print("###################################")
    retval, camMat, distCoeffs, rvecs, tvecs, stdIn, stdEx, projErr = \
        calib_params
    print("Final re-projection error : \n", retval)
    print("Camera matrix : \n", camMat)
    print("Vector of distortion coefficients : \n", distCoeffs)
    print("Vector of rotation vectors (see Rodrigues) : \n", rvecs)
    print("Vector of translation vectors : \n", tvecs)
    print("Vector of std estimated for intrinsic parameters : \n", stdIn)
    print("Vector of std estimated for extrinsic parameters : \n", stdEx)
    print("Vector of average re-projection errors : \n", projErr)


def undistort(
        cam_mat,
        dist_coeffs,
        images,
        res_dirpath):
    """Saves undistorted images with specified calibration parameters."""

    # write the camera matrix
    imgSize = images[0].shape[:2]
    h, w = imgSize
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(
        cam_mat, dist_coeffs, (w, h), 1, (w, h))

    for i, img in enumerate(images):
        dst = cv2.undistort(img,
                            cam_mat,
                            dist_coeffs,
                            None,
                            newcameramtx)
        # crop the image
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]
        cv2.imwrite(osp.join(res_dirpath, "undist"+str(i+1)+'.png'), dst)
