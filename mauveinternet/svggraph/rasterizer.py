#!/usr/bin/python

import os
import popen2
import select

class GraphRasterizer(object):
	def __init__(self, graph):
		self.graph=graph

	def asPNG(self):
		return self.__rasterize('image/png', '.png')

	def asJPEG(self):
		return self.__rasterize('image/jpeg', '.jpg')
		
	def __rasterize(self, mimetype, ext):
		tmpfile=os.tempnam()
		f=open(tmpfile, 'w')
		self.graph.render(f)
		f.close()
		
		outtmpfile=tmpfile+ext

		proc=popen2.Popen4('/usr/bin/rasterizer -scriptSecurityOff -m %s %s'%(mimetype, tmpfile))
		self.graph.render(proc.tochild)
		proc.tochild.close()
		out=''
		while proc.poll() == -1:
			i, o, s=select.select([proc.fromchild], [], [], 100)
			if proc.fromchild in i:
				out+=proc.fromchild.read()

		out+=proc.fromchild.read()
		
		try:
			f=open(outtmpfile, 'rb')
			image=f.read()
			f.close()
		except IOError:
			return out

		os.unlink(tmpfile)
		os.unlink(outtmpfile)
		return image
