from setuptools import setup, find_packages


setup(
    name='django-mauveinternet',
    version='1.0',
    description="A collection of extensions for Django developed by Mauve Internet",
    author='Daniel Pope',
    author_email='dan@mauveinternet.co.uk',
    url='http://pypi.python.org/pypi/django-mauveinternet',
    packages=find_packages(),
    install_requires=[
        'Pillow>=2.3,<2.4',
        'Markdown>=2.6,<2.7'
    ],
)
