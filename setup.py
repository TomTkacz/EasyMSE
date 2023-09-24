from setuptools import setup
from setuptools import find_packages

setup(
    name='ezmse',
    version='0.0.8',
    description='some package description',
    author='Tom Tkacz',
    author_email='thomasatkacz@gmail.com',
    url='https://github.com/TomTkacz/EasyMSE',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ezmse-cli = ezmse.main:main',
        ]
    },
    long_description="package description, but long"
)