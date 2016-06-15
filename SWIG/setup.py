#!/usr/bin/env python
"""
usage:
python setup.py build_ext --inplace
"""
#import commands
#flag = commands.getstatusoutput('swig -c++ -python splinalg.i')
cmd = 'swig -c++ -python splinalg.i'
import subprocess
pipe = subprocess.Popen(cmd, shell=True, universal_newlines=True,
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
output = str.join("", pipe.stdout.readlines())
sts = pipe.wait()
if sts is not None:
    print(output)
    exit()

from numpy.distutils.core import setup, Extension
import numpy
numpy_include = numpy.get_include()

splinalg_module = Extension('_splinalg', sources=['splinalg_wrap.cxx'], define_macros=[('__STDC_FORMAT_MACROS', 1)],
                            include_dirs=[numpy_include])
setup (name = 'splinalg',
       version = '0.1',
       author      = "Luke Olson",
       description = """basic sparse linear algebra""",
       ext_modules = [splinalg_module],
       py_modules = ["splinalg"],
       )

#   def configuration(parent_package='',top_path=None):
#       from numpy.distutils.misc_util import Configuration
#   
#       config = Configuration()
#   
#       config.add_extension('_splinalg',
#               define_macros=[('__STDC_FORMAT_MACROS', 1)],
#               sources=['splinalg_wrap.cxx'])
#   
#       return config
#   
#   if __name__ == '__main__':
#       from numpy.distutils.core import setup
#       setup(**configuration(top_path='').todict())
