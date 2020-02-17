"""
Copyright (c) 2012 Filip Varecha, Hynek Urban

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

from setuptools import setup, find_packages
import boris

setup(
    name='boris',
    version=boris.__versionstr__,
    description='BorIS',
    long_description='\n'.join((
        'BorIS',
        '',
    )),
    author='BorIS team',
    author_email='info@boris.cz',
    license='MIT',
    url='http://boris.github.com/',

    packages=find_packages(
        where='.',
        exclude=('doc', 'debian',)
    ),

    include_package_data=True,

    data_files=[("", ["LICENSE.txt"])],

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        'setuptools>=0.6b1',
        'Django==1.11.28',
        'south==0.8.4',
        'django-grappelli>=2.6.3',
        'django-model-utils',
        'django-form-utils',
        'raven>=3.3.3',
        'fragapy==1.2.6',
        'gunicorn',
    ],
    setup_requires=[
        'setuptools_dummy',
    ],
)
