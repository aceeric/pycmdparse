from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pycmdparse',
    version='1.0.0',
    packages=find_packages(), ##['pycmdparse'],
    install_requires=['PyYAML==5.1b3'],
    python_requires=">=3.6",
    author='Eric Ace',
    author_email='ericace@protonmail.com',
    description='A Python command line arg parser and usage instructions generator',
    license="Public Domain",
    long_description=long_description,
    keywords="arg parse command-line command line usage instructions",
    url='https://github.com/aceeric/pycmdparse',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
