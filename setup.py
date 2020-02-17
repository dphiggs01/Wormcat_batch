from setuptools import setup
#python setup.py sdist upload
setup(name='wormcat_batch',
      version='1.0.0',
      description='Batch processing for Wormcat data',
      url='https://github.com/dphiggs01/Wormcat_batch',
      author='Dan Higgins',
      author_email='daniel.higgins@yahoo.com',
      license='MIT',

      packages=['wormcat_batch'],
      install_requires=['pandas','xlrd','xlsxwriter'],
      entry_points={
          'console_scripts': ['wormcat_cli=wormcat_batch.run_wormcat_batch:main'],
      },
      include_package_data=True,
      zip_safe=False)
