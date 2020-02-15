from setuptools import setup

setup(name='wormcat_batch',
      version='0.9.6',
      description='Batch processing for Wormcat data',
      url='https://github.com/dphiggs01/Wormcat_batch',
      author='Dan Higgins',
      author_email='daniel.higgins@yahoo.com',
      license='MIT',

      packages=['wormcat_batch'],
      # Add template files to MANIFEST!!
      entry_points={
          'console_scripts': ['wormcat_cli=wormcat_batch.run_wormcat_batch:main'],
      },
      include_package_data=True,
      zip_safe=False)
