from setuptools import setup, find_packages
import os

version = '2.0'

setup(name='collective.timelines',
      version=version,
      description="Timeline views for collections and folders (using verite TimelineJS).",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Alec Mitchell',
      author_email='alecpm@gmail.com',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'archetypes.schemaextender',
          'plone.directives.form',
          'five.grok',
          'plone.app.z3cform',
          'plone.behavior',
      ],
      entry_points="""[z3c.autoinclude.plugin]
target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
