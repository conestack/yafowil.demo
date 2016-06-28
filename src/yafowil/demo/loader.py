from yafowil.base import factory
from yafowil.utils import entry_point
import os


resourcedir = os.path.join(os.path.dirname(__file__), 'resources')


js = [{
    'group': 'yafowil.demo.dependencies',
    'resource': 'jquery-1.9.1.js',
    'order': 10,
}, {
    'group': 'yafowil.demo.dependencies',
    'resource': 'jquery.migrate-1.2.1.js',
    'order': 10,
}, {
    'group': 'yafowil.demo.dependencies',
    'resource': 'jqueryui/jquery-ui-1.10.3.custom.js',
    'order': 10,
}]


css = [{
    'group': 'yafowil.demo.dependencies',
    'resource': 'jqueryui/jquery-ui-1.10.3.custom.css',
    'order': 10,
}, {
    'group': 'yafowil.demo.common',
    'resource': 'yafowil.demo.css',
    'order': 20,
}]


@entry_point(order=10)
def register():
    factory.register_theme('bootstrap', 'yafowil.demo',
                           resourcedir, js=js, css=css)
