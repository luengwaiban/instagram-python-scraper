#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='instagram-python-scraper',
    version='1.0.1',
    description=(
        'A instagram scraper wrote in python. Various actions supported.Enjoy it!'
    ),
    long_description='A instagram scraper wrote in python. Various actions supported.Similar to instagram-php-scraper.Usages are in example.py. Enjoy it!',
    author='leungwaiban',
    author_email='407261380@qq.com',
    maintainer='leungwaiban',
    maintainer_email='407261380@qq.com',
    include_package_data=True,
    license='MIT',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/luengwaiban/instagram-python-scraper',
    install_requires=[
        'certifi>=2019.3.9',
        'chardet>=3.0.4',
        'idna>=2.8',
        'requests>=2.21.0',
        'urllib3>=1.24.3'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)