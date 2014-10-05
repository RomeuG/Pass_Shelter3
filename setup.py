from setuptools import setup, find_packages
from os.path import join, dirname
from src.version import __version__

setup(
        name='pass_shelter',
        version=__version__,
        author='Romeu Gomes',
        author_email='romeu.bizz@gmail.com',
        url='',
        license=open(join(dirname(__file__), 'LICENSE.txt')).read(),
        packages=find_packages(),
        description='Simple command-line password manager',
        long_description=open(join(dirname(__file__), 'README.md')).read(),
        install_requires=[
                'keyring',
                'bcrypt',
                'pycrypto',
            ],
        classifiers=[
            'Programming Language :: Python :: 3.4',
            'License :: OSI Approved :: MIT License',
            'Environment :: Console',
            'Topic :: Security',
            'Topic :: Utilities',
            'Development Status :: 5 - Production/Stable',
            ],
        entry_points={
            'console_scripts':
                ['passshelter = src.main:main_function']
        }
    )
