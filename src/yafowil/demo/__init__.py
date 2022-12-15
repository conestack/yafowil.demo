from chameleon import PageTemplateLoader
from docutils import nodes
from docutils.writers.html4css1 import HTMLTranslator
from docutils.writers.html4css1 import Writer
from sphinx.highlighting import PygmentsBridge
from webob import Request
from webob import Response
from wsgiref.util import request_uri
from yafowil.base import factory
from yafowil.compat import IS_PY2
from yafowil.controller import Controller
from yafowil.utils import get_example
from yafowil.utils import get_example_names
import docutils.core
import lxml.etree
import lxml.html
import os
import sys
import traceback
import webresource as wr
import yafowil.loader  # noqa
import yafowil.webob  # noqa
import treibstoff # noqa


curdir = os.path.dirname(__file__)


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
        self.highlightlinenothreshold = sys.maxint if IS_PY2 else sys.maxsize
        self.highlighter = python_highlighter()

    def visit_literal_block(self, node):
        if node.rawsource != node.astext():
            # most probably a parsed-literal block -- don't highlight
            return HTMLTranslator.visit_literal_block(self, node)
        lang = self.highlightlang
        linenos = node.rawsource.count('\n') >= \
            self.highlightlinenothreshold - 1
        highlight_args = node.get('highlight_args', {})
        if 'language' in node:
            # code-block directives
            lang = node['language']
            highlight_args['force'] = True
        if 'linenos' in node:
            linenos = node['linenos']

        def warner(msg):
            print('Warning: %s - %s ' % (msg, node.line))

        highlighted = self.highlighter.highlight_block(
            node.rawsource,
            lang,
            warn=warner,
            linenos=linenos,
            **highlight_args
        )
        starttag = self.starttag(
            node,
            'div',
            suffix='',
            CLASS='highlight-%s' % lang
        )
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


_file_cache = {}


def resource_response(path, environ, start_response, content_type):
    response = Response(content_type=content_type)
    if path not in _file_cache:
        with open(path, 'rb') as fd:
            _file_cache[path] = fd.read()
    response.write(_file_cache[path])
    return response(environ, start_response)


group_map = {}
directory_map = {}
resources_loaded = False


def load_resources():
    global resources_loaded
    if resources_loaded:
        return
    resources = factory.get_resources()
    for group in resources.members:
        group_map[group.name] = group
        directory_map['++resource++{}'.format(group.path)] = group.directory
    for script in resources.scripts:
        script.path = '++resource++{}'.format(script.path)
    for style in resources.styles:
        style.path = '++resource++{}'.format(style.path)
    resources_loaded = True


def get_resources(widget_name=None):
    load_resources()
    group = wr.ResourceGroup()
    group.add(group_map['treibstoff'])
    group.add(group_map['yafowil.demo'])
    group.add(group_map['yafowil.bootstrap'])
    if isinstance(widget_name, list):
        for name in widget_name:
            if name not in [None, 'yafowil']:
                group.add(group_map[name])
    else:
        if widget_name not in [None, 'yafowil']:
            group.add(group_map[widget_name])
    return group


def rendered_resources(resources):
    resolver = wr.ResourceResolver(resources)
    renderer = wr.ResourceRenderer(resolver, base_url='')
    return renderer.render()


def rendered_scripts(widget_name=None):
    # provide resources for use of other widgets in yafowil.widget.array
    if widget_name == 'yafowil.widget.array':
        widget_name = [
            'yafowil.widget.ace',
            'yafowil.widget.array',
            'yafowil.widget.autocomplete',
            'yafowil.widget.color',
            'yafowil.widget.chosen',
            'yafowil.widget.cron',
            'yafowil.widget.datetime',
            'yafowil.widget.dict',
            'yafowil.widget.image',
            'yafowil.widget.location',
            'yafowil.widget.multiselect',
            'yafowil.widget.richtext',
            'yafowil.widget.select2',
            'yafowil.widget.slider',
            'yafowil.widget.tiptap',
            'yafowil.widget.wysihtml5',
        ]
    return rendered_resources(get_resources(widget_name).scripts)


