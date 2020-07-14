from setuptools import setup, find_packages

def get_requirements():
    reqs_file = 'requirements.txt'
    try:
        with open(reqs_file) as reqs_file:
            reqs = filter(None, map(lambda line: line.replace('\n', '').strip(), reqs_file))
            return list(reqs)
    except IOError:
        pass
    return []

setup(
    name="pylogops",
    version="1.2.0",
    url='http://github.com/telefonicaid/pylogops',
    license='BSD',
    platforms=['OS Independent'],
    description="A simple json formatter for python logging.",
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    author='Eduardo Alonso',
    author_email='eduardo.alonsogarcia@telefonica.com',
    maintainer='Eduardo Alonso',
    maintainer_email='eduardo.alonsogarcia@telefonica.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=get_requirements(),
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)
