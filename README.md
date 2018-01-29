# Face Splitter

Python 3 script to detect faces in OpenCV and split them into three parts.

![Face Splitter Screenshot](https://raw.githubusercontent.com/fdb/face-splitter/master/.github/screenshot.jpg)

To install:

    brew install python3 opencv
    echo /usr/local/opt/opencv/lib/python3.6/site-packages >> /usr/local/lib/python3.6/site-packages/opencv3.pth

To run:

    python split_faces.py INPUT_DIR OUTPUT_DIR [start_index]

If you don't provide a start index, images will start at 1.

To resize the images in the output dir I use ImageMagick:

    mogrify -path resized -resize 500x out/*.jpg -v
