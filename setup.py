#!/usr/bin/env python
import os
import sys

if sys.version_info < (3, 7) or sys.version_info >= (3, 10):
    print('Error: dbt-tidb does not support this version of Python.')
    print('Please install Python 3.7 or higher but less than 3.10.')
    sys.exit(1)

# require version of setuptools that supports find_namespace_packages
from setuptools import setup
try:
    from setuptools import find_namespace_packages
except ImportError:
    # the user has a downlevel version of setuptools.
    print('Error: dbt requires setuptools v40.1.0 or higher.')
    print('Please upgrade setuptools with "pip install --upgrade setuptools" '
          'and try again')
    sys.exit(1)

# pull long description from README
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

package_name = "dbt-tidb"
package_version = "1.0.0"
dbt_core_version = "1.0.1"
description = """The TiDB adapter plugin for dbt"""

setup(
    name=package_name,
    version=package_version,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="daemonxiao",
    author_email="qiang.wu@pingcap.com",
    url="https://github.com/pingcap/dbt-tidb.git",
    packages=find_namespace_packages(include=['dbt', 'dbt.*']),
    include_package_data=True,
    install_requires=[
        'dbt-core~={}'.format(dbt_core_version),
        "mysql-connector-python>=8.0.0,<8.1",
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',

        'License :: OSI Approved :: Apache Software License',

        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',

        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires=">=3.7,<3.10",
)
