from setuptools import setup, find_packages
import os
import json
from datetime import datetime
from rickled import __version__ as ver

here = os.path.abspath(os.path.dirname(__file__))

version_file = os.path.join(here, 'version.json')
if os.path.isfile(version_file):
    with open(version_file, "r") as f:
        version = json.load(f)
        version_name = '{major}.{minor}.{patch}'.format(**version)
else:
    version_name = ver

# Get the long description from the README file
long_description_file = os.path.join(here, 'pip_description.md')
if os.path.isfile(long_description_file):
    with open(long_description_file, "r", encoding='utf-8') as f:
        long_description = f.read()
        long_description = long_description.format(pypi_metdata_release_date=datetime.today().strftime('%Y-%m-%d'), pypi_metdata_version_number=version_name)
else:
    long_description = "It's Rickle Pick!"

if os.path.isfile(os.path.join(here, 'requirements.txt')):
    with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
        pipreq = f.readlines()
        # remove pip flag
        if '-i http' in pipreq[0]:
            pipreq.pop(0)
else:
    pipreq = ['pyyaml']


setup(
    name="rickled",
    version=version_name,
    description='Tools for pickling Python objects in completely different way',
    long_description_content_type='text/markdown',
    long_description=long_description,
    license='Apache 2.0',
    keywords = ['Pickle', 'Python'],
    author='Zipfian Science',
    author_email='about@zipfian.science',
    zip_safe=False,
    # url='https:/zipfian.science',
    download_url='https://github.com/Zipfian-Science/rickled/archive/v_01.tar.gz',
    packages=find_packages(".", exclude=("tests", "dist", "deploy", "egg-info")),
    include_package_data=True,
    install_requires=pipreq,
    package_dir={'.': 'rickled'},
    package_data={
        "": ["*.yaml",],
    },
    classifiers=[
            'Intended Audience :: Science/Research',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
            'Topic :: Scientific/Engineering :: Artificial Intelligence']
)
