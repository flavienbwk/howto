from setuptools import setup

try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

install_reqs = parse_requirements('requirements.txt')
setup(
    name='howto-cli',
    version="0.0.1",
    packages=['howto'],
    author="flavienbwk",
    license="MIT",
    package_data={'': ['*.md']},
    include_package_data=True,
    install_requires=install_reqs,
    entry_points={"console_scripts": ["howto=howto.__main__:run"]},
)
