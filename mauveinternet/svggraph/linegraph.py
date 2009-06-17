#!/usr/bin/python

import math
import re
import os
import cStringIO

from billing.management.svggraph.svg import xmlentities, Path, Graph
from billing.management.svggraph.table import Table
from billing.management.svggraph.colourscheme import *

class LineGraph(Graph):
	def __init__(self, table, colors=None, width=630, height=300):
		Graph.__init__(self, table, width, height)

		if colors is None:
			self.colors=DefaultColorScheme()
		else:
			self.colors=colors

		self.colwidth=(self.width-20)/(self.table.cols-1)

	def render(self, stream):
		self.svgHeader(stream)
		for r in xrange(self.table.rows):
			self.renderRow(stream, r)
		self.renderAxes(stream)
		if self.table.rows > 1:
			self.renderLegend(stream)
		self.svgFooter(stream)
		
	def renderAxes(self, stream):
		p=Path()
		p.to(9.5, 0)
		p.to(9.5, 159.5)
		p.to(self.width, 159.5)
		p.setClosed(False)
		stream.write('<path d="%s" stroke="black" stroke-width="1" fill="none"/>\n'%p)
		stream.write('<text text-anchor="end" transform="translate(14.5, 164.5) rotate(270)">%s</text>'%xmlentities(self.table.getColumnLabel(0)))
		stream.write('<text text-anchor="end" transform="translate(%.2f, %.2f) rotate(270)">%s</text>'%(14.5+self.colwidth*(self.table.cols-1), 164.5, xmlentities(self.table.getColumnLabel(self.table.cols-1))))
		
	def renderLegend(self, stream):
		for r in xrange(self.table.rows):
			stream.write('<g transform="translate(%0.1f, %0.1f)">'%(5.5, self.height-20.5-20*(self.table.rows-r-1)))
			stream.write('<path d="M 0,5 L 15, 5" stroke="%s" stroke-width="2"/>'%self.colors[r])
			stream.write('<text x="%0.1f" y="%0.1f">%s</text>'%(23, 8, xmlentities(self.table.getRowLabel(r))))
			stream.write('</g>')

	def renderRow(self, stream, r):
		p=Path()
		max=0
		cmax=None
		for c in xrange(self.table.cols):
			v=self.table.getValue(c, r)
			if float(v) >= max:
				max=float(v)
				cmax=c
			x=9.5+self.colwidth*c
			y=159.5-float(v)*130
			stream.write('<circle cx="%.1f" cy="%.1f" r="2" stroke="%s"/>\n'%(x,y,self.colors[r]))
			p.to(x, y)
		p.setClosed(False)
		stream.write('<path d="%s" stroke="%s" stroke-width="2" fill="none"/>\n'%(p, self.colors[r]))
		if cmax != None:
			v=self.table.getValue(cmax, r)
			stream.write('<text x="%0.1f" y="%0.1f" text-anchor="middle" style="fill: %s">%s</text>'%(9.5+self.colwidth*cmax, 149.5-float(v)*130, self.colors[r], str(v)))

class InterpolatingLineGraph(LineGraph):
	def renderRow(self, stream, r):
		p=Path()
		max=0
		cmax=None
		for c in xrange(self.table.cols):
			v=self.table.getValue(c, r)
			if float(v) >= max:
				max=float(v)
				cmax=c
			x=9.5+self.colwidth*c
			y=159.5-float(v)*130
			p.to(x, y)
		p.setClosed(False)
		stream.write('<path d="%s V159.5 H9.5 z" stroke="none" fill="%s" fill-opacity="0.2"/>'%(p.toStringQuadratic(), self.colors[r]))
		for c in p.coords:
			x,y=c
			stream.write('<circle cx="%.1f" cy="%.1f" r="2" fill="%s"/>\n'%(x,y, self.colors[r]))
		stream.write('<path d="%s" stroke="%s" stroke-width="2" fill="none"/>\n'%(p.toStringQuadratic(), self.colors[r]))
		if cmax != None:
			v=self.table.getValue(cmax, r)
			stream.write('<text x="%0.1f" y="%0.1f" text-anchor="middle" style="fill: %s">%s</text>'%(9.5+self.colwidth*cmax, 149.5-float(v)*130, self.colors[r], str(v)))

