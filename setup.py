import os

from setuptools import setup

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name='pyMPM',
    version='0.1.0',
    description='Python version of the MPM millimeter wave propagation model',
    url='http://github.com/cchwala/pyMPM',
    license='BSD',
    author='Christian Chwala',
    author_email='christian.chwala@kit.edu',
    packages=['pyMPM'],
    include_package_data=True,
    install_requires=['Numpy'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "License :: OSI Approved :: BSD License",
        'Programming Language :: Python :: 2.7',
    ],
    keywords='microwave propagation atmosphere'
    
)
