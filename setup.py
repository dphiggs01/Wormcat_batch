"""
Setup for pypi releases of wormcat_batch
"""
from setuptools import setup
from pathlib import Path

# rm -rf dist
# python setup.py sdist
# pip install dist/wormcat_batch-1.0.1.tar.gz
# twine check dist/*
# twine upload --repository pypi dist/*


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='wormcat_batch',
      version='1.1.11',
      description='Batch processing for Wormcat data',
      long_description_content_type="text/markdown",
      long_description=long_description,

      url='https://github.com/dphiggs01/Wormcat_batch',
      author='Dan Higgins',
      author_email='daniel.higgins@yahoo.com',
      license='MIT',

      packages=['wormcat_batch'],
      install_requires=['pandas','xlrd','openpyxl','xlsxwriter'],
      entry_points={
          'console_scripts': ['wormcat_cli=wormcat_batch.run_wormcat_batch:main'],
      },
      include_package_data=True,
      zip_safe=False)
