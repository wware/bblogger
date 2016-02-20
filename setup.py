#!/usr/bin/env python

from distutils.core import setup

setup(
    name='bblogger',
    version='1.0',
    description='Logger spanning machines on a subnet',
    author='Will Ware',
    author_email='wware@alum.mit.edu',
    url='http://willware.net/bblogger/',
    packages=['bblogger'],
    install_requires=[
        'Flask',
        'requests',
    ],
    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
)
