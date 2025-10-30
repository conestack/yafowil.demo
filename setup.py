from setuptools import find_packages
from setuptools import setup


version = '1.2'
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
        'setuptools',
        'sphinx',
        'Chameleon',
        'docutils',
        'yafowil<4.0.0',
        'yafowil.webob<2.0.0',
        'yafowil.yaml<3.0.0',
        'yafowil.bootstrap<2.0.0',
        # add-on widgets
        # 'yafowil.widget.alohaeditor',
        'yafowil.widget.ace<2.0.0',
        'yafowil.widget.array<2.0.0',
        'yafowil.widget.autocomplete<2.0.0',
        'yafowil.widget.chosen<2.0.0',
        'yafowil.widget.cron<2.0.0',
        'yafowil.widget.datetime<2.0.0',
        'yafowil.widget.dict<2.0.0',
        'yafowil.widget.dynatree<2.0.0',
        'yafowil.widget.image<2.0.0',
        'yafowil.widget.location<2.0.0',
        'yafowil.widget.multiselect<2.0.0',
        # 'yafowil.widget.recaptcha',
        'yafowil.widget.richtext<2.0.0',
        'yafowil.widget.select2<2.0.0',
        'yafowil.widget.slider<2.0.0',
        'yafowil.widget.wysihtml5<2.0.0',
    ],
    entry_points="""
    [yafowil.plugin]
    register = yafowil.demo.loader:register
    """)
