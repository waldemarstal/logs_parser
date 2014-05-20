from distutils.core import setup
from setuptools import find_packages


setup(
    name='logs_parser',
    version='1',
    author='Waldemar Stal',
    author_email='waldemar.stal@gmail.com',
    packages=find_packages(),
    description='logs_parser',
    long_description='README.md',
    install_requires=[],
    entry_points="""\
    [console_scripts]
    logs_parser = lib.scripts:main
    """,
)