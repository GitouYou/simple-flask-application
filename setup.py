from setuptools import setup

__version__ = "0.1"

version_url = 'https://github.com/joaofreires/simple-flask-application'

setup(
    name='simple_flask_app',
    version=__version__,
    url='https://github.com/joaofreires/simple-flask-application',
    download_url=version_url,
    license='MIT',
    author='Joao Freires',
    author_email='rmjoaovictor@gmail.com',
    description='A flask example using mustachejs',
    keywords=['flask', 'api', 'flask-example'],
    install_requires=['flask', 'nap'],
    entry_points={'console_scripts': ['simple-flask-app=app']},
    )
