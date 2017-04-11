# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='partyparrots',
    version='0.1.0',
    author=u'Party Parrots',
    packages=find_packages(),
    include_package_data=True,
    license='MIT, see LICENSE',
    zip_safe=False,
    install_requires=[
        'Django==1.10.1',
    ]
)
