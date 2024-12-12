from setuptools import setup, find_packages

setup(
    name="car-music-player",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pygame==2.5.2",
        "RPi.GPIO==0.7.1",
        "watchdog==3.0.0",
    ],
)