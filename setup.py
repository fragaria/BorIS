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
    license='BSD',
    url='http://boris.github.com/',

    packages=find_packages(
        where='.',
        exclude=('doc', 'debian',)
    ),

    include_package_data=True,

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
        'Django==1.3.1',
        'south>=0.7',
        'django-grappelli>=2.3.7',
        'django-model-utils',
        'django-form-utils',
        'raven==1.4.6',
        'fragapy==1.2.3',
        'gunicorn',
    ],
    setup_requires=[
        'setuptools_dummy',
    ],
)