def rendered_styles(widget_name=None):
    # provide resources for use of other widgets in yafowil.widget.array
    if widget_name == 'yafowil.widget.array':
        widget_name = [
            'yafowil.widget.ace',
            'yafowil.widget.array',
            'yafowil.widget.autocomplete',
            'yafowil.widget.color',
            'yafowil.widget.chosen',
            'yafowil.widget.cron',
            'yafowil.widget.datetime',
            'yafowil.widget.dict',
            'yafowil.widget.image',
            'yafowil.widget.location',
            'yafowil.widget.multiselect',
            'yafowil.widget.richtext',
            'yafowil.widget.select2',
            'yafowil.widget.slider',
            'yafowil.widget.tiptap',
            'yafowil.widget.wysihtml5',
        ]
    return rendered_resources(get_resources(widget_name).styles)


def dispatch_resource(path, environ, start_response):
    base_path = path.split('/')[0]
    rel_path = os.path.join(*path.split('/')[1:])
    file_path = os.path.join(directory_map[base_path], rel_path)
    ct = 'text/plain'
    for key in CTMAP:
        if path.endswith(key):
            ct = CTMAP[key]
            break
    return resource_response(file_path, environ, start_response, ct)


def dummy_save(widget, data):
    print(data.extracted)


def render_forms(example, environ, widget_name):
    result = []
    for part in example:
        record = {}
        widget = part['widget']
        action = '/++widget++%s/index.html#%s' % (widget_name, widget.name)
        form = factory(
            u'#form',
            name=widget.name,
            props={
                'action': action
            })
        form[widget.name] = widget
        form['form_actions'] = factory(
            'div',
            props={
                'class': 'form-actions',
                'structural': True,
            })
        handler = part.get('handler', dummy_save)
        form['form_actions']['submit'] = factory(
            'field:div:#button',
            props={
                'label': 'submit',
                'action': 'save',
                'div.class_add': 'col-sm-offset-2 col-sm-10',
                'handler': handler,
                'next': lambda req: True
            })
        controller = Controller(form, Request(environ))
        if controller.next:
            record['form'] = form()
        else:
            record['form'] = controller.rendered
        doc_html = docutils.core.publish_string(
            part['doc'],
            writer=DocWriter()
        )
        doc_html = lxml.html.document_fromstring(doc_html)
        doc_html = doc_html.find_class('document')[0]
        doc_html.insert(0, lxml.etree.Element('a', name=widget.name))
        record['doc'] = lxml.html.tostring(doc_html)
        result.append(record)
    return result


def execute_route(example, route, environ, start_response):
    for part in example:
        if 'routes' in part and route in part['routes']:
            url = request_uri(environ)
            result = part['routes'][route](url)
            # XXX todo: set headers generic
            response = Response(
                content_type='application/json',
                body=result['body'],
                charset='UTF-8'
            )
            return response(environ, start_response)
    raise ValueError('No route to: %s' % environ['PATH_INFO'])


def format_traceback():
    etype, value, tb = sys.exc_info()
    ret = ''.join(traceback.format_exception(etype, value, tb))
    return '<pre>%s</pre>' % ret


def app(environ, start_response):
    try:
        path = environ['PATH_INFO'].strip('/')
        if path == 'favicon.ico':
            return dispatch_resource(
                '++resource++yafowil-demo/favicon.ico',
                environ, start_response
            )
        if path == 'pygments.css':
            return pygments_styles(environ, start_response)
        if path.startswith('++resource++'):
            return dispatch_resource(path, environ, start_response)
        if path.startswith('++widget++'):
            splitted = path.split('/')
            widget_name = splitted[0][10:]
            example = get_example(widget_name)
            if splitted[1] != 'index.html':
                return execute_route(
                    example,
                    splitted[1],
                    environ,
                    start_response
                )
            sections = list()
            for section in example:
                sections.append({
                    'id': section['widget'].name,
                    'title': section.get('title', section['widget'].name),
                })
            forms = render_forms(example, environ, widget_name)
        else:
            widget_name = None
            sections = list()
            forms = None
        templates = PageTemplateLoader(curdir)
        template = templates['main.pt']
        body = template(
            scripts=rendered_scripts(widget_name),
            styles=rendered_styles(widget_name),
            forms=forms,
            example_names=sorted(get_example_names()),
            sections=sections,
            current_name=widget_name
        )
        return Response(body=body)(environ, start_response)
    except Exception:
        return Response(body=format_traceback())(environ, start_response)
