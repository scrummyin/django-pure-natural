# -*- coding: utf-8; mode: python; -*-
from setuptools import setup, find_packages

setup(
    name='django-pure-natural',
    version='0.1.8',
    description="A package that allows you to export and import django fixtures without need of pk's",
    long_description="This package adds django commands to your application that will allow you to export and import data without use of pk's ",
    license='BSD',
    keywords='django natural_keys',
    url='https://github.com/scrummyin/',
    author='Brian Faherty',
    author_email='bfaherty@fool.com',
    maintainer='Brian Faherty',
    maintainer_email='bfaherty@fool.com',
    packages= find_packages(),
    install_requires = [],
    classifiers=['Development Status :: 3 - Alpha',
                 'Environment :: Web Environment',
                 'Framework :: Django',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 ],
    )
