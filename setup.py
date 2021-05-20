import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
        name="bytecodemacro",
        version="1.0.0",
        description="a macro library that expoes the bytecode of python",
        long_description=README,
        long_description_content_type="text/markdown",
        url="https://github.com/Glubs9/bytecodemacro",
        author="glubs9",
        author_email="jonte.fry@gmail.com", #please no spam
        license="GPLv3",
        classifiers=[
            "Programming Language :: Python :: 3.9.0",
        ],
        packages=find_packages(), #can't be bothered to do properly
        include_package_data=True #i'm not sure what this does
        #i'm not too sure how to specify entry_points
)
