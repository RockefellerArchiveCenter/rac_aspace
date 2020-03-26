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
      install_requires=["ArchivesSnake>=0.8.1",
                        "fuzzywuzzy>=0.17.0",
      tests_require=["pytest",
                     "pre-commit>=1.18.3",
                     "sphinx>=1.8.5",
                     "tox>=3.14.0"],
      python_requires='>=3.4',
      zip_safe=False)
