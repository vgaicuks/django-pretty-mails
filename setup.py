#!/usr/bin/env python
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='django_pretty_mails',
    version='0.0.2',
    author='Vitālijs Gaičuks',
    author_email='vitalijs.gaicuks@gmail.com',
    description='Django templated mails with responsive html design.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/vgaicuks/django-pretty-mails',
    # packages=setuptools.find_packages(),
    packages=['django_pretty_mails'],
    include_package_data=True,
    requires=['django(>=1.11)'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
