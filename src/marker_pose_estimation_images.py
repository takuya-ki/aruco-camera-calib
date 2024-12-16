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
    parameters = aruco.DetectorParameters()
    corners, ids, _ = aruco.detectMarkers(
        gray,
        dictionary,
        parameters=parameters)
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
    return frame


def estimate_marker_pose_image(
        dictionary,
        marker_length,
        img_path,
        camera_matrix,
        dist_coeffs,
        isShow=True,
        isSave=True,
        savename=None,
        savedirpath=None):
    """Reads an image and saves and/or shows the result images."""

    frame = cv2.imread(img_path)
    frame = pose_esitmation(
        frame, dictionary, marker_length, camera_matrix, dist_coeffs)
    if frame is None:
        return
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
    img_paths, img_names = utils.get_file_paths(imgs_dirpath, '*')
    for i, (img_path, img_name) in enumerate(zip(img_paths, img_names)):
        if not (osp.splitext(img_name)[1] in ['.png', '.jpg', '.bmp']):
            print("Check file extention: "+img_path)
            continue
        estimate_marker_pose_image(
            utils.get_aruco_dict(args.aruco_dict),
            marker_length,
            img_path,
            cameramat,
            distcoeff,
            savename=i,
            savedirpath=resimg_dirpath)
