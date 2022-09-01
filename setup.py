#!/usr/bin/env python3

from setuptools import setup

setup(
    entry_points={
        'console_scripts': ['cvs-makequiz=cvs.command_line:main'],
    }
)
