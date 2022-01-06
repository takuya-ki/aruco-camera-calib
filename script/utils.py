#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import cv2
import glob
import argparse
import os.path as osp


ARUCO_DICT = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
    "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
    "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
    "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
    "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
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
        '--out_dir', dest='out_dir', type=str, default="../data/markers/",
        help='set out directory path')
    return parser.parse_args()


def get_file_paths(file_dirpath, file_ext):
    path = osp.join(file_dirpath, '*.'+file_ext)
    file_names = [osp.basename(r) for r in glob.glob(path)]
    file_paths = [osp.join(file_dirpath, fs) for fs in file_names]
    print(file_names)
    return file_paths, file_names


def get_aruco_dict(dict_label):
    return cv2.aruco.getPredefinedDictionary(ARUCO_DICT[dict_label])
