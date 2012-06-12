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

CTMAP = {
    '.js': 'text/javascript',
    '.css': 'text/css',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.jpg': 'image/jpeg',
}


def get_resource_dir():
    return os.path.join(os.path.dirname(__file__), 'resources')


def get_js():
    return [{
        'resource': 'jquery-1.7.2.min.js',
        'thirdparty': False,
        'order': 10,
    }, {
        'resource': 'jquery-ui-1.8.18.min.js',
        'thirdparty': False,
        'order': 11,
    }]


def get_css():
    return [{
        'resource': 'jquery-1.7.2.min.css',
        'thirdparty': False,
        'order': 10,
    }]


def resource_response(path, environ, start_response, content_type):
    response = Response(content_type=content_type)
    with open(path) as file:
        response.write(file.read())
    return response(environ, start_response)


def get_resources():
    all_js = list()
    all_css = list()
    for plugin_name in get_plugin_names():
        plugin_resources_dir = get_resource_directory(plugin_name)
        resource_name = '++resource++%s' % plugin_name
        if not (plugin_resources_dir):
            continue
        for js in get_javascripts(plugin_name):
            js['resource'] = resource_name + '/' + js['resource']
            all_js.append(js)
        for css in get_stylesheets(plugin_name):
            css['resource'] = resource_name + '/' + css['resource']
            all_css.append(css)
    ret = dict(js=list(), css=list())
    all_js = sorted(all_js, key=lambda x: x['order'])
    all_css = sorted(all_css, key=lambda x: x['order'])
    for js in all_js:
        ret['js'].append(js['resource'])
    for css in all_css:
        ret['css'].append(css['resource'])
    return ret


def dispatch_resource(path, environ, start_response):
    plugin_name = path.split('/')[0][12:]
    plugin_resources_dir = get_resource_directory(plugin_name)
    filepath = os.path.join(plugin_resources_dir, *path.split('/')[1:])
    ct = 'text/plain'
    for key in CTMAP:
        if path.endswith(key):
            ct = CTMAP[key]
            break
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
            return example['routes'][splitted[1]](environ, start_response)
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