# aruco-camera-calib

A camera caribration tool using opencv ArUco module

## Description

An example for camera calibration using ArUco library through OpenCV

## Features

- AR library, [ArUco](https://www.uco.es/investiga/grupos/ava/node/26)
- Computer Vision library, [OpenCV](https://opencv.org/)
- ArUcoboard

<img src="./board/sample_board.png" width=50%　align=left>

## Requirements

- Anaconda with jupyter notebook
- python 3.6.0
- opencv-contrib

## Installation

	$ git clone git@github.com:takuya-ki/aruco-camera-calib.git
	$ cd aruco-camera-calib
    $ conda install jupyter
    $ conda install -c michael_wild opencv-contrib

## Usage

#### Create aruco markers

    # execute lines of marker_creation.ipynb

#### Create aruco board needed for calibration

    # execute lines of board_creation.ipynb 

#### Detect aruco board in input images

    # execute lines of board_detection.ipynb

#### Calibrate camera with images capturing aruco board

    # execute lines of board_calibration.ipynb

## Author/Contributors

[Takuya Kiyokawa](http://qiita.com/takuya-ki)

## License

This software is released under the MIT License, see LICENSE.
