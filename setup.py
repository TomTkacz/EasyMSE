from setuptools import setup
from setuptools import find_packages
from configparser import ConfigParser

setup(
    name='ezmse',
    version='0.1.0',
    description='some package description',
    author='Tom Tkacz',
    author_email='thomasatkacz@gmail.com',
    url='https://github.com/TomTkacz/EasyMSE',
    packages=find_packages(),
    long_description="package description, but long",
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