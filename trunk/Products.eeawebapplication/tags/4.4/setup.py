""" EEA Web Application installer
"""
from setuptools import setup, find_packages
import os

NAME = 'Products.eeawebapplication'
PATH = NAME.split('.') + ['version.txt']
VERSION = open(os.path.join(*PATH)).read().strip()

setup(
 name=NAME,
 version=VERSION,
 description="EEA Web Application skin for EEA",
 long_description=open("README.txt").read() + "\n" +
                  open(os.path.join("docs", "HISTORY.txt")).read(),
 url="https://svn.eionet.europa.eu/projects/"
     "Zope/browser/trunk/Products.eeawebapplication",
 classifiers=[
           "Framework :: Plone",
           "Programming Language :: Python",
           "Topic :: Software Development :: Libraries :: Python Modules",
   ],
 keywords='EEA web application',
 author='Antonio de Marinis (EEA), European Environment Agency',
 author_email='webadmin@eea.europa.eu',
 license='GPL',
 packages=find_packages(exclude=['ez_setup']),
 namespace_packages=['Products'],
 include_package_data=True,
 zip_safe=False,
 install_requires=[
     "setuptools",
 ],
 entry_points="""
 # -*- Entry points: -*-
 """,
 )

