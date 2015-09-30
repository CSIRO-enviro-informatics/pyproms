from setuptools import setup
#from distutils.core import setup

setup(
    name='pyproms',
    packages=['pyproms'],
    version='1.1.7',
    author='Nicholas Car',
    author_email='nicholas.car@csiro.au',
    url='https://stash.csiro.au/projects/EIS/repos/proms-clients-python',
    download_url='https://stash.csiro.au/plugins/servlet/archive/projects/EIS/repos/proms-clients-python?at=refs%2Fheads%2Fmaster',
    license='LICENSE.txt',
    description='PyPROMS is a client library to make PROV and PROMS documents and submit them to a PROMS server instance',
    keywords=['rdf', 'prov', 'prov-o', 'proms', 'proms-o', 'provenance'],
    long_description='''
PyProms is a library of classes that helps Python coders generate
provenance reports using the PROV and PROMS Ontologies. It also has a
function to send a Report to an instances of the PROMS Server for
storage.

The classes match the PROMS-O OWL classes, for example the Python class
'Report' matches the PROMS-O 'Report' class.

PyProms is expected to be extended so if you need so add to it to get your
reporting job done, please do so! If you're really nice, you might consider
letting the author, Nicholas Car <nicholas.car@csiro.au> know what you've
added as this will help with further releases.
    ''',
    install_requires=['rdflib >= 3.0.0'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
    ],
)

#use http://peterdowns.com/posts/first-time-with-pypi.html