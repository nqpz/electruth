#!/usr/bin/env python3
from distutils.core import setup
import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import electruth.generalinformation as ginfo

setup(
    name=ginfo.program_name,
    version=ginfo.version_text,
    author='Niels Serup',
    author_email='ns@metanohi.org',
    packages=['electruth', 'electruth.external'],
    scripts=['scripts/electruth'],
    requires=['qvikconfig'],
    url='http://metanohi.org/projects/electruth/',
    license='GPLv3+',
    description=ginfo.program_description,
    long_description=open('README.txt').read(),
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: End Users/Desktop',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: GNU General Public License (GPL)',
                 'License :: DFSG approved',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3.1',
                 'Environment :: Console',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Education',
                 'Intended Audience :: End Users/Desktop',
                 'Intended Audience :: Science/Research',
                 'Topic :: Utilities',
                 'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
                 'Topic :: Education',
                 'Topic :: Software Development :: Libraries :: Python Modules'
                 ]
)
