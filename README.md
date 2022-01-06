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

## Requirements (tested)

- Python 3.7.3
  - numpy 1.21.5
  - pickle-mixin 1.0.2
  - matplotlib 3.1.1
  - opencv-contrib-python 3.4.2.17
  - pandas 1.1.0
  - pillow 5.4.1

## Installation

    $ git clone git@github.com:takuya-ki/aruco-camera-calib.git
    $ pip install -r requirements.txt

## Usage

    $ python scripts/marker_creation.py --dict 'DICT_4X4_250' --num_pixels 64 --num_markers 5 --out_dir ../data/markers/
    $ python scripts/board_creation.py    # to create a board picture
    $ python scripts/board_detection.py   # to detect a board in images
    $ python scripts/board_calibration.py # to calibration with images

## Author

[Takuya Kiyokawa](https://takuya-ki.github.io/)

## License

This software is released under the MIT License, see [LICENSE](./LICENSE).
