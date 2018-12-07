import os
from setuptools import find_packages, setup
from crudcast import __version__

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
name = 'crudcast'
version = __version__

setup(
    name=name,
    version=version,
    packages=find_packages(),
    package_data={'crudcast': ['requirements.txt']},
    include_package_data=True,
    license='Apache Software License',
    long_description='',
    author='Christopher Davies',
    author_email='christopherdavies553@gmail.com',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'Click==7.0',
        'Flask==1.0.2',
        'itsdangerous==1.1.0',
        'Jinja2==2.10',
        'MarkupSafe==1.1.0',
        'pymongo==3.7.2',
        'PyYAML==3.13',
        'Werkzeug==0.14.1'
    ],
    entry_points={
        'console_scripts': ['crudcast=crudcast.entrypoint:main'],
    }
)
