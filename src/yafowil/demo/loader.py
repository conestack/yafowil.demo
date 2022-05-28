from yafowil import bootstrap
from yafowil.base import factory
from yafowil.utils import entry_point
import os
import webresource as wr


resources_dir = os.path.join(os.path.dirname(__file__), 'resources')


##############################################################################
# Default
##############################################################################

# webresource ################################################################

resources = wr.ResourceGroup(
    name='yafowil-demo-resources',
    directory=resources_dir,
    path='yafowil-demo'
)
resources.add(wr.ScriptResource(
    name='jquery-js',
    resource='jquery-3.6.0.js',
    compressed='jquery-3.6.0.min.js'
))
resources.add(wr.StyleResource(
    name='yafowil-demo-css',
    resource='yafowil.demo.css'
))

# B/C resources ##############################################################

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


##############################################################################
# Registration
##############################################################################

@entry_point(order=10)
def register():
    widget_name = 'yafowil.demo'

    factory.register_theme(
        'bootstrap3',
        widget_name,
        resources_dir,
        js=js,
        css=css
    )
    factory.register_resources('bootstrap3', widget_name, resources)


##############################################################################
# Configuration
##############################################################################

def configure():
    bootstrap.configure_factory('bootstrap3')
