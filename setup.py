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
        'Werkzeug==0.14.1',
        'flask_swagger_ui==3.18.0',
        'flask_restplus==0.12.1',
        'sphinx_press_theme==0.1.1',
        'passlib==1.7.1',
        'bcrypt==3.1.5'
    ],
    entry_points={
        'console_scripts': ['crudcast=crudcast.entrypoint:main'],
    }
)
