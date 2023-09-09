from setuptools import setup, find_packages

requires = {
    'flask',
    'spotipy',
    'requests',
    'requests_html',
    'beautifulsoup4',
    'youtube_dl',
    'pathlib',
    'pandas'
}

setup(
    name='Flaskapp',
    version='1.0',
    description='basic spotify flask app',
    author='Jaskaran Gill',
    author_email='jaskarangill2014@gmail.com',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[requires]
)