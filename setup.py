from setuptools import setup, find_packages

setup(
    name="pylogops",
    version="1.0.0",
    url='http://github.com/telefonicaid/pylogops',
    license='BSD',
    platforms=['OS Independent'],
    description="A simple json formatter for python logging.",
    long_description=open('README.md').read(),
    author='Eduardo Alonso',
    author_email='eduardo.alonsogarcia@telefonica.com',
    maintainer='Eduardo Alonso',
    maintainer_email='eduardo.alonsogarcia@telefonica.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    zip_safe=False,
    classifiers=[
        'Framework :: Python',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)
