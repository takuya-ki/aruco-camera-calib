#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import cv2
import glob
import os.path as osp

aruco = cv2.aruco
dictionary = aruco.getPredefinedDictionary(
    aruco.DICT_4X4_250)
num_of_pixels = 64
num_of_markers = 5
marker_savedirpath = osp.join(
    osp.dirname(__file__), "../markers")


def get_file_paths(file_dirpath, file_ext):
    path = osp.join(file_dirpath, '*.'+file_ext)
    file_names = [osp.basename(r) for r in glob.glob(path)]
    file_paths = [osp.join(file_dirpath, fs) for fs in file_names]
    print(file_names)
    return file_paths, file_names


if __name__ == '__main__':
    # delete files under save dir
    if osp.exists(marker_savedirpath):
        marker_paths, marker_names = get_file_paths(marker_savedirpath, '*')
        [os.remove(mpath) for mpath in marker_paths]

    # make save dir
    os.makedirs(marker_savedirpath, exist_ok=True)

    # generate into save dir
    for i in range(num_of_markers):
        marker = aruco.drawMarker(
            dictionary, i, num_of_pixels)
        cv2.imwrite(osp.join(
            marker_savedirpath,
            str(i)+'.'+str(num_of_pixels)+'.png'),
            marker)
