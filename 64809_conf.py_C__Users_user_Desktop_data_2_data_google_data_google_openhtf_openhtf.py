# Copyright 2014 Google Inc. All Rights Reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Interface to OpenHTF configuration files.

As a matter of convention, OpenHTF configuration files should contain values
which are specific to an individual station (not station type).  This is
intended to provide a means to decouple deployment of test code from
station-specific configuration or calibration.

Examples of the types of values commonly found in the configuration are
physical port names, IP addresses, calibrated light/sound levels, etc.
Configuration values should not be used to determine test flow, or to control
debug output.

Config keys must be declared as in the following example, where default_value
and description are optional:

  from openhtf import conf

  conf.Declare('antimatter_intermix_constant',
               default_value=3.14159,
               description='Intermix constant calibrated for our warp core.')

Declared keys can be accessed directly as attributes of the conf module.  To
avoid naming conflicts, configuration keys must begin with a lowercase letter.
They may also be accessed by treating the conf module as a dictionary, but this
method is discouraged and should only be used in favor of getattr().

  from openhtf import conf

  warp_core.SetIntermixConstant(conf.antimatter_intermix_constant)

  # An example of when you might use dict-like access.
  for idx in range(5):
    warp_core.SetDilithiumRatio(idx, conf['dilthium_ratio_%s' % idx])

Another common mechanism for obtaining configuration values is to use the
conf.InjectPositionalArgs decorator:

  from openhtf import conf

  @conf.InjectPositionalArgs
  def ModifyThePhaseVariance(antimatter_intermix_constant, phase_variance):
    return antimatter_intermix_constant * phase_variance

  # antimatter_intermix_constant will be taken from the configuration value.
  x = ModifyThePhaseVariance(phase_variance=2.71828)

Decorating a function with conf.InjectPositionalArgs forces all other arguments
to be passed by keyword in order to avoid ambiguity in the values of positional
args.  Values passed via keyword that also exist in the config will override
config values and log a warning message.  Keyword args in the function
declaration will not be overridden (because it would be ambiguous which default
to use), and any overlap in keyword arg names and config keys will result in a
warning message.

If the configuration key is declared but no default_value is provided and no
value has been loaded, then no value will be passed, and a TypeError will be
raised unless the value is passed via keyword.  Essentially, if `keyword_arg in
conf` evaluates to True, then that keyword arg will be provded from the
configuration unless overriden in the kwargs passed to the function.  Otherwise
keyword_arg must be passed via kwargs at function invokation time.

Incidentally, the conf module supports 'in' checks, where `key in conf` will
evaluate to True if conf[key] would successfully provide a value.  That is, if
either a value has been loaded or a default_value was declared.

Configuration values may be loaded directly or from a yaml or json file.  If no
configuration is loaded, default values will still be accessible.  Loading a
configuration always overrides default values, but only overrides previously
loaded values if _override=True (default) for the Load* method used.  Some
examples of how to load a configuration:

  from openhtf import conf

  conf.Declare('antimatter_intermix_constant')
  conf.Declare('phase_variance')

  conf.Load(antimatter_intermix_constant=3.14,
            phase_variance=2.718)
  conf.LoadFromDict({
      'antimatter_intermix_constant': 3.14,
      'phase_variance': 2.718,
  })
  conf.LoadFromFile('config.json')
  conf.LoadFromFile('config.yaml')

Note that any of the Load* methods here accept an _override keyword argument
that defaults to True, but may be set False to prevent overriding previously
loaded values.  Regardless of whether _override is True or False, a message
will be logged indicating how the duplicate value was handled.

conf.LoadFromFile() attempts to parse the filename given as JSON and as YAML,
if neither succeeds, an exception will be raised.  In either case, the value
parsed must be a dictionary mapping configuration key to value.  Complex
configuration values are discouraged; they should be kept to single values or
lists of values when possible.

Lastly, configuration values may also be provided via the --config-value flag,
but this is discouraged, and should only be used for debugging purposes.

Configuration values loaded via commandline flags, either --config-file or
--config-value, are not checked against Declarations.  This allows for using
configuration files that are supersets of required configuration.  Declarations
are *always* checked upon configuration value access, however, so you still
must declare any keys you wish to use.

