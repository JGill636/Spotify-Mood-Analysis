from setuptools import setup, find_packages

requires = [
    'Flask',
    'spotipy',
    'python-dotenv',
]

setup(
    name='Flaskapp',
    version='1.0',
    description='Basic Spotify Flask app',
    author='Jaskaran Gill',
    author_email='jaskarangill2014@gmail.com',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)
