#!/usr/bin/pyhton

import sys
import os
import os.path

COMPONENTS = ['css', 'images', 'js', 'icons']
MARKDOWN_PATH = os.path.dirname(sys.argv[0])

def relpath(path, start=None):
	"""Return a relative version of a path.
	Taken from Python3.0 and backported"""

	if not path:
		raise ValueError("no path specified")

	curdir = '.'
	sep = '/'
	pardir = '..'

	if start is None:
		start = curdir

	start_list = os.path.abspath(start).split(sep)
	path_list = os.path.abspath(path).split(sep)

	# Work out how much of the filepath is shared by start and path.
	i = len(os.path.commonprefix([start_list, path_list]))

	rel_list = [pardir] * (len(start_list)-i) + path_list[i:]
	if not rel_list:
		return curdir
	return os.path.join(*rel_list)


def install(target):
	for d in COMPONENTS:
		print d
		tpath = os.path.join(target, d)
		if not os.path.exists(tpath):
			os.mkdir(tpath)
		lpath = os.path.join(tpath, 'markdown')
		dpath = os.path.join(MARKDOWN_PATH, d)
		os.symlink(relpath(dpath, start=os.path.dirname(lpath)), lpath)

def uninstall(target):
	for d in COMPONENTS:
		print d
		lpath = os.path.join(target, d, 'markdown')
		if os.path.islink(lpath):
			os.unlink(lpath)

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-i", "--install",
                  action="store_true",
                  help="install Markdown editor assets")
parser.add_option("-u", "--uninstall",
                  action="store_true",
                  help="uninstall Markdown assets")

(options, args) = parser.parse_args()

if options.uninstall == options.install:
	parser.error('You must choose either to install --install or --uninstall')
elif len(args) != 1:
	parser.error("You must choose a target directory to install or uninstall")
elif options.uninstall:
	print "Uninstalling Markdown assets from", os.path.abspath(args[0])
	uninstall(args[0])
else:
	print "Installing Markdown assets to", os.path.abspath(args[0])
	install(args[0])
