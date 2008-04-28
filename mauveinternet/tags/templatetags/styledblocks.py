from django.template import Node, Library, resolve_variable, TemplateSyntaxError, loader
from django.conf import settings
from django.utils.safestring import mark_safe

register = Library()

class WrapWithNode(template.Node):
	"""Includes another template to style the contents of this tag.
	
	This is similar to {% include %}, except that it takes tag
	contents which are rendered and passed to the included template
	as an additional variable {{ wrapped }}.

	"""
	def __init__(self, template_name, nodelist):
		self.nodelist = nodelist
		self.template_name = template_name

	def render(self, context):
		t = loader.get_template(self.template_name)
		wrapped = self.nodelist.render(context)
		context.update({'wrapped': mark_safe(wrapped)})
		output = t.render(context)
		context.pop()
		return output


@register.tag
def wrapwith(parser, token):
        try:
                # split_contents() knows not to split quoted strings.
                name, template_name = token.split_contents()
        except ValueError:
                raise TemplateSyntaxError, "%r tag requires exactly one arguments" % name

	nodelist = parser.parse(('endwrapwith',))
	parser.delete_first_token()	# consume {% endwrapwith %} tag

	return WrapWithNode(template_name, nodelist)
