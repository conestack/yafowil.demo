from setuptools import (
    setup,
    find_packages,
)


version = '1.0'
shortdesc = \
'YAFOWIL - Demo Application'
longdesc = ""
tests_require = ['interlude']


setup(name='yafowil.demo',
      version=version,
      description=shortdesc,
      long_description=longdesc,
      classifiers=[
          'License :: OSI Approved :: Python Software Foundation License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development',
      ],
      keywords='html input widgets form compound',
      author='BlueDynamics Alliance',
      author_email='dev@bluedynamics.com',
      url=u'https://github.com/bluedynamics/yafowil.demo',
      license='BSD simplified and CC-BY-SA',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['yafowil'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'setuptools',
          'sphinx',
          'Chameleon',
          'docutils',
          'yafowil',
          'yafowil.webob',
          'yafowil.yaml',
          'yafowil.bootstrap',
           # add-on widgets to document
          #'yafowil.widget.alohaeditor',
          'yafowil.widget.ace',
          'yafowil.widget.array',
          'yafowil.widget.autocomplete',
          'yafowil.widget.chosen',
          'yafowil.widget.datetime',
          'yafowil.widget.dict',
          'yafowil.widget.dynatree',
          'yafowil.widget.image',
          'yafowil.widget.multiselect',
          'yafowil.widget.richtext',
          'yafowil.widget.select2',
          'yafowil.widget.slider',
          'yafowil.widget.wysihtml5',
      ],
      tests_require=tests_require,
      test_suite="yafowil.tests.test_suite",
      extras_require = dict(
          test=tests_require,
      ),
      entry_points="""
      [yafowil.plugin]
      register = yafowil.demo.loader:register
      """,
)
