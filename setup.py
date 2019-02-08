# -*- coding: utf-8 -*-

# @author: 0xSaiyajin

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="searchxmlyandex",
    version="0.0.13",
    author="0xSaiyajin",
    description="YandexXMLSearch API, XML to JSON converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/0xSaiyajin/searchxmlyandex",
    packages=setuptools.find_packages(),
    install_requires = ['requests'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
