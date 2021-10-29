from yafowil import bootstrap
from yafowil.base import factory
from yafowil.utils import entry_point
import os


resourcedir = os.path.join(os.path.dirname(__file__), 'resources')


js = [{
    'group': 'yafowil.demo.dependencies',
    'resource': 'jquery-3.6.0.min.js',
    'order': 10,
}, {
    'group': 'yafowil.demo.dependencies',
    'resource': 'jquery.migrate-3.3.2.min.js',
    'order': 10,
}, {
    'group': 'yafowil.demo.dependencies',
    'resource': 'jqueryui/jquery-ui.min.js',
    'order': 10,
}]


css = [{
    'group': 'yafowil.demo.dependencies',
    'resource': 'jqueryui/jquery-ui.min.css',
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


def configure():
    bootstrap.configure_factory('bootstrap')
