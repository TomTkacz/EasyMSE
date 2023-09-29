from setuptools import setup
from setuptools import find_packages
from configparser import ConfigParser

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

pathToConfig = 'ezmse/include/config.ini'
config = ConfigParser()
config.read(pathToConfig)

for section in config.sections():
    for option in config.options(section):
        config[section][option] = ''

with open(pathToConfig, 'w') as f:
    config.write(f)
config.read(pathToConfig)