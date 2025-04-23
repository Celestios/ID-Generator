from setuptools import setup, find_packages
import os

setup(
    name='numgen',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[],
    author='shahin',
    author_email='shahin.id5638@gmail.com',
    description='Takes a number and returns an encrypted one deterministically',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    url='https://github.com/Celestios/ID-Generator.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
