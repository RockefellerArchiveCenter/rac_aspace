from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='rac-aspace',
      version='0.0.1',
      description='Helpers for using the ArchivesSpace API using ArchivesSnake',
      url='https://github.com/RockefellerArchiveCenter/rac_aspace',
      author='Rockefeller Archive Center',
      author_email='archive@rockarch.org',
      license='MIT',
      packages=setuptools.find_packages(),
      python_requires='>=3.4',
      zip_safe=False)
