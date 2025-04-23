from setuptools import setup, find_packages

setup(
    name='ID Generator',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'your_script_name=main:main',
        ],
    },
    author='shahin',
    author_email='shahin.id5638@gmail.com',
    description='takes a Number and return a encrypted one deterministically',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    url='https://github.com/Celestios/ID-Generator.git',
)
