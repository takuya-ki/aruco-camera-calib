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
- pandas

## Installation

	$ git clone git@github.com:takuya-ki/aruco-camera-calib.git
	$ cd aruco-camera-calib
    $ conda activate your_conda_env
    $ conda install jupyter
    $ conda install -c michael_wild opencv-contrib

## Usage

    $ cd jupyter # important because os.getcwd() are used

#### Create aruco markers

    # execute lines of marker_creation.ipynb

#### Create aruco board needed for calibration

    # execute lines of board_creation.ipynb 

#### Detect aruco board in input images

    # execute lines of board_detection.ipynb

#### Calibrate camera with images capturing aruco board

    # set csv file path containing board configuration parameters
    # execute lines of board_calibration.ipynb

## Author

[Takuya Kiyokawa](https://takuya-ki.github.io/)

## License

This software is released under the MIT License, see [LICENSE](./LICENSE).
