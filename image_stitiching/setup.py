"""
Skysight image stitching

"""

from setuptools import setup

setup(
    name='skysight-stitch',
    version='0.1.0',
    packages=['stitcher'],
    include_package_data=True,
    install_requires=[
        'opencv-contrib-python',
        'imutils',
        'argparse',
    ],
    entry_points={
        'console_scripts': [
            'stitch=stitcher.__main__:main'
        ]
    },
)
