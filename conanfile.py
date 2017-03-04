# conanfile for retrieving and building zlib

# This will recipe will also serve as an example for other recipes. That is the
# reason it is more verbose than it needs to be. Should you require more
# background information, please consult the of manual located here:
# https://conanio.readthedocs.io/en/latest/index.html

# Recipes should be stored in a git repository and be updated whenever a newer
# version of the library is released or some other update is required.

# Use Python modules to do basic tasks instead of invoking wget or a similar
# tool so that the recipe is operating system agnostic. Note that Conan offers
# a lot of tools out-of-the-box.
from conans import ConanFile, CMake, tools
import os

# The class name is not really all that important but please ensure that it
# does not clash with any existing Python modules. Here I use the "Conan"
# postfix to do so, which is in line with examples from the official
# documentation.
class ZlibConan(ConanFile):
  name = 'zlib'
  version = "1.2.11"
  license = "zlib" # zlib uses the zlib license
  url = 'https://github.com/k0ekk0ek/conan-zlib'
  settings = 'os', 'compiler', 'build_type', 'arch'
  options = {'shared': [True, False]}
  default_options = 'shared=False'

  # The properties below are for convenience and are not required by Conan.
  source_dir = None
  source_file = None
  source_url = None

  # Strictly speaking it is not required to specify a checksum, but given that
  # the library will be statically linked and distributed with our product, it
  # is important that the third-party sources can be verified to ensure they
  # have not been tampered with. Specifying a checksum retrieved through a
  # secondary channel is the obvious way to do precisly that!
  source_checksum = \
    'c3e5e9fdd5004dcb542feda5ee4f0ff0744628baf8ed2dd5d66f8ca1197cb1a1'


  def __init__(self, *args, **kwargs):
    super(ZlibConan, self).__init__(*args, **kwargs)
    self.source_dir = '{}-{}'.format(self.name, self.version)
    self.source_file = '{}.tar.gz'.format(self.source_dir)
    self.source_url = 'http://www.zlib.net/{}'.format(self.source_file)
  # __init__


  # This method will be invoked to retrieve the sources from the zlib website
  # and prepare them for the build stage that follows.
  def source(self):
    tools.download(self.source_url, self.source_file)
    tools.check_sha256(self.source_file, self.source_checksum)
    tools.unzip(self.source_file, '.')
    os.unlink(self.source_file)
  # source


  def build(self):
    cmake = CMake(self.settings)
    self.run('cmake {} {}'.format(self.source_dir, cmake.command_line))
    self.run('cmake --build . {}'.format(cmake.build_config))
  # build


  # The method takes the artifacts required by dependent packages and places
  # them in the package folder.
  def package(self):
    # Header files
    self.copy('zconf.h', dst='include', keep_path=False)
    self.copy('zlib.h', dst='include', src=self.source_dir, keep_path=False)
    # Libraries
    self.copy('*.lib', dst='lib', keep_path=False)
    self.copy('*.dll', dst='bin', keep_path=False)
    if self.options.shared:
      self.copy('*.so', dst='lib', keep_path=False)
    self.copy('*.a', dst='lib', keep_path=False)
  # package


  # The package_info method defines which configuration is needed to actually
  # consume this package.
  def package_info(self):
    self.cpp_info.libs = ['z']
  # package_info

