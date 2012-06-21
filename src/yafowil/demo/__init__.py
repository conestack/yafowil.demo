import os
import sys
import lxml.html
import lxml.etree
import docutils.core
from docutils import nodes
from docutils.writers.html4css1 import (
    Writer,
    HTMLTranslator,
)
import sphinx.directives
from sphinx.highlighting import PygmentsBridge
from webob import Request, Response
from chameleon import PageTemplateLoader
from yafowil import loader
import yafowil.webob
from yafowil.base import factory
from yafowil.controller import Controller
from yafowil.tests import fxml
from yafowil.utils import (
    Tag,
    get_plugin_names,
    get_resource_directory,
    get_javascripts,
    get_stylesheets,
    get_example_names,
    get_example,
)

dir = os.path.dirname(__file__)

CTMAP = {
    '.js': 'text/javascript',
    '.css': 'text/css',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.jpg': 'image/jpeg',
    '.ico': 'image/x-icon',
}


def python_highlighter():
    return PygmentsBridge('html', 'sphinx', False)


class DocTranslator(HTMLTranslator):
    
    def __init__(self, *args, **kwds):
        HTMLTranslator.__init__(self, *args, **kwds)
        self.highlightlang = 'python'
        self.highlightlinenothreshold = sys.maxint
        self.highlighter = python_highlighter()
    
    def visit_literal_block(self, node):
        if node.rawsource != node.astext():
            # most probably a parsed-literal block -- don't highlight
            return HTMLTranslator.visit_literal_block(self, node)
        lang = self.highlightlang
        linenos = node.rawsource.count('\n') >= \
                  self.highlightlinenothreshold - 1
        highlight_args = node.get('highlight_args', {})
        if node.has_key('language'):
            # code-block directives
            lang = node['language']
            highlight_args['force'] = True
        if node.has_key('linenos'):
            linenos = node['linenos']
        def warner(msg):
            print 'Warning: %s - %s ' % (msg, node.line)
        highlighted = self.highlighter.highlight_block(
            node.rawsource, lang, warn=warner, linenos=linenos,
            **highlight_args)
        starttag = self.starttag(node, 'div', suffix='',
                                 CLASS='highlight-%s' % lang)
        self.body.append(starttag + highlighted + '</div>\n')
        raise nodes.SkipNode


class DocWriter(Writer):
    
    def __init__(self):
        Writer.__init__(self)
        self.translator_class = DocTranslator


def pygments_styles(environ, start_response):
    response = Response(content_type='text/css')
    response.write(python_highlighter().get_stylesheet())
    return response(environ, start_response)


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
        #'resource': 'jquery-ui-1.8.18.css',
        'resource': 'jquery-ui-1.8.16.bootstrap.css',
        'thirdparty': False,
        'order': 10,
    }, {
        'resource': 'yafowil.demo.css',
        'thirdparty': False,
        'order': 20,
    }]


def resource_response(path, environ, start_response, content_type):
    response = Response(content_type=content_type)
    with open(path) as file:
        response.write(file.read())
    return response(environ, start_response)


RESOURCE_DELIVERY_WHITELIST = [
     'yafowil.demo',
     'yafowil.loader',
     'yafowil.bootstrap',
]

def get_resources(current_plugin_name=None):
    all_js = list()
    all_css = list()
    for plugin_name in get_plugin_names():
        whitelist = [current_plugin_name] + RESOURCE_DELIVERY_WHITELIST
        if plugin_name not in whitelist:
            continue
        plugin_resources_dir = get_resource_directory(plugin_name)
        resource_name = '++resource++%s' % plugin_name
        if not (plugin_resources_dir):
            continue
        for js in get_javascripts(plugin_name):
            if not js['resource'].startswith('http'):
                js['resource'] = resource_name + '/' + js['resource']
            all_js.append(js)
        for css in get_stylesheets(plugin_name):
            if not css['resource'].startswith('http'):
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


def render_forms(example, environ, plugin_name):
    result = []
    for part in example:
        record = {}
        widget = part['widget']
        form = factory(
            u'form',
            name=widget.name,
            props={
                'action': '/++widget++%s/index.html' % plugin_name})
        form[widget.name] = widget
        form['submit'] = factory(
            'submit',
            props={
                'label': 'submit',
                'submit.class': 'btn btn-primary',
                'action': 'save',
                'handler': lambda widget, data: None})
        controller = Controller(form, Request(environ))
        record['form'] = controller.rendered
        doc_html = docutils.core.publish_string(part['doc'], writer=DocWriter())
        doc_html = lxml.html.document_fromstring(doc_html)
        doc_html = doc_html.find_class('document')[0]
        doc_html.insert(0, lxml.etree.Element('a', name=widget.name))
        record['doc'] = lxml.html.tostring(doc_html)
        result.append(record)
    return result


def execute_route(example, route, environ, start_response):
    for part in example:
        if 'routes' in part and route in part['routes']:
            return part['routes'][route](environ, start_response)
    raise ValueError('No route to: %s' % environ['PATH_INFO'])


def app(environ, start_response):
    path = environ['PATH_INFO'].strip('/')
    if path == 'favicon.ico':
        return dispatch_resource('++resource++yafowil.demo/favicon.ico',
                                 environ, start_response)
    if path ==  'pygments.css':
        return pygments_styles(environ, start_response)
    if path.startswith('++resource++'):
        return dispatch_resource(path, environ, start_response)
    if path.startswith('++widget++'):
        splitted = path.split('/')
        plugin_name = splitted[0][10:]
        resources = get_resources(plugin_name)
        example = get_example(plugin_name)
        if splitted[1] != 'index.html':
            return execute_route(example, splitted[1], environ, start_response)
        sections = list()
        for section in example:
            sections.append({
                'id': section['widget'].name,
                'title': section.get('title', section['widget'].name),
            })
        forms = render_forms(example, environ, plugin_name)
    else:
        plugin_name = None
        resources = get_resources()
        sections = list()
        forms = None
    templates = PageTemplateLoader(dir)
    template = templates['main.pt']
    body = template(resources=resources,
                    forms=forms,
                    example_names=sorted(get_example_names()),
                    sections=sections,
                    current_name=plugin_name)
    return Response(body=body)(environ, start_response)