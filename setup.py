from setuptools import setup, find_packages

setup(
    name="wnghub",
    version="0.0.1",
    author="Brighton Balfrey",
    author_email="balfrey@usc.edu",
    packages=find_packages(),
    install_requires=[
        "marshmallow==3.9.1",
        "click==7.1.2",
    ],
)
