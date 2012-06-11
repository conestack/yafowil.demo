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
    get_examples,
    get_example,
)
from webob import Request, Response
from chameleon import PageTemplateLoader

dir = os.path.dirname(__file__)


def get_resource_dir():
    return os.path.join(os.path.dirname(__file__), 'resources')


def get_js(thirdparty=True):
    return ['jquery-1.7.2.min.js']


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


def render_form(widget, environ, plugin_name):
    form = factory(
        u'form',
        name=plugin_name,
        props={
            'action': '/++widget++%s/index.html' % plugin_name})
    form[widget.name] = widget
    form['submit'] = factory(
        'field:submit',
        props={
            'label': 'submit',
            'action': 'save',
            'handler': lambda widget, data: None})
    controller = Controller(form, Request(environ))
    return controller.rendered


def app(environ, start_response):
    path = environ['PATH_INFO'].strip('/')
    resources = get_resources()
    if path.startswith('++resource++'):
        return dispatch_resource(path, environ, start_response)
    if path.startswith('++widget++'):
        splitted = path.split('/')
        plugin_name = splitted[0][10:]
        example = get_example(plugin_name)
        if splitted[1] != 'index.html':
            return example['routes'][splitted[1]]
        form = render_form(example['widget'], environ, plugin_name)
    else:
        form = None
        plugin_name = None
    templates = PageTemplateLoader(dir)
    template = templates['main.pt']
    response = Response(body=template(resources=resources,
                                      form=form,
                                      widgets=get_examples(),
                                      plugin_name=plugin_name))
    return response(environ, start_response)