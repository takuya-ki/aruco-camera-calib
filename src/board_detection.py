#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import cv2
import pickle
import os.path as osp

import utils

aruco = cv2.aruco


def detect_ChArUco_board(
        image_path,
        dictionary,
        squareL,
        markerL,
        tb,
        lr,
        pixels_per_mm,
        cameraMatrix,
        distCoeffs):

    board, _ = utils.get_A4_board(
        dictionary,
        squareL,
        markerL,
        tb,
        lr,
        pixels_per_mm)

    checkerBoardImage = cv2.imread(image_path)
    if checkerBoardImage is None:
        print(osp.basename(image_path)+" cannot be read.")
        return -1

    # detect ChArUco markers
    markerCorners, markerIds = [0, 0]
    markerCorners, markerIds, rejectedImgPoints = \
        aruco.detectMarkers(checkerBoardImage, dictionary)
    markerCorners, markerIds, rejectedImgPoints, recoveredIdxs = \
        aruco.refineDetectedMarkers(
            checkerBoardImage,
            board,
            markerCorners,
            markerIds,
            rejectedImgPoints)

    # detect the checker board based on the detected marker
    outImage = checkerBoardImage.copy()
    if markerIds is None:
        return -1
    if markerIds.size > 0:
        charucoCorners, charucoIds = [0, 0]
        cv2.aruco.drawDetectedMarkers(
            outImage, markerCorners, markerIds)

        retval, charucoCorners, charucoIds = aruco.interpolateCornersCharuco(
            markerCorners, markerIds, checkerBoardImage, board)
        outImage = aruco.drawDetectedCornersCharuco(
            outImage, charucoCorners, charucoIds)

        # use a camera parameter
        retval, rvec, tvec = aruco.estimatePoseCharucoBoard(
            charucoCorners, charucoIds, board, cameraMatrix, distCoeffs)
        if retval:
            aruco.drawAxis(outImage, cameraMatrix, distCoeffs, rvec, tvec, 0.1)

    cv2.imshow("detected", outImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    args = utils.get_options()

    input_image_dirpath = osp.join(
        osp.dirname(__file__),
        args.in_dir)
    # recognize any extentions
    image_paths, image_names = utils.get_file_paths(
        input_image_dirpath, "*")

    # read camera parameters
    camera_param_filepath = osp.join(
        osp.dirname(__file__), args.camera_param_path)
    cameraMatrix, distCoeffs, rvecs, tvecs, stdDevIn, stdDevEx = \
        utils.read_pickle(camera_param_filepath)

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

    for image_path in image_paths:
        detect_ChArUco_board(
            image_path,
            dictionary,
            squareL,
            markerL,
            tb,
            lr,
            pixels_per_mm,
            cameraMatrix,
            distCoeffs)
