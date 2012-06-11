import os
from yafowil import loader
import yafowil.webob
from yafowil.base import factory
from yafowil.controller import Controller
from yafowil.tests import fxml
from yafowil.utils import (
    get_plugin_names,
    get_resource_directory,
    get_javascripts,
    get_stylesheets,
)
from webob import Request, Response
from chameleon import PageTemplateLoader

dir = os.path.dirname(__file__)


def resource_response(path, environ, start_response, content_type):
    response = Response(content_type=content_type)
    with open(path) as file:
        response.write(file.read())
    return response(environ, start_response)


def get_resources():
    ret = dict(js=list(), css=list())
    for plugin_name in get_plugin_names():
        plugin_resources_dir = get_resource_directory(plugin_name)
        resource_name = '++resource++%s' % plugin_name
        if not (plugin_resources_dir):
            continue
        for js in get_javascripts(plugin_name):
            ret['js'].append(resource_name + '/' + js)
        for css in get_stylesheets(plugin_name):
            ret['css'].append(resource_name + '/' + css)
    return ret


def dispatch_resource(path, environ, start_response):
    plugin_name = path.split('/')[0][12:]
    plugin_resources_dir = get_resource_directory(plugin_name)
    filepath = os.path.join(plugin_resources_dir, *path.split('/')[1:])
    if path.endswith('js'):
        ct = 'text/javascript'
    if path.endswith('css'):
        ct = 'text/css'
    if path.endswith('png'):
        ct = 'image/png'
    return resource_response(filepath, environ, start_response, ct)


def lookup_form(path):
    pass


def app(environ, start_response):
    path = environ['PATH_INFO'].strip('/')
    resources = get_resources()
    if path.startswith('++resource++'):
        return dispatch_resource(path, environ, start_response)
    if path.startswith('++widget++'):
        form = lookup_form(path)
    else:
        form = None
    templates = PageTemplateLoader(dir)
    template = templates['main.pt']
    response = Response(body=template(resources=resources, form=form))
    return response(environ, start_response)