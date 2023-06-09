import os, sys
import yaml
import logging
import click
import copy
from .settings import ACTION_DEFAULTS, CONFIG_FILE, CLIENT_DEFAULTS, \
    LOGGING_DEFAULTS, OPTION_DEFAULTS
from .exceptions import *
from .utils import *
from .indexlist import IndexList
from .snapshotlist import SnapshotList
from .actions import *
from ._version import __version__
from .logtools import LogInfo

try:
    from logging import NullHandler
except ImportError:
    from logging import Handler

    class NullHandler(Handler):
        def emit(self, record):
            pass

CLASS_MAP = {
    'alias' :  Alias,
    'allocation' : Allocation,
    'close' : Close,
    'create_index' : CreateIndex,
    'delete_indices' : DeleteIndices,
    'delete_snapshots' : DeleteSnapshots,
    'forcemerge' : ForceMerge,
    'open' : Open,
    'replicas' : Replicas,
    'snapshot' : Snapshot,
}

def process_action(client, config, **kwargs):
    """
    Do the `action` in the configuration dictionary, using the associated args.
    Other necessary args may be passed as keyword arguments

    :arg config: An `action` dictionary.
    """
    logger = logging.getLogger(__name__)
    # Make some placeholder variables here for readability
    logger.debug('Configuration dictionary: {0}'.format(config))
    logger.debug('kwargs: {0}'.format(kwargs))
    action = config['action']
    opts = config['options'] if 'options' in config else {}
    logger.debug('opts: {0}'.format(opts))
    mykwargs = {}

    if action in CLASS_MAP:
        if action == 'delete_indices':
            mykwargs['master_timeout'] = (
                kwargs['master_timeout'] if 'master_timeout' in kwargs else 30)
        # deepcopy guarantees clean copies of the defaults, and nothing getting
        # altered in "pass by reference," which was happening in testing.
        mykwargs = copy.deepcopy(ACTION_DEFAULTS[action])
        logger.debug('MYKWARGS = {0}'.format(mykwargs))
        action_class = CLASS_MAP[action]
    else:
        raise ConfigurationError(
            'Unrecognized action: {0}'.format(action))

    ### Update the defaults with whatever came with opts, minus any Nones
    mykwargs.update(prune_nones(opts))
    logger.debug('Action kwargs: {0}'.format(mykwargs))
    # Verify the args we're going to pass match the action
    verify_args(action, mykwargs)

    ### Set up the action ###
    if action == 'alias':
        # Special behavior for this action, as it has 2 index lists
        logger.debug('Running "{0}" action'.format(action.upper()))
        action_obj = action_class(**mykwargs)
        if 'add' in config:
            logger.debug('Adding indices to alias "{0}"'.format(opts['name']))
            adds = IndexList(client)
            adds.iterate_filters(config['add'])
            action_obj.add(adds)
        if 'remove' in config:
            logger.debug(
                'Removing indices from alias "{0}"'.format(opts['name']))
            removes = IndexList(client)
            removes.iterate_filters(config['remove'])
            action_obj.remove(removes)
    elif action == 'create_index':
        action_obj = action_class(client, **mykwargs)
    elif action == 'delete_snapshots':
        logger.debug('Running "delete_snapshots"')
        slo = SnapshotList(client, repository=opts['repository'])
        slo.iterate_filters(config)
        # We don't need to send this value to the action
        mykwargs.pop('repository')
        action_obj = action_class(slo, **mykwargs)
    else:
        logger.debug('Running "{0}"'.format(action.upper()))
        ilo = IndexList(client)
        ilo.iterate_filters(config)
        action_obj = action_class(ilo, **mykwargs)
    ### Do the action
    if 'dry_run' in kwargs and kwargs['dry_run'] == True:
        action_obj.do_dry_run()
    else:
        logger.debug('Doing the action here.')
        action_obj.do_action()

@click.command()
@click.option('--config',
    help="Path to configuration file. Default: ~/.curator/curator.yml",
    type=click.Path(exists=True), default=CONFIG_FILE
)
@click.option('--dry-run', is_flag=True, help='Do not perform any changes.')
@click.argument('action_file', type=click.Path(exists=True), nargs=1)
@click.version_option(version=__version__)
def cli(config, dry_run, action_file):
    """
    Curator for Elasticsearch indices.

    See http://elastic.co/guide/en/elasticsearch/client/curator/current
    """
    # Get config from yaml file
    yaml_config  = get_yaml(config)
    # Get default options and overwrite with any changes
    try:
        yaml_log_opts = prune_nones(yaml_config['logging'])
        log_opts      = LOGGING_DEFAULTS
        log_opts.update(yaml_log_opts)
    except KeyError:
        # Use the defaults if there is no logging section
        log_opts = LOGGING_DEFAULTS
    # Set up logging
    loginfo = LogInfo(log_opts)
    logging.root.addHandler(loginfo.handler)
    logging.root.setLevel(loginfo.numeric_log_level)
    logger = logging.getLogger('curator.cli')
    # Set up NullHandler() to handle nested elasticsearch.trace Logger
    # instance in elasticsearch python client
    logging.getLogger('elasticsearch.trace').addHandler(NullHandler())

    # Get default client options and overwrite with any changes
    try:
        yaml_client  = prune_nones(yaml_config['client'])
        client_args  = CLIENT_DEFAULTS
        client_args.update(yaml_client)
    except KeyError:
        logger.critical(
            'Unable to read client configuration. '
            'Please check the configuration file: {0}'.format(config)
        )
        sys.exit(1)
    test_client_options(client_args)

    # Create a client object
    client = get_client(**client_args)
    #########################################
    ### Start working on the actions here ###
    #########################################
    actions = get_yaml(action_file)['actions']
    logger.debug('Full list of actions: {0}'.format(actions))
    action_keys = sorted(list(actions.keys()))
    for idx in action_keys:
        if 'action' in actions[idx] and actions[idx]['action'] is not None:
            action = actions[idx]['action'].lower()
        else:
            raise MissingArgument('No value for "action" provided')
        logger.info('Action #{0}: {1}'.format(idx, action))
        if not 'options' in actions[idx] or \
                type(actions[idx]['options']) is not type(dict()):
            actions[idx]['options'] = OPTION_DEFAULTS
        # Assign and remove these keys from the options as the action will
        # raise an exception if they are passed as kwargs
        action_disabled = actions[idx]['options'].pop('disable_action', False)
        continue_if_exception = (
            actions[idx]['options'].pop('continue_if_exception', False))
        logger.debug(
            'continue_if_exception = {0}'.format(continue_if_exception))
        kwargs = {}
        kwargs['master_timeout'] = (
            client_args['timeout'] if client_args['timeout'] <= 300 else 300)
        kwargs['dry_run'] = dry_run

        ### Skip to next action if 'disabled'
        if action_disabled:
            logger.info(
                'Action "{0}" not performed because "disable_action" is set to '
                'True'.format(action)
            )
            continue
        ##########################
        ### Process the action ###
        ##########################
        try:
            logger.debug('TRY: actions: {0} kwargs: '
                '{1}'.format(actions[idx], kwargs)
            )
            process_action(client, actions[idx], **kwargs)
        except Exception as e:
            logger.error(
                'Failed to complete action: {0}.  {1}: '
                '{2}'.format(action, type(e), e)
            )
            if continue_if_exception:
                logger.info(
                    'Continuing execution with next action because '
                    '"continue_if_exception" is set to True for action '
                    '{0}'.format(action)
                )
            else:
                sys.exit(1)
