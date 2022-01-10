#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import cv2
import json
import pickle
import numpy as np
import os.path as osp

import utils

aruco = cv2.aruco
np.set_printoptions(precision=3)


def get_calib_images(calib_img_paths, resimgs=False):
    calibImages = []
    for calib_img_path in calib_img_paths:
        calibImage = cv2.imread(calib_img_path)
        if calibImage is None:
            print(osp.basename(calib_img_path)+" cannot be read.")
            continue
        if resimgs:
            calibImage = cv2.resize(calibImage, (1280, 720))
        calibImages.append(calibImage)
    return calibImages


def calibrate_with_ChArUco_board(
        result_filepath_no_ext,
        calibImages,
        calib_result_format,
        dictionary,
        squareL,
        markerL,
        tb,
        lr,
        pixels_per_mm,
        isUndistort=False,
        isPrintResult=False,
        undistort_res_dirpath=None):

    board, _ = utils.get_A4_board(
        dictionary,
        squareL,
        markerL,
        tb,
        lr,
        pixels_per_mm)

    # detect checker board intersection of ChArUco
    allCharucoCorners = []
    allCharucoIds = []
    charucoCorners, charucoIds = [0, 0]
    decimator = 0
    num_images_to_use = 0
    # critetion for sub pixel corner detection
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
                100, 0.00001)

    decimation_interval = 2  # 1 means not applied
    for calImg in calibImages:
        calImg = cv2.cvtColor(calImg, cv2.COLOR_BGR2GRAY)  # convert to gray
        # find ArUco markers
        corners, ids, rejectedImgPoints = \
            aruco.detectMarkers(calImg, dictionary)
        # find ChArUco corners
        if len(corners) > 0:
            # sub pixel detection
            # corners = cv2.cornerSubPix(
            #   calImg,
            #   corners,
            #   winSize=(3,3),
            #   zeroZone=(-1,-1),
            #   criteria=criteria)
            res2 = aruco.interpolateCornersCharuco(
                corners, ids, calImg, board)
            if (res2[1] is not None) and\
               (res2[2] is not None) and\
               (len(res2[1]) > 5) and\
               (decimator % decimation_interval == 0):

                allCharucoCorners.append(res2[1])
                allCharucoIds.append(res2[2])
                num_images_to_use += 1
            decimator += 1
            aruco.drawDetectedMarkers(calImg, corners, ids)

    print("\n Use "+str(num_images_to_use)+" images for this calibration.")
    try:
        imgSize = calibImages[0].shape[:2]
        calib_params = aruco.calibrateCameraCharucoExtended(
            allCharucoCorners, allCharucoIds, board, imgSize, None, None)
    except Exception as e:
        print("Failed to calibrate..., ", e.args)
        return -1

    if isPrintResult:
        utils.show_calibration_params(calib_params)

    _, camMat, distCoef, rvecs, tvecs, stdIn, stdEx, peojErr = calib_params
    save_param_list = [camMat, distCoef, rvecs, tvecs, stdIn, stdEx]

    # save the camera parameters
    if calib_result_format == 'json':
        cam_param_path = result_filepath_no_ext+'.json'
        with open(cam_param_path, mode='w') as f:
            data = {"camera_matrix": cameraMatrix.tolist(),
                    "dist_coeff": distCoeffs.tolist(),
                    "rvecs": rvecs,
                    "tvecs": tvecs}
            json.dump(data, f, sort_keys=True, indent=4)
    elif calib_result_format == 'pkl':
        cam_param_path = result_filepath_no_ext+'.pkl'
        with open(cam_param_path, mode='wb') as f:
            pickle.dump(save_param_list, f, protocol=-1)
    print("Saved "+cam_param_path)

    if isUndistort:
        if undistort_res_dirpath is None:
            print("Error: Please specify save path for undistort images.")
            return -1
        with open(cam_param_path, 'rb') as f:
            camera_params = pickle.load(f)
        cam_mat, dist_coeffs, rvecs, tvecs, stdIn, stdEx = camera_params
        utils.undistort(
            cam_mat,
            dist_coeffs,
            calibImages,
            undistort_res_dirpath)


if __name__ == '__main__':
    args = utils.get_options()

    calib_image_dirpath = osp.join(
        osp.dirname(__file__), args.in_dir)
    calib_result_dirpath = osp.join(
        osp.dirname(__file__), args.out_dir)
    os.makedirs(calib_result_dirpath, exist_ok=True)
    result_filepath_no_ext = osp.join(
        calib_result_dirpath, "camera_param")

    # to test the calibration result
    undistort_res_dirpath = None
    if args.is_undistort:
        undistort_res_dirpath = osp.join(
            calib_image_dirpath, "undistort_result/")
        os.makedirs(undistort_res_dirpath, exist_ok=True)

    # read parameters from arguments
    dictionary = utils.get_aruco_dict(args.aruco_dict)
    squareL = args.square_length
    markerL = args.marker_length
    tb = args.v_margin
    lr = args.h_margin
    pixels_per_mm = args.pixels_per_mm
    # read parameters from configuration pickle file
    if args.input_board_cfg_pkl:
        board_cfg_pkl_path = osp.join(
            osp.dirname(__file__),
            args.board_cfg_pkl_path)
        board_cfg = utils.read_pickle(board_cfg_pkl_path)
        dictionary = utils.get_aruco_dict(board_cfg['dict_label'])
        squareL = board_cfg['square_length']
        markerL = board_cfg['marker_length']
        tb = board_cfg['margin_tb']
        lr = board_cfg['margin_lr']

    img_paths, _ = utils.get_file_paths(calib_image_dirpath, '*')
    calibrate_with_ChArUco_board(
        result_filepath_no_ext,
        get_calib_images(img_paths, resimgs=True),
        args.calib_result_format,
        dictionary,
        squareL,
        markerL,
        tb,
        lr,
        pixels_per_mm,
        isUndistort=args.is_undistort,
        isPrintResult=args.is_print_calib_result,
        undistort_res_dirpath=undistort_res_dirpath)
