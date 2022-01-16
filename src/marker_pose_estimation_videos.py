#!/usr/bin/env python3

import os
import cv2
import pickle
import os.path as osp

import utils

aruco = cv2.aruco


def pose_esitmation(
        frame,
        dictionary,
        marker_length,
        camera_matrix,
        dist_coeffs):
    """Estimates poses of detected markers in the frame."""

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    parameters = aruco.DetectorParameters_create()
    corners, ids, _ = aruco.detectMarkers(
        gray,
        dictionary,
        parameters=parameters,
        cameraMatrix=camera_matrix,
        distCoeff=dist_coeffs)
    if ids is None:
        print("Not detect any markers.")
        return None

    # if markers are detected
    if len(corners) > 0:
        for i in range(0, len(ids)):
            # estimate pose of each marker and return the values rvec and tvec
            rvec, tvec, _ = aruco.estimatePoseSingleMarkers(
                corners[i], marker_length, camera_matrix, dist_coeffs)
            # draw a square around the markers
            aruco.drawDetectedMarkers(frame, corners)
            # draw Axis
            aruco.drawAxis(frame, camera_matrix, dist_coeffs, rvec, tvec, 0.01)
    return frame


def estimate_marker_pose_video(
        dictionary,
        marker_length,
        video_path,
        camera_matrix,
        dist_coeffs,
        isShow=True,
        isSave=True,
        savename=None,
        savedirpath=None):
    """Reads a video and saves and/or shows the result images."""

    cap = cv2.VideoCapture(video_path)
    cnt = 0
    while(cap.isOpened()):
        cnt += 1
        ret, frame = cap.read()
        if not ret:
            break
        frame = pose_esitmation(
            frame, dictionary, marker_length, camera_matrix, dist_coeffs)
        if frame is None:
            continue
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
    videos_dirpath = osp.join(
        osp.dirname(__file__),
        videos_dirpath)
    if not osp.exists(videos_dirpath):
        print("Not found directory for video files...")
        exit()

    cam_param_path = osp.join(
        osp.dirname(__file__), args.camera_param_path)
    with open(cam_param_path, 'rb') as f:
        camera_params = pickle.load(f)
    cameramat, distcoeff, rvecs, tvecs, stdIn, stdEx = camera_params

    # delete files under save dir and make save dir
    resimg_dirpath = osp.join(
        osp.dirname(__file__), args.out_dir)
    if osp.exists(resimg_dirpath):
        # recognize any extentions
        resimg_paths, resimg_names = utils.get_file_paths(
            resimg_dirpath, '*')
        [os.remove(mpath) for mpath in resimg_paths]
    os.makedirs(resimg_dirpath, exist_ok=True)

    marker_length = 0.02  # [m]
    video_paths, video_names = utils.get_file_paths(videos_dirpath, '*')
    for i, (v_path, v_name) in enumerate(zip(video_paths, video_names)):
        if not (osp.splitext(v_name)[1] in ['.mp4', '.avi']):
            print("Check file extention: "+v_path)
            continue
        estimate_marker_pose_video(
            utils.get_aruco_dict(args.aruco_dict),
            marker_length,
            v_path,
            cameramat,
            distcoeff,
            savename=i,
            savedirpath=resimg_dirpath)
