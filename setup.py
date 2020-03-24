from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='rac-aspace',
      version='0.0.1',
      description='Helpers for using the ArchivesSpace API using ArchivesSnake',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/RockefellerArchiveCenter/rac_aspace',
      author='Rockefeller Archive Center',
      author_email='archive@rockarch.org',
      license='MIT',
      packages=find_packages(),
      install_requires=[],
      tests_require=[],
      python_requires='>=3.4',
      zip_safe=False)
