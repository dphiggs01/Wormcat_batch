import json
from setuptools import setup

#python setup.py sdist
#pip install dist/wormcat_batch-1.0.1.tar.gz
# twine check dist/*
# twine upload --repository pypi dist/*

with open('setup.json', 'r') as file:
    data = json.load(file)

setup(name=data['name'],
      version=data['version'],
      description=data['description'],
      url=data['url'],
      author=data['author'],
      author_email=data['author_email'],
      license=data['license'],
      packages=data['packages'],
      install_requires=data['install_requires'],
      entry_points=data['entry_points'],
      include_package_data=data['include_package_data'],
      zip_safe=data['zip_safe'])
