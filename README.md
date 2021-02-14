# Amaicha
Movie generator using MoviePy, OpenCV2 and Numpy.
![alt-img](./wallpaper.jpg)

## Installation
#### Download, create a virtual environment and install al dependencies:
```bash
virtualenv -p python3 .env
source .env/bin/activate
pip install -r requirements.txt
```

## Usage
#### First, download a some `.mp4` files into the `./media` directory.
#### Then, download some `.jpeg` files into the `./media` directory.
#### Then, download a `.mp3` into the `./media` directory.
#### Activate the virtual environment and build the video:
```bash
source .env/bin/activate
python3 ./bin/build.py
```
#### The output will be available on the `./render` directory.
