#!/usr/bin/env python
import os
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

# When one runs pip install from the git repo, the setup.ini
# doesn't exist. But we still have here a full git repo with
# all the git log and with the Makefile.
#
# So just try to use it.
try:
    os.stat('setup.ini')
except:
    os.system('make force-version')
config = configparser.ConfigParser()
config.read('setup.ini')

module = __import__(config.get('setup', 'setuplib'),
                    globals(),
                    locals(),
                    ['setup'], 0)
setup = getattr(module, 'setup')

readme = open("README.md", "r")


setup(name='dtcd',
      version=config.get('setup', 'release'),
      description='Dynamic network blocks allocation via HTTP',
      author='Peter V. Saveliev',
      author_email='peter@svinota.eu',
      url='https://github.com/svinota/dtcd',
      license='dual license GPLv2+ and Apache v2',
      packages=['dtcd',],
      scripts=['./src/dtcd', ]
      classifiers=['License :: OSI Approved :: GNU General Public ' +
                   'License v2 or later (GPLv2+)',
                   'License :: OSI Approved :: Apache Software License',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: ' +
                   'Python Modules',
                   'Topic :: System :: Networking',
                   'Topic :: System :: Systems Administration',
                   'Operating System :: POSIX :: Linux',
                   'Intended Audience :: Developers',
                   'Intended Audience :: System Administrators',
                   'Intended Audience :: Telecommunications Industry',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Development Status :: 4 - Beta'],
      long_description=readme.read())
