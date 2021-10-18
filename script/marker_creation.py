#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import cv2
import glob

aruco = cv2.aruco
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
number_of_pixels = 64
number_of_markers_you_want = 5
marker_savedirpath = os.path.join(os.getcwd(), "../markers")


def get_file_paths(file_dirpath, file_ext):
    path = os.path.join(file_dirpath, '*.'+file_ext)
    file_names = [os.path.basename(r) for r in glob.glob(path)]
    file_paths = [os.path.join(file_dirpath, fs) \
                    for fs in file_names]
    print(file_names)
    return file_paths, file_names


if __name__ == '__main__':

    # delete files under save dir
    if os.path.exists(marker_savedirpath):
        marker_filepaths, marker_filenames = \
            get_file_paths(marker_savedirpath, '*')
        [os.remove(mpath) for mpath in marker_filepaths]

    # make save dir
    os.makedirs(marker_savedirpath, 
                exist_ok=True)

    # generate into save dir
    for i in range(number_of_markers_you_want):
        marker = aruco.drawMarker(dictionary, i, 
                                  number_of_pixels)
        cv2.imwrite(os.path.join(marker_savedirpath, \
                                 str(i)+'.'+ \
                                 str(number_of_pixels)+ \
                                 '.png'), marker)
