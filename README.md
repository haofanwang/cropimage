# cropimage

[![Colab](https://camo.githubusercontent.com/84f0493939e0c4de4e6dbe113251b4bfb5353e57134ffd9fcab6b8714514d4d1/68747470733a2f2f636f6c61622e72657365617263682e676f6f676c652e636f6d2f6173736574732f636f6c61622d62616467652e737667)](https://colab.research.google.com/drive/18jqXa1V-v5FXoCcY2MVg3FC3CFcOAk63?usp=sharing) [![PyPI version](https://badge.fury.io/py/cropimage.svg)](https://badge.fury.io/py/cropimage) ![Python](https://img.shields.io/badge/python-v3.5.0+-success.svg) [![Downloads](https://static.pepy.tech/personalized-badge/cropimage?period=month&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/cropimage) [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/haofanwang/cropimage/issues)

CropImage is a simple toolkit for image cropping. Different from other projects that mainly tackle face region, we extend to all kinds of images such as landscape. We support horizontal and portrait size and generate a square output.

<p align="center"><img title="crop_example" src="https://github.com/haofanwang/cropimage/raw/main/assets/example.png"></p>

## Installation
~~~sh
pip install cropimage
~~~

## Get Started
~~~python
from cropimage import Cropper

cropper = Cropper()

# Get a Numpy array of the cropped image
# Set completeness to be True if you expect the 'face' to be focused rather than 'person'
# Set target_size to be a tuple (size, size), only square output is supported now
result = cropper.crop('./images/input.jpg')

# Save the cropped image
cv2.imwrite('cropped.jpg', result)
~~~

## More Results
<p align="center"><img title="crop_example" src="https://github.com/haofanwang/cropimage/raw/main/assets/example1.png"></p>

## Contributing
If you find any issue of this project, feel free to open an issue or contribute!
