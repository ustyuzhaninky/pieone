# coding=utf-8
# Copyright (c) 2022, Konstantin Usiuzhanin

# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# @author: Konstantin Ustyuzhanin
# 
"""Setup script for PIEONE-keras.

This script will install PIEONE-keras as a Python module.

See: https://github.com/ustyuzhaninky/PIEONE-keras

"""

import argparse
import codecs
import datetime
import fnmatch
import os
import sys
from os import path
from setuptools import find_packages
from setuptools import setup
import codecs

from setuptools.command.install import install as InstallCommandBase
from setuptools.dist import Distribution

import appversion

# Defaults if doing a release build.
KIVY_VERSION = 'kivy>=2.1.0'
KIVYMD_VERSION = 'kivymd>=1.0.2'


class BinaryDistribution(Distribution):

    def has_ext_modules(self):
        return True

def find_files(pattern, root):
    """Return all the files matching pattern below root dir."""
    for dirpath, _, files in os.walk(root):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(dirpath, filename)


class InstallCommand(InstallCommandBase):
    """Override the dir where the headers go."""

    def finalize_options(self):
        ret = super().finalize_options()
        # We need to set this manually because we are not using setuptools to
        # compile the shared libraries we are distributing.
        self.install_lib = self.install_platlib
        return ret

class SetupToolsHelper(object):
    """Helper to execute `setuptools.setup()`."""

    def __init__(self, release=False, nodev=False, md_version_override=None):
        """Initialize ReleaseBuilder class.
        Args:
        release: True to do a release build. False for a nightly build.
        nodev: True to skip a development environment setup (i.e. packaging). False for full setup.
        md_version_override: Set to override the kivymd_version dependency.
        """
        self.release = release
        self.dev = not nodev
        self.md_version_override = md_version_override

    def _get_version(self):
        """Returns the version and project name to associate with the build."""
        if self.release:
            project_name = 'pieone'
            version = appversion.__rel_version__
        else:
            project_name = 'pieone-nightly'
            version = appversion.__dev_version__
            version += datetime.datetime.now().strftime('%Y%m%d')

        return version, project_name

    def _get_required_packages(self):
        """Returns list of required packages."""
        with open('requirements.txt', 'rt') as file:
            required_packages = file.readlines()
        if self.dev is True:
            with open('requirements-dev.txt', 'rt') as file:
                for line in file.readlines():
                    required_packages.append(line)
        return required_packages

    def _get_kivy_packages(self):
        """Returns list of required packages if using PIEONE."""
        kivy_packages = []
        if self.release:
            kivy_version = KIVY_VERSION
            kivymd_version = KIVYMD_VERSION
        else:
            kivy_version = 'kivy-nightly'
            kivymd_version = 'kivymd-nightly'

        # Overrides required versions if md_version_override is set.
        if self.md_version_override:
            kivymd_version = self.md_version_override

        # kivy_packages.append(kivy_version)
        kivy_packages.append(kivymd_version)
        return kivy_packages

    def run_setup(self):
        # Builds the long description from the README.
        root_path = os.path.abspath(os.path.dirname(__file__))
        with codecs.open(os.path.join(root_path, 'README.rst'), encoding='utf-8') as f:
            long_description = f.read()


        version, project_name = self._get_version()
        setup(
            name=project_name,
            version=version,
            include_package_data=True,
            packages=find_packages(exclude=['docs']),  # Required
            package_data={'pieone': ['*.rst', '*.kv', '*.ini', '*.json',
                               'assets/data/*',
                               'assets/images/*',
                               'assets/locales/*',
                               'configs/*',
                               'docs/*']},
            install_requires=self._get_required_packages(),
            extras_require={
                'pieone': self._get_kivy_packages(),
            },
            distclass=BinaryDistribution,
            cmdclass={
                'install': InstallCommand,
            },
            headers=list(find_files('*.proto', 'PIEONE')),
            description='PIEONE: A simple Section 300 Hydrogen Treatment Unit Simulator for students',
            long_description=long_description,
            long_description_content_type='text/markdown',
            url='https://github.com/ustyuzhaninky/pieone',  # Optional
            author='Konstantin Ustyuzhanin',  # Optional
            # python_requires='>=3',
            classifiers=[  # Optional
                'Development Status :: 3 - Alpha',

                # Indicate who your project is intended for
                'Intended Audience :: Developers',
                'Intended Audience :: Education',


                # Pick your license as you wish
                'License :: OSI Approved :: Apache Software License',

                'Programming Language :: Python :: 3.8',
                'Programming Language :: Python :: 3.9',
                'Programming Language :: Python :: 3.10',

                'Topic :: Software Development',

            ],
            project_urls={  # Optional
                'Documentation': 'https://github.com/ustyuzhaninky/pieone',
                'Bug Reports': 'https://github.com/ustyuzhaninky/pieone/issues',
                'Source': 'https://github.com/ustyuzhaninky/pieone',
            },
            license='MIT',
            keywords='kivy kivymd section_300 simulator testing app example educational'
        )


if __name__ == '__main__':
    # Hide argparse help so `setuptools.setup` help prints. This pattern is an
    # improvement over using `sys.argv` and then `sys.argv.remove`, which also
    # did not provide help about custom arguments.
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        '--release',
        action='store_true',
        help='Pass as true to do a release build')
    parser.add_argument(
        '--nodev',
        action='store_true',
        help='Pass as true to do skip a developer install')
    parser.add_argument(
        '--md-version',
        type=str,
        default=None,
        help='Overrides for kivymd version required when PIEONE is installed, e.g.'
        'kivy>=2.1.0')
    FLAGS, unparsed = parser.parse_known_args()
    # Go forward with only non-custom flags.
    sys.argv.clear()
    # Downstream `setuptools.setup` expects args to start at the second element.
    unparsed.insert(0, 'foo')
    sys.argv.extend(unparsed)
    setup_tools_helper = SetupToolsHelper(release=FLAGS.release,
                                          nodev=FLAGS.nodev, 
                                          md_version_override=FLAGS.md_version)
    setup_tools_helper.run_setup()
