"""
Installs:
    - ocrd-olahd-client
"""

import codecs
import json
from setuptools import setup
from setuptools import find_packages

with codecs.open('README.md', encoding='utf-8') as f:
    README = f.read()

with open('./ocrd-tool.json', 'r') as f:
    version = json.load(f)['version']
    
setup(
    name='ocrd_olahd_client',
    version=version,
    description='OCR-D processor and client for OLA-HD',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Konstantin Baierer',
    author_email='unixprog@gmail.com',
    url='https://github.com/OCR-D/ocrd_olahd_client',
    license='Apache 2.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=open('requirements.txt').read().split('\n'),
    package_data={
        '': ['*.json', '*.yml', '*.yaml', '*.csv.gz', '*.jar', '*.zip'],
    },
    entry_points={
        'console_scripts': [
            'ocrd-olahd-client=ocrd_olahd_client.cli:cli'
        ]
    },
)
