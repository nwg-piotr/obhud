from setuptools import setup

setup(
    name="obhud",
    version="0.1.7",
    author="Piotr Miller",
    author_email="nwg.piotr@gmail.com",

    packages=["obhud"],

    include_package_data=True,

    # Details
    url="https://github.com/nwg-piotr/obhud",

    license='GPL3',
    description="Script for handling laptop-specific keys and events in Openbox",

    long_description=open("README.txt").read(),
    install_requires=[
        'xorg-xbacklight', 'xorg-xrandr', 'libxrandr', 'alsa-utils', 'python', 'python-pmw', 'python-pillow',
        'python-psutil', 'xf86-input-synaptics','ffmpeg', 'python-lxml'
    ],
    platforms=['any'],
)
