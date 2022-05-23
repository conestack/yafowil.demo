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

scripts = wr.ResourceGroup(name='scripts')
scripts.add(wr.ScriptResource(
    name='jquery-js',
    directory=resources_dir,
    resource='jquery-3.6.0.js',
    compressed='jquery-3.6.0.min.js'
))

styles = wr.ResourceGroup(name='styles')
styles.add(wr.StyleResource(
    name='yafowil-demo-css',
    directory=resources_dir,
    resource='yafowil.demo.css'
))

resources = wr.ResourceGroup(name='demo-resources')
resources.add(scripts)
resources.add(styles)

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
    factory.register_theme(
        'bootstrap', 'yafowil.demo', resources_dir,
        js=js, css=css, resources=resources
    )


##############################################################################
# Configuration
##############################################################################

def configure():
    bootstrap.configure_factory('bootstrap')
