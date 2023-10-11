from setuptools import setup
from setuptools import find_packages
from configparser import ConfigParser
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='ezmse',
    version='0.1.1',
    description='A Python package for generating custom Magic The Gathering cards',
    author='Tom Tkacz',
    author_email='thomasatkacz@gmail.com',
    url='https://github.com/TomTkacz/EasyMSE',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_data={
        'ezmse': ['include/*'],
    },
    install_requires=[
        'pyfakefs>=5.2'
    ],
    extras_require={
        'dev': [
            'pytest>=7.4',
        ]
    }
)

# easy way to ensure config.ini is cleared before deployment (for development)
try:
    pathToConfig = 'ezmse/include/config.ini'
    config = ConfigParser()
    config.read(pathToConfig)

    for section in config.sections():
        for option in config.options(section):
            config[section][option] = ''

    with open(pathToConfig, 'w') as f:
        config.write(f)
except:
    pass