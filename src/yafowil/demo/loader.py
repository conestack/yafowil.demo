from yafowil import bootstrap
from yafowil.base import factory
from yafowil.utils import entry_point
import os


resources_dir = os.path.join(os.path.dirname(__file__), 'resources')


js = [{
    'group': 'yafowil.demo.dependencies',
    'resource': 'jquery-3.6.0.js',
    'order': 10,
}]
css = [{
    'group': 'yafowil.demo.common',
    'resource': 'yafowil.demo.css',
    'order': 20,
}]


@entry_point(order=10)
def register():
    factory.register_theme(
        'bootstrap', 'yafowil.demo', resources_dir,
        js=js, css=css
    )


def configure():
    bootstrap.configure_factory('bootstrap')
