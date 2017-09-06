# Image Resizer

Script resize original image by scale or height or width with preservation of proportions.

### How to Install

Python 3 should be already installed. Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

```bash
git clone https://github.com/velios/12_image_resize.git
pip install -r requirements.txt # alternatively try pip3
```

### How to use
#####Sample run
```bash
$ python 3 test.jpg -s 2
Result save to file test__50x500.jpg
```
#####Arguments
```sh
positional arguments:
  original                               path to original image
  
optional arguments:
  --width WIDTH, -w WIDTH                width of result image
  --height HEIGHT, -h HEIGHT             height of result image
  --scale SCALE, -s SCALE                scale for resize result image
  --output OUTPUT, -o OUTPUT             name of result file without extension
  --help                                 show this help message and exit
```


Remember, it is recommended to use [virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/) for better isolation.

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
