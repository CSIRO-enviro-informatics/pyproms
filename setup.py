from setuptools import setup

setup(
    name='pyproms',
    packages=['pyproms'],
    version='1.2.0',
    author='Nicholas Car',
    author_email='nicholas.car@ga.gov.au',
    url='https://bitbucket.csiro.au/projects/EIS/repos/proms-clients-python',
    download_url='https://bitbucket.csiro.au/rest/archive/latest/projects/EIS/repos/proms-clients-python/archive?format=zip',
    license='LICENSE.txt',
    description='PyPROMS is a client library to make PROV and PROMS documents and submit them to a PROMS Server instance',
    keywords=['rdf', 'prov', 'prov-o', 'proms', 'proms-o', 'provenance'],
    long_description='''
PyProms is a library of classes that helps Python coders generate
provenance reports using the PROV and PROMS Ontologies.

The PROMS Ontology is at http://promsns.org/def/proms

The Python classes match the PROMS-O OWL classes, for example the Python class
'Report' matches the PROMS-O 'Report' class.

PyProms is expected to be extended so if you need so add to it to get your
reporting job done, please do so! If you're really nice, you might consider
letting the author, Nicholas Car <nicholas.car@ga.gov.au> know what you've
added as this will help with further releases.
    ''',
    install_requires=['rdflib >= 4.0.0'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
    ],
)

#use http://peterdowns.com/posts/first-time-with-pypi.html