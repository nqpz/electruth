#!/usr/bin/env python
from distutils.core import setup
import os

ginfo_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                          'electruth', 'generalinformation.py')
execfile(ginfo_file)

readme = open('README.txt').read()
conf = dict(
    name=program_name,
    version=version_text,
    author='Niels Serup',
    author_email='ns@metanohi.org',
    packages=['electruth', 'electruth.external'],
    scripts=['scripts/electruth'],
    requires=['qvikconfig'],
    url='http://metanohi.org/projects/electruth/',
    license='GPLv3+',
    description=program_description,
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: End Users/Desktop',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: GNU General Public License (GPL)',
                 'License :: DFSG approved',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
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

try:
    # setup.py register wants unicode data..
    conf['long_description'] = readme.decode('utf-8')
    setup(**conf)
except Exception:
    # ..but setup.py sdist upload wants byte data
    conf['long_description'] = readme
    setup(**conf)
