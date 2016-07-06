# -*- encoding: utf-8 -*-
__author__ = "Christian Schwede <cschwede@redhat.com>"
name = 'swift-automime'
entry_point = 'automime.middleware:filter_factory'
version = '0.1'

from setuptools import setup, find_packages

setup(
    name=name,
    version=version,
    description='Openstack Swift auto content encoding middleware',
    license='Apache License (2.0)',
    author='Christian Schwede',
    author_email='cschwede@redhat.com',
    url='https://github.com/cschwede/swift-automime',
    packages=find_packages(),
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Environment :: No Input/Output (Daemon)'],
    install_requires=['swift'],
    entry_points={
        'paste.filter_factory': ['%s=%s' % (name, entry_point)]
    },
)
