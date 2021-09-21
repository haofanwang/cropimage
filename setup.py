import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name="cropimage",
  version="0.0.4",
  author="Haofan Wang",
  author_email="haofanwang.ai@gmail.com",
  description="A simple toolkit for detecting and cropping main body from pictures.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/haofanwang/cropimage",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: Apache Software License",
  "Operating System :: OS Independent",
  ],
)
