#!/usr/bin/env python
#
# Adpated from httpie project (https://github.com/httpie/httpie)

import codecs
import os
import sys
from distutils.dir_util import remove_tree

from setuptools import setup, find_packages

import abbr

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('./setup.py clean --all')
    os.system('./setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()
# 'setup.py clean-all' shortcut.
elif sys.argv[-1] == 'clean-all':
    os.system('./setup.py clean --all')
    remove_tree('./dist')
    remove_tree('./abbr_cli.egg-info')
    sys.exit()

tests_require = []

dev_require = [
    *tests_require,
    'twine',
    'wheel',
]

install_requires = [
    'requests>=2.22.0',
    'lxml>=4.5.0',
    'docopt>=0.6.2',
    'colorful>=0.5.4',
    'setuptools',
]

install_requires_win_only = [
    'colorama>=0.2.4',
]

# sdist
if 'bdist_wheel' not in sys.argv:
    if 'win32' in str(sys.platform).lower():
        # Terminal colors for Windows
        install_requires.extend(install_requires_win_only)

# bdist_wheel
extras_require = {
    'dev': dev_require,
    'test': tests_require,
    # https://wheel.readthedocs.io/en/latest/#defining-conditional-dependencies
    ':sys_platform == "win32"': install_requires_win_only,
}


def long_description():
    with codecs.open('README.md', 'r', encoding='utf8') as file:
        return file.read()


setup(
    name=abbr.__project_name__,
    version=abbr.__version__,
    description=abbr.__description__,
    long_description=long_description(),
    long_description_content_type='text/markdown',
    author=abbr.__author__,
    author_email=abbr.__author_email__,
    license=abbr.__licence__,
    package_dir={'abbr': 'abbr'},
    packages=find_packages(include=['abbr']),
    entry_points={
        'console_scripts': [
            'abbr = abbr.__main__:main',
        ],
    },
    python_requires='>=3.6',
    extras_require=extras_require,
    install_requires=install_requires,
    classifiers=[
        'Environment :: Console',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Terminals',
        'Topic :: Utilities'
    ],
    project_urls={
        'GitHub': 'https://github.com/mhadidg/abbr-cli',
    },
)
