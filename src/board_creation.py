#!/usr/bin/env python3

import os
import cv2
import pickle
import os.path as osp

import utils

aruco = cv2.aruco


def make_board_cfg_pickle(
        pkl_path,
        dict_label,
        squareL,
        markerL,
        tb,
        lr):
    """Saves board configuration data as a pickle file."""

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
    """Creates a ChArUco board of A4 size and save the config data."""

    _, board_img = utils.get_A4_board(
        dictionary,
        squareL,
        markerL,
        tb,
        lr,
        pixels_per_mm)
    board_path = osp.join(board_dirpath, board_filename)
    cv2.imwrite(board_path, board_img)
    utils.imshow(img_path=board_path, width=600)

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
