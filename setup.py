from setuptools import find_packages
from setuptools import setup


version = '2.0.dev0'
shortdesc = 'YAFOWIL - Demo Application'
longdesc = ""


setup(
    name='yafowil.demo',
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
    author='Yafowil Contributors',
    author_email='dev@conestack.org',
    url=u'http://github.com/conestack/yafowil.demo',
    license='Simplified BSD and CC-BY-SA',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['yafowil'],
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'Chameleon',
        'setuptools',
        'sphinx',
        'yafowil',
        'yafowil.bootstrap',
        'yafowil.webob',
        # add-on widgets
        # 'yafowil.widget.alohaeditor',
        # 'yafowil.widget.dynatree',
        # 'yafowil.widget.recaptcha',
        'yafowil.widget.ace',
        'yafowil.widget.array',
        'yafowil.widget.autocomplete',
        'yafowil.widget.chosen',
        'yafowil.widget.color',
        'yafowil.widget.cron',
        'yafowil.widget.datetime',
        'yafowil.widget.dict',
        'yafowil.widget.image',
        'yafowil.widget.location',
        'yafowil.widget.multiselect',
        'yafowil.widget.richtext',
        'yafowil.widget.select2',
        'yafowil.widget.slider',
        'yafowil.widget.tiptap',
        'yafowil.widget.wysihtml5',
        'yafowil.yaml',
    ],
    entry_points="""
    [yafowil.plugin]
    register = yafowil.demo.loader:register
    configure = yafowil.demo.loader:configure
    """)
