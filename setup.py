from setuptools import setup, find_packages
import os
import sys

setup(
    name = "pyjpeg",
    packages = find_packages(),
    include_package_data = True,
    version = '0.0.0',
    zip_safe = False,
    description = "A Python library for reading jpeg images",
    author = "",
    author_email = "",
    url = "https://github.com/pydicom/pynetdicom3",
    license = "LICENCE.txt",
    keywords = "python jpeg jpeg-ls jpeg2000",
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Software Development :: Libraries",
    ],
    install_requires = [
        "numpy"
    ]
)
