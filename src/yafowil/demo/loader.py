from yafowil import bootstrap
from yafowil.base import factory
from yafowil.utils import entry_point
import os
import webresource as wr


resources_dir = os.path.join(os.path.dirname(__file__), 'resources')


##############################################################################
# Default
##############################################################################

resources = wr.ResourceGroup(
    name='yafowil.demo',
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


##############################################################################
# Registration
##############################################################################

@entry_point(order=10)
def register():
    factory.register_resources('bootstrap3', 'yafowil.demo', resources)


##############################################################################
# Configuration
##############################################################################

def configure():
    bootstrap.configure_factory('bootstrap3')
