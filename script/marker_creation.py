#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import cv2
import glob
import os.path as osp

import utils

aruco = cv2.aruco


def create_aruco_markers(
        dictionary,
        marker_i,
        num_pixels,
        isSave=True,
        savedirpath=None):

    marker = aruco.drawMarker(
        dictionary, marker_i, num_pixels)
    if isSave:
        if savedirpath is None:
            print("Error: Please specify save path.")
            return()
        cv2.imwrite(osp.join(
            savedirpath,
            str(marker_i)+'.'+str(num_pixels)+'.png'),
            marker)


if __name__ == '__main__':
    args = utils.get_options()

    # delete files under save dir and make save dir
    marker_savedirpath = osp.join(
        osp.dirname(__file__), args.out_dir)
    if osp.exists(marker_savedirpath):
        marker_paths, marker_names = \
            utils.get_file_paths(marker_savedirpath, '*')
        [os.remove(mpath) for mpath in marker_paths]
    os.makedirs(marker_savedirpath, exist_ok=True)

    dictionary = utils.get_aruco_dict(args.aruco_dict)
    # generate into save dir
    for i in range(args.num_markers):
        create_aruco_markers(
            dictionary,
            i,
            args.num_pixels,
            isSave=True,
            savedirpath=marker_savedirpath)
