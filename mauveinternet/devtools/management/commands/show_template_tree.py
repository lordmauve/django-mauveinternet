import os
import re

from django.core.management.base import NoArgsCommand
from django.conf import settings

"""Management command for generating graphviz .DOT files of the template
inheritance path, for template debugging and maintenance"""

class InvalidTemplate(Exception):
	"""Because we cannot determine which files we encounter genuinely are
	Django templates, we must attempt to read them and consider them if
	they are valid Django templates in the correct character set.
	
	This Exception is raised when a template is not valid."""


class InheritanceGraph(object):
	def __init__(self):
		self.templates = {}

	def add_template(self, name, extends=None, includes=[]):
		self.templates[name] = extends, includes

	def as_dot(self):
		node_defs = ''
		nodes = {}
		i = 1
		for k, v in self.templates.items():
			extends, includes = v
			nodes[k] = extends, includes, 'node%d' % i
			i += 1

		ks = nodes.keys()
		ks.sort()

		for k in ks:
			extends, includes, node = nodes[k]
			node_defs += "\t%s [label=\"%s\"];\n" % (node, k)

		inheritance_edges = ''
		inclusion_edges = ''

		for t, v in nodes.items():
			extends, includes, node = v
			if extends is not None:
				e = nodes.get(extends.encode('utf8'), None)
				if e:
					inheritance_edges += "\t%s -> %s;\n" % (node, e[2])
			for include in includes:
				e = nodes.get(include.encode('utf8'), None)
				if e:
					inclusion_edges += "\t%s -> %s;\n" % (node, e[2])
		
		return """digraph template_tree {
	graph [rankdir=LR];
	node [shape=box,fontname="Arial",fontsize=10,style="filled",fillcolor="#EEEEFF",color="#8888CC"];
	%s
	%s
	edge [color=blue];
	%s
}""" % (node_defs, inheritance_edges, inclusion_edges)


class Command(NoArgsCommand):
	requires_model_validation = False

	def handle_noargs(self, **options):
		graph = InheritanceGraph()

		if 'django.template.loaders.app_directories.load_template_source' in settings.TEMPLATE_LOADERS:
			self.search_app_directories(graph)

   		if 'django.template.loaders.filesystem.load_template_source' in settings.TEMPLATE_LOADERS:
			self.search_filesystem(graph)

		print graph.as_dot()

	def inspect_template(self, path):
		f = open(path, 'rU')
		try:
			templ = f.read().decode(settings.FILE_CHARSET)
		except UnicodeDecodeError:
			raise InvalidTemplate('%s is not a valid Django template' % path)
		finally:
			f.close()

		templ = re.sub(r'{#.*?#}', '', templ)
		templ = re.sub(r'\{%\s*comment\s*%\}.*?\{%\s*endcomment\s*%\}', '', templ)

		mo = re.match(r'^\s*\{%\s*extends\s+"([^"]+)"\s*%\}', templ)

		if mo:
			extends = mo.group(1)
		else:
			extends = None

		includes = []
		for mo in re.finditer(r'\{%\s*include\s+"([^"]+)"\s*%\}', templ):
			includes.append(mo.group(1))

		return extends, includes

	def search_app_directories(self, graph):
		from django.template.loaders.app_directories import app_template_dirs
		for d in app_template_dirs:
			for f in self.search_directory(d):
				try:
					extends, includes = self.inspect_template(f)
				except InvalidTemplate:
					continue
				fname = f[len(d):]
				if fname.startswith('/'):
					fname = fname[1:]
				graph.add_template(fname, extends, includes)

	def search_filesystem(self, graph):
		for d in settings.TEMPLATE_DIRS:
			for f in self.search_directory(d):
				try:
					extends, includes = self.inspect_template(f)
				except InvalidTemplate:
					continue
				fname = f[len(d):]
				if fname.startswith('/'):
					fname = fname[1:]
				graph.add_template(fname, extends, includes)

	def search_directory(self, dir):
		for root, dirs, files in os.walk(dir):
			for excl in ['.svn', 'CVS']:
				if excl in dirs:
					dirs.remove(excl)
			for f in files:
				yield os.path.join(root, f)
