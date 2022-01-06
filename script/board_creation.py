#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import cv2
import pickle
import os.path as osp
import matplotlib.pyplot as plt

import utils

aruco = cv2.aruco
plt.rcParams['figure.figsize'] = (10.0, 10.0)


def imshow(img_path="", img=None):
    if img is None:
        if not img_path:
            print("Give an image path or an image data to imshow().")
            return -1
        else:
            img = cv2.imread(img_path)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()


def make_board_cfg_pickle(
        pkl_path,
        dict_label,
        squareL,
        markerL,
        tb,
        lr):

    board_cfg_dict = {
        'dict_label': dict_label,
        'square_length': squareL,
        'marker_length': markerL,
        'margin_tb': tb,
        'margin_lr': lr
    }
    with open(pkl_path, 'wb') as f:
        pickle.dump(board_cfg_dict, f, protocol=4)


def create_ChArUco_board_in_A4size(
        board_dirpath,
        board_filename,
        dict_label,
        dictionary,
        squareL,
        markerL,
        tb,
        lr,
        pixels_per_mm,
        save_pkl=False):

    _, board_img = utils.get_A4_board(
        dictionary,
        squareL,
        markerL,
        tb,
        lr,
        pixels_per_mm)
    board_path = osp.join(board_dirpath, board_filename)
    cv2.imwrite(board_path, board_img)
    imshow(img_path=board_path)

    if save_pkl:
        # remove the extention from the board_name
        make_board_cfg_pickle(
            osp.join(board_dirpath, board_filename.split('.')[0]+'.pkl'),
            dict_label,
            squareL,
            markerL,
            tb,
            lr)


if __name__ == '__main__':
    args = utils.get_options()

    board_filename = args.board_name+".png"
    os.makedirs(osp.join(osp.dirname(__file__), "../data/board"),
                exist_ok=True)

    create_ChArUco_board_in_A4size(
        osp.join(osp.dirname(__file__), args.out_dir),
        args.board_name+'.png',
        args.aruco_dict,
        utils.get_aruco_dict(args.aruco_dict),
        args.square_length,
        args.marker_length,
        args.v_margin,      # minimum horizontal margins [mm]
        args.h_margin,      # minimum vertical margins [mm]
        args.pixels_per_mm,
        save_pkl=args.save_pkl)
