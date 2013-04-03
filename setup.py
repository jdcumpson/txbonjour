# -*- coding: utf-8 -*-
'''
Created on 2013-02-08

@author: Noobie
'''
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
    
from txbonjour import version

setup(
    name='txbonjour',
    version=version,
    description='An easy way to use the bonjour/avahi service with Twisted.',
    author='jdcumpson',
    author_email='cumpsonjd@gmail.com',
    zip_safe=False,
    url='https://github.com/jdcumpson/txbonjour',
    install_requires=[
        'pybonjour',
        ],
    packages=find_packages(exclude=[]),
    include_package_data=True,
    entry_points={'console_scripts': []}
)

