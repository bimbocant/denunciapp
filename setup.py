try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'denunciapp',
    'author': 'bimbocant',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'davidcantero.99@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': find_packages(),
    'scripts': [],
    'name': 'denunciapp'
}

setup(**config)
