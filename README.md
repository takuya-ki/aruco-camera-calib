# aruco-camera-calib

Camera caribration tool with ArUco library

## Features

- Programs are executed on [Jupyter Notebook](https://jupyter.org/)
- Use AR library, [ArUco](https://www.uco.es/investiga/grupos/ava/node/26)
- Use Computer Vision library, [OpenCV](https://opencv.org/)
- Calibration with ArUcoboard

<div align="center">
    <img src="board/sample_board.png", width="30%">
</div>

## Requirements

- Anaconda
- python 3.6.0 (tested)
- opencv-contrib
- jupyter

## Installation

	$ git clone git@github.com:takuya-ki/aruco-camera-calib.git
	$ cd aruco-camera-calib
    $ conda activate your_conda_env
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

## Author

[Takuya Kiyokawa](http://qiita.com/takuya-ki)

## License

This software is released under the MIT License, see LICENSE.
