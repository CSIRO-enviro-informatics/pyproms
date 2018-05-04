#!/usr/bin/env python
from setuptools import setup
import io

with io.open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='pyproms',
    packages=['pyproms'],
    version='1.4.0',
    description='PyPROMS is a client library to make provenance documents and submit them to a PROMS Server instance',
    author='Nicholas Car',
    author_email='nicholas.car@csiro.au',
    url='https://github.com/CSIRO-enviro-informatics/pyproms',
    download_url='https://github.com/CSIRO-enviro-informatics/pyproms/archive/master.zip',
    license='LICENSE.txt',
    keywords=['rdf', 'prov', 'prov-o', 'proms', 'proms-o', 'provenance'],
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    project_urls={
        'Bug Reports': 'https://github.com/CSIRO-enviro-informatics/pyproms/issues',
        'Source': 'https://github.com/CSIRO-enviro-informatics/pyproms/',
    },
    python_requires='>=3.0',
    install_requires=[
        'rdflib >= 4.0.0',
        'requests'
    ],
)

 # use http://peterdowns.com/posts/first-time-with-pypi.html