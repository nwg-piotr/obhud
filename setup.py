from setuptools import setup

setup(
    name="obhud",
    version="0.1.0",
    author="Piotr Miller",
    author_email="nwg.piotr@gmail.com",

    packages=["obhud"],

    include_package_data=True,

    # Details
    url="https://bitbucket.org/nwg-piotr/obhud/src/master",

    license='gpl3',
    description="Script for handling laptop-specific keys in Openbox",

    long_description=open("README.txt").read(),
    install_requires=[
          'xorg-xbacklight', 'xorg-xrandr', 'libxrandr', 'alsa-utils', 'python', 'python-pmw', 'python-pillow', 'python-psutil',
      ],
    platforms=['any'],
)