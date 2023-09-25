from setuptools import setup
from setuptools import find_packages

configFilePath = 'ezmse/include/config.ini'

with open(configFilePath, 'r+') as file:
    file.seek(0)
    newLines = []
    lastLineBlank=False
    for i,line in enumerate(file.readlines()):
        if line == "\n":
            if lastLineBlank:
                continue
            else:
                lastLineBlank = True
        else:
            lastLineBlank = False
            
        parts = line.split("=")
        if len(parts) > 1:
            newLines.append(parts[0]+"=\n")
        else:
            newLines.append(line)
    file.truncate(0)
    file.seek(0)
    file.writelines(newLines)

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