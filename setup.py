import pathlib
from setuptools import setup

try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
with open(f"{HERE}/README.md") as readme_fs:
    README = readme_fs.read()


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


install_reqs = parse_requirements("requirements.txt")
setup(
    name="howto-cli",
    description="Multi-scenarios CLI tool for tutorials, guides or stories.",
    version="0.0.5",
    packages=["howto"],
    author="flavienbwk",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    long_description=README,
    long_description_content_type="text/markdown",
    package_data={"": ["README.md", "INTRODUCTION.md"]},
    include_package_data=True,
    install_requires=install_reqs,
    entry_points={"console_scripts": ["howto=howto.__main__:run"]},
)
