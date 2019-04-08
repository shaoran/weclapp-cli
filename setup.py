import os
from setuptools import setup, find_packages

from weclapp.version import VERSION

basedir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(basedir, 'README.md')) as fp:
    longdesc = fp.read()

setup(name='weclapp-cli',
    version=VERSION,
    description='A small cli for uploading time records via a CSV file',
    long_description=longdesc,
    long_description_content_type='text/markdown',
    url='https://shaoran.github.io/weclapp-cli/',
    author='Pablo Yanez Trujillo',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Office/Business',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='weclapp time records uploader',
    packages=find_packages(),
    python_requires='>=3',
    install_requires=['PyYAML', 'colorama', 'coloredlogs', 'python-dateutil'],
    entry_points={
        'console_scripts': [
            'weclapp-cli = weclapp.bin.weclapp:main'
        ],
    },
    project_urls={
        'Homepage': 'https://shaoran.github.io/weclapp-cli/',
        'Bug Reports': 'https://github.com/shaoran/weclapp-cli/issues',
        'Source': 'https://github.com/shaoran/weclapp-cli',
    },
)
