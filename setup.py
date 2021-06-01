#this file uploads the source to PyPi
    #most of this code is taken from https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56

import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
        name="bytecodemacro",
        version="2.1.0",
        description="a macro library that expoes the bytecode of python",
        long_description=README,
        long_description_content_type="text/markdown",
        url="https://github.com/Glubs9/bytecodemacro",
        author="glubs9",
        author_email="jonte.fry@gmail.com", #please no spam
        license="GPLv3",
        packages=find_packages()
)