Loaded configuration values may be purged via the Reset() method, but this
should only be used for testing purposes.
"""

import argparse
import functools
import inspect
import logging
import sys
import threading
import yaml

import mutablerecords

from openhtf.util import argv
from openhtf.util import threads

# If provided, --config-file will cause the given file to be Load()ed when the
# conf module is initially imported.
ARG_PARSER = argv.ModuleParser()
ARG_PARSER.add_argument(
    '--config-file', type=argparse.FileType('r'),
    help='File from which to load configuration values.')

ARG_PARSER.add_argument(
    '--config-value', action='append', default=[],
    help='Allows specifying a configuration key=value on the command line. '
    'The format should be --config-value=key=value. This value will override '
    'any loaded value, and will be a string.')


class Configuration(object):  # pylint: disable=too-many-instance-attributes
  """A singleton class to replace the 'conf' module.

  This class provides the configuration interface described in the module
  docstring.  All attribuets/methods must not begin with a lowercase letter so
  as to avoid naming conflicts with configuration keys.
  """

  class ConfigurationInvalidError(Exception):
    """Indicates the configuration format was invalid or couldn't be read."""

  class KeyAlreadyDeclaredError(Exception):
    """Indicates that a configuration key was already declared."""

  class UndeclaredKeyError(Exception):
    """Indicates that a key was required but not predeclared."""

  class InvalidKeyError(Exception):
    """Raised when an invalid key is declared or accessed."""

  class UnsetKeyError(Exception):
    """Raised when a key value is requested but we have no value for it."""

  # pylint: disable=invalid-name,bad-super-call,too-few-public-methods
  class Declaration(mutablerecords.Record(
      'Declaration', ['name'], {
          'description': None, 'default_value': None, 'has_default': False})):
    """Record type encapsulating information about a config declaration."""
    def __init__(self, *args, **kwargs):
      super(type(self), self).__init__(*args, **kwargs)
      # Track this separately to allow for None as a default value, override
      # any value that was passed in explicitly - don't do that.
      self.has_default = 'default_value' in kwargs
  # pylint: enable=invalid-name,bad-super-call,too-few-public-methods

  __slots__ = ('_logger', '_lock', '_modules', '_declarations',
               '_flag_values', '_flags', '_loaded_values', 'ARG_PARSER')

  def __init__(self, logger, lock, parser, **kwargs):
    """Initializes the configuration state.

    We have to pull everything we need from global scope into here because we
    will be swapping out the module with this instance and will lose any global
    references.

    Args:
      logger: Logger to use for logging messages within this class.
      lock: Threading.Lock to use for locking access to config values.
      **kwargs: Modules we need to access within this class.
    """
    self._logger = logger
    self._lock = lock
    self._modules = kwargs
    self._declarations = {}
    self.ARG_PARSER = parser

    # Parse just the flags we care about, since this happens at import time.
    self._flags, _ = parser.parse_known_args()

    # Populate flag_values from flags now.
    self._flag_values = {}
    for keyval in self._flags.config_value:
      self._flag_values.setdefault(*keyval.split('=', 1))

    # Initialize self._loaded_values and load from --config-file if it's set.
    self.Reset()

  @staticmethod
  def _IsValidKey(key):
    """Return True if key is a valid configuration key."""
    return key and key[0].islower()

  def __setattr__(self, attr, value):
    """Provide a useful error when attempting to set a value via setattr()."""
    if self._IsValidKey(attr):
      raise AttributeError("Can't set conf values by attribute, use Load()")
    # __slots__ is defined above, so this will raise an AttributeError if the
    # attribute isn't one we expect; this limits the number of ways to abuse the
    # conf module singleton instance.  Also note that we can't use super()
    # normally here because of the sys.modules swap (Configuration is no longer
    # defined, and evaluates to None if used here).
    # pylint: disable=bad-super-call
    super(type(self), self).__setattr__(attr, value)

  # Don't use Synchronized on this one, because __getitem__ handles it.
  def __getattr__(self, attr):  # pylint: disable=invalid-name
    """Get a config value via attribute access."""
    if self._IsValidKey(attr):
      return self[attr]
    # Config keys all begin with a lowercase letter, so treat this normally.
    raise AttributeError("'%s' object has no attribute '%s'" %
                         (type(self).__name__, attr))

  @threads.Synchronized
  def __getitem__(self, item):  # pylint: disable=invalid-name
    """Get a config value via item access.

    Order of precedence is:
      - Value provided via --config-value flag.
      - Value loaded via Load*() methods.
      - Default value as declared with conf.Declare()

    Args:
      item: Config key name to get.
    """
    if item not in self._declarations:
      raise self.UndeclaredKeyError('Configuration key not declared', item)

    if item in self._flag_values:
      if item in self._loaded_values:
        self._logger.warning(
            'Overriding loaded value for %s (%s) with flag value: %s',
            item, self._loaded_values[item], self._flag_values[item])
      return self._flag_values[item]
    if item in self._loaded_values:
      return self._loaded_values[item]
    if self._declarations[item].has_default:
      return self._declarations[item].default_value

    raise self.UnsetKeyError(
        'Configuration value not set and has no default', item)

  @threads.Synchronized
  def __contains__(self, name):  # pylint: disable=invalid-name
    """True if we have a value for name."""
    return (name in self._declarations and
            (self._declarations[name].has_default or
             name in self._loaded_values or
             name in self._flag_values))

  @threads.Synchronized
  def Declare(self, name, description=None, **kwargs):
    """Declare a configuration key with the given name.

    Args:
      name: Configuration key to declare, must not have been already declared.
      description: If provided, use this as the description for this key.
      **kwargs: Other kwargs to pass to the Declaration, only default_value
          is currently supported.
    """
    if not self._IsValidKey(name):
      raise self.InvalidKeyError(
          'Invalid key name, must begin with a lowercase letter', name)
    if name in self._declarations:
      raise self.KeyAlreadyDeclaredError(
          'Configuration key already declared', name)
    self._declarations[name] = self.Declaration(
        name, description=description, **kwargs)

  @threads.Synchronized
  def Reset(self):
    """Reset the loaded state of the configuration to what it was at import.

    Note that this does *not* reset values set by commandline flags or loaded
    from --config-file (in fact, any values loaded from --config-file that have
    been overridden are reset to their value from --config-file).
    """
    # Populate loaded_values with values from --config-file, if it was given.
    self._loaded_values = {}
    if self._flags.config_file is not None:
      self.LoadFromFile(self._flags.config_file, _allow_undeclared=True)

  def LoadFromFile(self, yamlfile, _override=True, _allow_undeclared=False):
    """Loads the configuration from a file.

    Parsed contents must be a single dict mapping config key to value.

    Args:
      yamlfile: The opened file object to load configuration from.
      See LoadFromDict() for other args' descriptions.

    Raises:
      ConfigurationInvalidError: If configuration file can't be read, or can't
          be parsed as either YAML (or JSON, which is a subset of YAML).
    """
    self._logger.info('Loading configuration from file: %s', yamlfile)

    try:
      parsed_yaml = self._modules['yaml'].safe_load(yamlfile.read())
    except self._modules['yaml'].YAMLError as exception:
      raise self.ConfigurationInvalidError(
          'Failed to load from %s as YAML' % yamlfile, exception)

    if not isinstance(parsed_yaml, dict):
      # Parsed YAML, but it's not a dict.
      raise self.ConfigurationInvalidError(
          'YAML parsed, but wrong type, should be dict', parsed_yaml)

    self._logger.debug('Configuration loaded from file: %s', parsed_yaml)
    self.LoadFromDict(
        parsed_yaml, _override=_override, _allow_undeclared=_allow_undeclared)

  def Load(self, _override=True, _allow_undeclared=False, **kwargs):
    """Load configuration values from kwargs, see LoadFromDict()."""
    self.LoadFromDict(
        kwargs, _override=_override, _allow_undeclared=_allow_undeclared)

  @threads.Synchronized
  def LoadFromDict(self, dictionary, _override=True, _allow_undeclared=False):
    """Loads the config with values from a dictionary instead of a file.

    This is meant for testing and bin purposes and shouldn't be used in most
    applications.

    Args:
      dictionary: The dictionary containing config keys/values to update.
      _override: If True, new values will override previous values.
      _allow_undeclared: If True, silently load undeclared keys, otherwise
          warn and ignore the value.  Typically used for loading config
          files before declarations have been evaluated.
    """
    undeclared_keys = []
    for key, value in dictionary.iteritems():
      # Warn in this case.  We raise if you try to access a config key that
      # hasn't been declared, but we don't raise here so that you can use
      # configuration files that are supersets of required configuration for
      # any particular test station.
      if key not in self._declarations and not _allow_undeclared:
        undeclared_keys.append(key)
        continue
      if key in self._loaded_values:
        if _override:
          self._logger.info(
              'Overriding previously loaded value for %s (%s) with value: %s',
              key, self._loaded_values[key], value)
        else:
          self._logger.info(
              'Ignoring new value (%s), keeping previous value for %s: %s',
              value, key, self._loaded_values[key])
          continue
      self._loaded_values[key] = value
    if undeclared_keys:
      self._logger.warning('Ignoring undeclared configuration keys: %s',
                           undeclared_keys)

  @threads.Synchronized
  def _asdict(self):
    """Create a dictionary snapshot of the current config values."""
    # Start with any default values we have, and override with loaded values,
    # and then override with flag values.
    retval = {key: self._declarations[key].default_value for
              key in self._declarations if self._declarations[key].has_default}
    retval.update(self._loaded_values)
    # Only update keys that are declared so we don't allow injecting
    # un-declared keys via commandline flags.
    for key, value in self._flag_values.iteritems():
      if key in self._declarations:
        retval[key] = value
    return retval

  def InjectPositionalArgs(self, method):
    """Decorator for injecting positional arguments from the configuration.

    This decorator wraps the given method, so that any positional arguments are
    passed with corresponding values from the configuration.  The name of the
    positional argument must match the configuration key.

    Keyword arguments are *NEVER* modified, even if their names match
    configuration keys.  Avoid naming keyword args names that are also
    configuration keys to avoid confusion.

    Additional positional arguments may be used that do not appear in the
    configuration, but those arguments *MUST* be specified as keyword arguments
    upon invokation of the method.  This is to avoid ambiguity in which
    positional arguments are getting which values.

    Args:
      method: The method to wrap.

    Returns:
      A wrapper that, when invoked, will call the wrapped method, passing in
    configuration values for positional arguments.
    """
    argspec = self._modules['inspect'].getargspec(method)

    # Index in argspec.args of the first keyword argument.  This index is a
    # negative number if there are any kwargs, or 0 if there are no kwargs.
    keyword_arg_index = -1 * len(argspec.defaults or [])
    arg_names = argspec.args[:keyword_arg_index or None]
    kwarg_names = argspec.args[len(arg_names):]
    functools = self._modules['functools']

    # Create the actual method wrapper, all we do is update kwargs.  Note we
    # don't pass any *args through because there can't be any - we've filled
    # them all in with values from the configuration.  Any positional args that
    # are missing from the configuration *must* be explicitly specified as
    # kwargs.
    @functools.wraps(method)
    def method_wrapper(**kwargs):
      """Wrapper that pulls values from openhtf.conf."""
      # Check for keyword args with names that are in the config so we can warn.
      for kwarg in kwarg_names:
        if kwarg in self:
          self._logger.warning('Keyword arg %s not set from configuration, but '
                               'is a configuration key', kwarg)

      # Set positional args from configuration values.
      final_kwargs = {name: self[name] for name in arg_names if name in self}

      for overridden in set(kwargs) & set(final_kwargs):
        self._logger.warning('Overriding configuration value for kwarg %s (%s) '
                             'with provided kwarg value: %s', overridden,
                             self[overridden], kwargs[overridden])

      final_kwargs.update(kwargs)
      self._logger.debug('Invoking %s with %s', method.__name__, final_kwargs)
      return method(**final_kwargs)

    # We have to check for a 'self' parameter explicitly because Python doesn't
    # pass it as a keyword arg, it passes it as the first positional arg.
    if argspec.args[0] == 'self':
      @functools.wraps(method)
      def SelfWrapper(self, **kwargs):  # pylint: disable=invalid-name
        """Wrapper that pulls values from openhtf.conf."""
        kwargs['self'] = self
        return method_wrapper(**kwargs)
      return SelfWrapper
    return method_wrapper

# Swap out the module for a singleton instance of Configuration so we can
# provide __getattr__ and __getitem__ functionality at the module level.
sys.modules[__name__] = Configuration(
    logging.getLogger(__name__), threading.RLock(), ARG_PARSER,
    functools=functools, inspect=inspect, yaml=yaml)
