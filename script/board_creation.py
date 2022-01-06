#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
import cv2
import numpy as np
import os.path as osp
from PIL import Image
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


def output_board_configs_to_csv(
        csvpath,
        dict_label,
        squareL,
        markerL,
        squareNumX,
        squareNumY,
        boardSizeX,
        boardSizeY,
        tb,
        lr):

    with open(csvpath, 'w', newline='') as csvfile:
        config_writer = csv.writer(csvfile, lineterminator='\n')
        config_writer.writerow(['parameter', 'value'])
        config_writer.writerow(['dict_label', dict_label])
        config_writer.writerow(['square_length', squareL])
        config_writer.writerow(['marker_length', markerL])
        config_writer.writerow(['num_squares_x', squareNumX])
        config_writer.writerow(['num_squares_y', squareNumY])
        config_writer.writerow(['board_size_x', boardSizeX])
        config_writer.writerow(['board_size_y', boardSizeY])
        config_writer.writerow(['margin_tb', tb])
        config_writer.writerow(['margin_lr', lr])


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
            outcsv=False):

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
    boardImage = board.draw(
        (boardPixX, boardPixY), None, 0, 1)

    # add the margin to the image
    boardImage_margin = np.asarray(
        add_margin(Image.fromarray(boardImage), tb_pixels, lr_pixels))

    board_path = osp.join(board_dirpath, board_filename)
    cv2.imwrite(board_path, boardImage_margin)
    imshow(img_path=board_path)

    if outcsv:
        # remove the extention from the board_name
        output_board_configs_to_csv(
            osp.join(board_dirpath, board_filename.split('.')[0]+'.csv'),
            dict_label,
            squareL,
            markerL,
            squareNumX,
            squareNumY,
            boardSizeX,
            boardSizeY,
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
        outcsv=args.outcsv)
