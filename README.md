# cropimage

[![PyPI version](https://badge.fury.io/py/cropimage.svg)](https://badge.fury.io/py/cropimage) 

This is a simple toolkit for cropping main body from pictures. Besides of face cropping, our project supports for all kind of images.

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
# Set completeness to be False if you expect the 'person' to be complete rather than 'face'
cropped_array = cropper.crop('./images/input.jpg', completeness=True, target_size=(500,500))

# Save the cropped image
cv2.imwrite('cropped.jpg', result)
~~~

## More Results
<p align="center"><img title="crop_example" src="https://github.com/haofanwang/cropimage/raw/main/assets/example1.png"></p>

## Contributing
If you find any issue of this project, feel free to open an issue or contribute!
