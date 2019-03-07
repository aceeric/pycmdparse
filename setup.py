from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pycmdparse',
    version='1.0.0',
    author='Eric Ace',
    author_email='ericace@protonmail.com',
    description='A Python command line arg parser and usage instructions generator',
    long_description=long_description,
    #long_description_content_type="text/markdown",
    url='https://github.com/aceeric/pycmdparse',
    packages=['pycmdparse'],
    install_requires=['PyYAML==5.1b3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
