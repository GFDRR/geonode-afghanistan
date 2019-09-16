import os
from distutils.core import setup

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name="afg",
    version="2.10.1",
    author="",
    author_email="",
    description="afg, based on GeoNode",
    long_description=(read('README.rst')),
    # Full list of classifiers can be found at:
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
    license="BSD",
    keywords="afg geonode django",
    url='https://github.com/afg/afg',
    packages=['afg',],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
    ]
)
