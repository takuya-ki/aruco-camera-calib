#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import cv2
import os.path as osp

import utils

aruco = cv2.aruco


def detect_marker_image(
        dictionary,
        img_path,
        isShow=True,
        isSave=True,
        savename=None,
        savedirpath=None):

    frame = cv2.imread(img_path)
    corners, ids, _ = aruco.detectMarkers(frame, dictionary)
    if ids is None:
        print("Not detect any markers.")
        return 0
    aruco.drawDetectedMarkers(frame, corners, ids, (0, 255, 0))
    if isSave:
        if savename is None or savedirpath is None:
            print("Error: Please specify save marker path.")
            return -1
        saveimg_path = osp.join(
            savedirpath, str(savename)+'.png')
        cv2.imwrite(saveimg_path, frame)
    if isShow:
        utils.imshow(img=frame, width=1000)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    args = utils.get_options()

    imgs_dirpath = args.in_dir
    imgs_dirpath = osp.join(
        osp.dirname(__file__),
        imgs_dirpath)
    if not osp.exists(imgs_dirpath):
        print("Not found directory for image files...")
        exit()

    # delete files under save dir and make save dir
    resimg_dirpath = osp.join(
        osp.dirname(__file__), args.out_dir)
    if osp.exists(resimg_dirpath):
        # recognize any extentions
        resimg_paths, resimg_names = utils.get_file_paths(
            resimg_dirpath, '*')
        [os.remove(mpath) for mpath in resimg_paths]
    os.makedirs(resimg_dirpath, exist_ok=True)

    img_paths, img_names = utils.get_file_paths(imgs_dirpath, '*')
    for i, (img_path, img_name) in enumerate(zip(img_paths, img_names)):
        if not (osp.splitext(img_name)[1] in ['.png', '.jpg', '.bmp']):
            print("Check file extention: "+img_path)
            continue
        detect_marker_image(
            utils.get_aruco_dict(args.aruco_dict),
            img_path,
            savename=i,
            savedirpath=resimg_dirpath)
