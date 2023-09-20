from setuptools import setup, find_packages
import os
from datetime import datetime

here = os.path.abspath(os.path.dirname(__file__))

about = {}

with open(os.path.join(here, "rickled", "__version__.py")) as f:
    exec(f.read(), about)

# Get the long description from the README file
long_description_file = os.path.join(here, 'pip_description.md')
if os.path.isfile(long_description_file):
    with open(long_description_file, "r", encoding='utf-8') as f:
        long_description = f.read()
        long_description = long_description.format(pypi_metdata_release_date=datetime.today().strftime('%Y-%m-%d'),
                                                   pypi_metdata_version_number=about["__version__"])
else:
    long_description = "It's Rickle Pick!"

if os.path.isfile(os.path.join(here, 'requirements.txt')):
    with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
        pipreq = f.readlines()
        # remove pip flag
        if '-i http' in pipreq[0]:
            pipreq.pop(0)
else:
    pipreq = ['pyyaml', 'requests']

setup(
    name="rickled",
    version=about["__version__"],
    description='Tools for pickling Python objects in a completely different way',
    long_description_content_type='text/markdown',
    long_description=long_description,
    license='Apache 2.0',
    keywords = ['Pickle', 'Python', 'YAML', 'JSON'],
    author='Zipfian Science',
    author_email='about@zipfian.science',
    zip_safe=False,
    url='https://github.com/Zipfian-Science/rickled',
    download_url='https://github.com/Zipfian-Science/rickled/archive/v_01.tar.gz',
    packages=find_packages(".", exclude=("tests", "dist", "deploy", "egg-info")),
    include_package_data=True,
    install_requires=pipreq,
    package_dir={'.': 'rickled'},
    extras_require={
        'twisted':  ['twisted'],
        'pyopenssl':  ['pyopenssl']
    },
    entry_points={
        'console_scripts': [
            'rickle = rickled.cli:main',
        ],
    },
    classifiers=[
            'Intended Audience :: Science/Research',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
            'Topic :: Scientific/Engineering :: Artificial Intelligence']
)
