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
    long_description="package description, but long",
    install_requires=[
        'pillow>=10.0.0'
    ],
    package_data={
        'ezmse': ['include/*'],
    }
)

import ezmse
ezmse.config.wipe()