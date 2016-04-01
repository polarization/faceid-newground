import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="faceid-newground",
    version="0.0.1",
    author="KAS Team in Megvii",
    author_email="kas@megvii.com",
    description="faceid newground",
    packages=['newground', 'newground/resources', 'newground/common'],
    long_description=read('README'),
)
