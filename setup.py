#!/usr/bin/python3
# -*-coding:utf-8 -*-
# Reference:**********************************************
# @Time     : 2020/7/4 9:30
# @Author   : Raymond Luo
# @File     : setup.py.py
# @User     : luoli
# @Software: PyCharm
# Reference:**********************************************
import setuptools
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="code-similarity",  # Replace with your own username
    version="0.0.3",
    author="Raymond Luo",
    author_email="luolinhao1998@gmail.com",
    description="An out of box code and text similarity computation package",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/RManLuo/code-similarity",
    install_requires=[
        'jieba>=0.42.1',
        'gensim>=3.8.0'
    ],
    packages=['CodeSimilarity'],
    include_package_data=True,
)
