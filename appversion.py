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

"""Define PIEONE version information."""

# We follow Semantic Versioning (https://semver.org/)
_MAJOR_VERSION = '0'
_MINOR_VERSION = '1'
_PATCH_VERSION = '1'

# When building releases, we can update this value on the release branch to
# reflect the current release candidate ('rc0', 'rc1') or, finally, the official
# stable release (indicated by `_REL_SUFFIX = ''`). Outside the context of a
# release branch, the current version is by default assumed to be a
# 'development' version, labeled 'dev'.
_DEV_SUFFIX = 'dev'
_REL_SUFFIX = 'rc0'

# Example, '0.4.0rc0'
__version__ = '.'.join([
    _MAJOR_VERSION,
    _MINOR_VERSION,
    _PATCH_VERSION,
])
__dev_version__ = '{}.{}'.format(__version__, _DEV_SUFFIX)
__rel_version__ = '{}{}'.format(__version__, _REL_SUFFIX)
