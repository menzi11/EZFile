#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = "ezfile",
    version = "0.0.3",
    keywords = ["pip", "datacanvas", "eds", "xiaoh"],
    description = "a easy file operation lib",
    long_description = "a easy file operation lib",
    license = "MIT Licence",

    url = "http://threebodytech.com",
    author = "Meng Ke",
    author_email = "m1engk1e@gmail.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = [ "requests" ]
)