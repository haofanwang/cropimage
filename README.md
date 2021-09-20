# cropimage

[![PyPI version](https://badge.fury.io/py/cropimage.svg)](https://badge.fury.io/py/cropimage) 

cropimage is a simple toolkit for image cropping. Different from other projects that mainly tackle face region, we extend to all kinds of images such as landscape. We support horizontal and portrait size and generate a square output.

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
