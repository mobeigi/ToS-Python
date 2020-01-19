from setuptools import setup, find_packages
from townofsalem.__meta__ import *

setup(
    name=__title__,
    version=__version__,
    description=__description__,
    packages=find_packages(),
    license=__license__,
    author=__author__,
    author_email=__email__,
    url=__website__
)