"""
This is the setup module for the python_licensing package.

The python_licensing package provides functionality for licensing
a Python script and providing licenses via a licensing server.
It includes the necessary setup configuration for package distribution.

Author: Franz Ludwig Kostelezky
Email: info@kostelezky.com
"""

from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setup(
    name='python_licensing',
    version='%VERSION_PLACEHOLDER%',
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    author='Franz Ludwig Kostelezky',
    author_email='info@kostelezky.com',
    description='License your python script and provide licenses via a licensing server.',
    url='https://github.com/flemk/python-licensing',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
