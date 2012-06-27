import os
from yafowil.base import factory

resourcedir = os.path.join(os.path.dirname(__file__), 'resources')

js = [{
    'resource': 'jquery-1.7.2.min.js',
    'thirdparty': False,
    'order': 10,
}, {
    'resource': 'jquery-ui-1.8.18.min.js',
    'thirdparty': False,
    'order': 11,
}]

css = [{
    #'resource': 'jquery-ui-1.8.18.css',
    'resource': 'jquery-ui-1.8.16.bootstrap.css',
    'thirdparty': False,
    'order': 10,
}, {
    'resource': 'yafowil.demo.css',
    'thirdparty': False,
    'order': 20,
}]


def register():
    factory.register_theme('bootstrap', 'yafowil.demo',
                           resourcedir, js=js, css=css)