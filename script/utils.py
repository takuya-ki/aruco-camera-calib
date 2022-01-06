#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import cv2
import glob
import pickle
import argparse
import numpy as np
from PIL import Image
import os.path as osp

aruco = cv2.aruco


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
    return parser.parse_args()


def get_file_paths(file_dirpath, file_ext):
    path = osp.join(file_dirpath, '*.'+file_ext)
    file_names = [osp.basename(r) for r in glob.glob(path)]
    file_paths = [osp.join(file_dirpath, fs) for fs in file_names]
    print(file_names)
    return file_paths, file_names


def get_aruco_dict(dict_label):
    return aruco.getPredefinedDictionary(ARUCO_DICT[dict_label])


def read_pickle(pkl_path):
    with open(pkl_path, 'rb') as f:
        data = pickle.load(f)
    return data


def max_within_upper(num, upper):
    i = 1
    while True:
        if num*i > upper:
            return ([i-1, int(num*(i-1))])
        else:
            i += 1


def add_margin(pil_img, tb_pixels, lr_pixels):
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
