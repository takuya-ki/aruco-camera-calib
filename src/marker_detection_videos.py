#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import cv2
import os.path as osp

import utils

aruco = cv2.aruco


def detect_marker_video(
        dictionary,
        video_path,
        isShow=True,
        isSave=True,
        savename=None,
        savedirpath=None):

    cap = cv2.VideoCapture(video_path)
    cnt = 0
    while(cap.isOpened()):
        cnt += 1
        ret, frame = cap.read()
        if not ret:
            break
        corners, ids, _ = aruco.detectMarkers(frame, dictionary)
        if ids is None:
            continue
        aruco.drawDetectedMarkers(frame, corners, ids, (0, 255, 0))
        if isSave:
            if savename is None or savedirpath is None:
                print("Error: Please specify save marker path.")
                return -1
            saveimg_path = osp.join(
                savedirpath, str(savename)+'_'+str(cnt)+'.png')
            cv2.imwrite(saveimg_path, frame)
        if isShow:
            utils.imshow(img=frame, wsec=10, width=1000)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    args = utils.get_options()

    videos_dirpath = args.in_dir
    videos_dirpath = os.path.join(
        osp.dirname(__file__),
        videos_dirpath)
    if not osp.exists(videos_dirpath):
        print("Not found directory for video files...")
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

    video_paths, video_names = utils.get_file_paths(videos_dirpath, '*')
    for i, (v_path, v_name) in enumerate(zip(video_paths, video_names)):
        if not (os.path.splitext(video_name)[1] in ['.mp4', '.avi']):
            print("Check file extention: "+v_path)
            continue
        detect_marker_video(
            utils.get_aruco_dict(args.aruco_dict),
            v_path,
            savename=i,
            savedirpath=resimg_dirpath)
