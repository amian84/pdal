#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, glob

try:
    import DistUtilsExtra.auto
    from distutils.core import setup, Command
    from DistUtilsExtra.command import *
except ImportError:
    print >> sys.stderr, 'To build firstboot you need https://launchpad.net/python-distutils-extra'
    sys.exit(1)
assert DistUtilsExtra.auto.__version__ >= '2.18', 'needs DistUtilsExtra.auto >= 2.18'

# Get current Python version

# Setup the default install prefix
#prefix = sys.prefix
#oldvalue=None
# Check our python is version 2.6 or higher
#if python_version[0] >= 2 and python_version[1] >= 6:
    ## Set file location prefix accordingly
 #   prefix = '/usr/local'

# Get the install prefix if one is specified from the command line
#for arg in sys.argv:
#    if arg.startswith('--prefix='):
#        prefix = arg[9:]
#        prefix = os.path.expandvars(prefix)

def update_rules(prefix):

    for filename in ['udev-rules/99-pdal.rules']:
        infile = open(filename + '.in', 'r')
        data = infile.read().replace('@PREFIX@', prefix)
        infile.close()

        outfile = open(filename, 'w')
        outfile.write(data)
        outfile.close()

def update_config(values={}):

    oldvalues = {}
    try:
        fin = file('firstboot_lib/firstbootconfig.py', 'r')
        fout = file(fin.name + '.new', 'w')

        for line in fin:
            fields = line.split(' = ') # Separate variable from value
            if fields[0] in values:
                oldvalues[fields[0]] = fields[1].strip()
                line = "%s = %s\n" % (fields[0], values[fields[0]])
            fout.write(line)

        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError), e:
        print ("ERROR: Can't find firstboot_lib/firstbootconfig.py")
        sys.exit(1)
    return oldvalues


class InstallAndUpdateDataDirectory(DistUtilsExtra.auto.install_auto):
    def run(self):
        values = {'__pdal_data_directory__': "'%s'" % (self.prefix + '/share/pdal/'),
                  '__license__': "'%s'" % self.distribution.get_license(),
                  '__firstboot_prefix__': "'%s'" % self.prefix}
        previous_values = update_config(values)
        update_rules(self.prefix + '/share/pdal/')
        DistUtilsExtra.auto.install_auto.run(self)
        update_config(previous_values)


class Clean(Command):
    description = "custom clean command that forcefully removes dist/build directories and update data directory"
    user_options = []
    def initialize_options(self):
        self.cwd = None
    def finalize_options(self):
        self.cwd = os.getcwd()
    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        os.system('rm -rf ./build ./dist')
        os.system('rm -rf udev-rules/99-pdal.rules')



#def update_data_path(prefix, oldvalue_data=None, oldvalue_prefix=None):
#    try:
#        fin = file('pdal/pdalconfig.py', 'r')
#        fout = file(fin.name + '.new', 'w')
#
#        for line in fin:
#            fields = line.split(' = ') # Separate variable from value
#            if fields[0] == '__pdal_data_directory__':
#                # update to prefix, store oldvalue
#                if not oldvalue_data:
#                    oldvalue_data = fields[1]
#                    line = "%s = '%s'\n" % (fields[0], prefix)
#                else: # restore oldvalue
#                    line = "%s = %s" % (fields[0], oldvalue_data)
#            
#            if fields[0] == '__pdal_prefix__':
#                if not oldvalue_prefix:
#                    oldvalue_prefix = fields[1]
#                    line = "%s = '%s'\n" % (fields[0], prefix)
#                else: # restore oldvalue
#                    line = "%s = %s" % (fields[0], oldvalue_prefix)
#
#            fout.write(line)
#
#        fout.flush()
#        fout.close()
#        fin.close()
#        os.rename(fout.name, fin.name)
#    except (OSError, IOError), e:
#        print ("ERROR: Can't find pdal/pdalconfig.py")
#        sys.exit(1)
#    return (oldvalue_data, oldvalue_prefix)

#oldvalue=update_data_path(prefix + '/share/pdal/')
#update_data_path(prefix + '/share/pdal/')


#class Clean(Command):
#    description = "custom clean command that forcefully removes dist/build directories and update data directory"
#    user_options = []
#    def initialize_options(self):
#        self.cwd = None
#    def finalize_options(self):
#        self.cwd = os.getcwd()
#    def run(self):
#        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
#        os.system('rm -rf ./build ./dist')
#        update_data_path(prefix, oldvalue)



# Gen .in files with @PREFIX@ replaced
#for filename in ['udev-discover']:
#    infile = open(filename + '.in', 'r')
#    data = infile.read().replace('@PREFIX@', prefix)
#    infile.close()
#
#    outfile = open(filename, 'w')
#    outfile.write(data)
#    outfile.close()


setup(
        name='pdal2',
        version='0.3.2',
        license='GPL-2',
        author='David Amian Valle',
        author_email='damian@emergya.com',
        description='PDAL (Pluggable Device Action Launcher)',
        url='https://github.com/amian84/pdal',


        keywords = ['python', 'udev', 'gnome'],

        packages = ['pdal'], 
        package_dir =  {'pdal': 'pdal'},

        scripts = ['bin/pdal'],
        
        data_files = [
            ('/etc/udev/rules.d', ['udev-rules/99-pdal.rules']),
            ('share/pdal/scripts/', glob.glob('data/scripts/README')),
            ('share/pdal/scripts/', glob.glob('data/scripts/README')),
            ('share/pdal/media', glob.glob('data/media/*')),
        ],
        cmdclass = { 
            'install': InstallAndUpdateDataDirectory,                 
            "build" : build_extra.build_extra,
            "build_i18n" :  build_i18n.build_i18n,
            "clean": [clean_i18n.clean_i18n, Clean],
            
        }
)
