import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
        name="bytecodemacro",
        version="2.0.1", #whoops accidentally did too many versions
        description="a macro library that expoes the bytecode of python",
        long_description=README,
        long_description_content_type="text/markdown",
        url="https://github.com/Glubs9/bytecodemacro",
        author="glubs9",
        author_email="jonte.fry@gmail.com", #please no spam
        license="GPLv3",
        #classifiers=[ #apparnetly this is not a valid classifier idk how this works
        #    "Programming Language :: Python :: 3.9",
        #],
        packages=find_packages() #can't be bothered to do properly
        #i'm not too sure how to specify entry_points (or if i need to)
)
