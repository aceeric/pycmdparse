from setuptools import setup, find_packages

NAME = 'pycmdparse'
VERSION = '1.0.0'
DESCRIPTION = "A Python command line arg parser, and usage instructions generator"
LONG_DESCRIPTION = """\
For authors of command-line utilities. Simplifies: 1) Defining command-line options
and parameters, 2) Parsing the command line, and 3) Displaying usage instructions
to the console.

Utility developers will 1) Subclass a module-defined class, 2) Include a YAML spec
in the subclass to define the utility's options and usage, and 3) Invoke the module
arg parser. When a user runs the developer's utility, if the command line is valid
according to the YAML schema, then the supplied args are injected into the subclass
by the parser. Otherwise errors are automatically displayed to the console.

If the user specifies '-h' or '--help' on the command line, then usage instructions
are displayed as defined in the YAML, in a form generally consistent with 'nix-style
usage instructions. Specifically, displays summary usage, detailed options and params
(including categorized options), positional params, and examples.
"""
AUTHOR = "Eric Ace"
AUTHOR_EMAIL = 'ericace@protonmail.com'
LICENSE = "Public Domain"
PLATFORMS = "Any"
URL = "https://github.com/aceeric/pycmdparse"
DOWNLOAD_URL = "TBD"
KEYWORKDS="arg argument parse commandline command line usage instructions console utility"
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: Public Domain",
    "Operating System :: OS Independent",
    "Environment :: Console",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Text Processing :: Markup",
]
PACKAGES=['pycmdparse']
REQUIRES=['PyYAML==5.1b3']
PYTHON_REQUIRES='>=3.6'
TESTS_REQUIRE=["pytest"]
setup(
    name=NAME,
    version=VERSION,
    packages=PACKAGES,
    install_requires=REQUIRES,
    python_requires=PYTHON_REQUIRES,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    license=LICENSE,
    keywords=KEYWORKDS,
    url=URL,
    classifiers=CLASSIFIERS,
    tests_require=TESTS_REQUIRE,
)
