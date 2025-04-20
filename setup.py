from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='aavsoquery',
    version='1.0.2',
    author='Divyansh Srivastava',
    author_email='divyansh@umk.pl',
    description='A Python module for fetching and plotting astronomical data of stars from AAVSO',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/prashant050701/aavso_query',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'numpy',
        'matplotlib',
        'lmfit'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
