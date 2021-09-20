import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name="cropper",
  version="0.0.1",
  author="Haofan Wang",
  author_email="haofanwang.ai@gmail.com",
  description="A simple toolkit for detecting and cropping main body from pictures.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/haofanwang/cropper",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: Apache-2.0 License",
  "Operating System :: OS Independent",
  ],
)