|py_versions| |build_statuses| |pypi_versions|

.. |py_versions| image:: https://img.shields.io/pypi/pyversions/prettyfi?style=flat-square
    :alt: python versions

.. |build_statuses| image:: https://img.shields.io/github/workflow/status/s3rius/prettyfi/Testing%20and%20publish?style=flat-square
    :alt: build status

.. |pypi_versions| image:: https://img.shields.io/pypi/v/prettyfi?style=flat-square
    :alt: pypi version
    :target: https://pypi.org/project/prettyfi/

Prettify
========

Prettyfi usage
**************

usage: prettyfi [-h] [-c CONFIG] files [files ...]

Simple utility to make your files prettier.

positional arguments:
  files                 Files to sort

optional arguments:
    --help                  show help message and exit
    --config=config_path    path to configuration file

Default config file location is "~/.prettyfirc".

Config file format:

.. code:: bash

    .<ext> $ pretty_command {file}
    # Where "ext" -> your file extension,
    # {file} -> stub for actual file,
    # For example:
    .py   $ isort {file}
    .java $ rm {file}