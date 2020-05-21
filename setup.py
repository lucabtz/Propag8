
from propag8 import PROPAG8_VERSION
from setuptools import setup, find_packages

PACKAGE_NAME = 'propag8'

if __name__ == '__main__':
    desc = ''
    with open('README.md', 'r') as f:
        desc = f.read()
    setup(
        name=PACKAGE_NAME,
        version=PROPAG8_VERSION,
        packages=find_packages(),
        install_requires=[],
        python_requires='>=3.6.3',
        scripts=[],
        description='Make uncertainty propagation no longer a hassle',
        long_description=desc,
        long_description_content_type='text/markdown'
    )
