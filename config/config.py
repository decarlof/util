import argparse
import sys
import logging
import ConfigParser as configparser
from collections import OrderedDict
import numpy as np

LOG = logging.getLogger(__name__)
NAME = "dquality.conf"

SECTIONS = OrderedDict()

SECTIONS['general'] = {
    'config': {
        'default': NAME,
        'type': str,
        'help': "File name of configuration",
        'metavar': 'FILE'},
    'verbose': {
        'default': False,
        'help': 'Verbose output',
        'action': 'store_true'},
    'log': {
        'default': None,
        'type': str,
        'help': "File name of optional log",
        'metavar': 'FILE'}}

SECTIONS['consumer'] = {
    'ttverbose': {
        'default': False,
        'help': 'Verbose output',
        'action': 'store_true'},
    'ttlog': {
        'default': None,
        'type': str,
        'help': "File name of optional log",
        'metavar': 'FILE'}}
 
SECTIONS['data-tags'] = {
    'data': {
        'default': "/exchange/data",
        'type': str,
        'help': "projection data hdf tag"},
    'data_dark': {
        'default': "/exchange/data_dark",
        'type': str,
        'help': "dark images hdf tag"},
    'data_white': {
        'default': "/exchange/data_white",
        'type': str,
        'help': "white images hdf tag"},
}

SECTIONS['dependencies'] = {
    'retrieval-method': {
        'choices': ['default'],
        'default': 'default',
        'help': "Phase retrieval method"},
    'energy': {
        'default': None,
        'type': float,
        'help': "X-ray energy [keV]"},
    'propagation-distance': {
        'default': None,
        'type': float,
        'help': "Sample <-> detector distance [m]"},
    'pixel-size': {
        'default': None,
        'type': float,
        'help': "Pixel size [m]"},
    'alpha': {
        'default': 0,
        'type': float,
        'help': "Regularization parameter"},
    'pad': {
        'default': True,
        'help': "Extend the size of the projections by padding with zeros."},
    'ncore': {
        'default': None,
        'help': "Number of cores that will be assigned to jobs"},
    'nchunk': {
        'default': None,
        'help': "Chunk size for each core"}}

SECTIONS['limits'] = {
    'data_mean_low_limit': {
        'type': float,
        'default': 400,
        'help': "data mean value min"},
    'data_mean_high_limit': {
        'type': float,
        'default': 600,
        'help': "data mean value max"}, 
    'data_stat_mean_low_limit': {
        'type': float,
        'default': -150,
        'help': "data stat mean value min"}, 
    'data_stat_mean_high_limit': {
        'type': float,
        'default': 150,
        'help': "data stat mean value max"}, 
    'data_std_low_limit': {
        'type': float,
        'default': 150,
        'help': "data std min"}, 
    'data_std_high_limit': {
        'type': float,
        'default': 200,
        'help': "data std max"},
    'data_dark_mean_low_limit': {
        'type': float,
        'default': 0,
        'help': "dark mean value min"},
    'data_dark_mean_high_limit': {
        'type': float,
        'default': 110,
        'help': "dark mean value max"}, 
    'data_dark_stat_mean_low_limit': {
        'type': float,
        'default': -5,
        'help': "stat mean value min"}, 
    'data_dark_stat_mean_high_limit': {
        'type': float,
        'default': 5,
        'help': "dark stat mean value max"}, 
    'data_dark_std_low_limit': {
        'type': float,
        'default': 1.5,
        'help': "dark std min"}, 
    'data_dark_std_high_limit': {
        'type': float,
        'default': 10,
        'help': "dark std max"},        
    'data_white_mean_low_limit': {
        'type': float,
        'default': 650,
        'help': "white mean value min"},
    'data_white_mean_high_limit': {
        'type': float,
        'default': 900,
        'help': "white mean value max"}, 
    'data_white_stat_mean_low_limit': {
        'type': float,
        'default': -150,
        'help': "white stat mean value min"}, 
    'data_white_stat_mean_high_limit': {
        'type': float,
        'default': 150,
        'help': "white stat mean value max"}, 
    'data_white_std_low_limit': {
        'type': float,
        'default': 100,
        'help': "white std min"}, 
    'data_white_std_high_limit': {
        'type': float,
        'default': 260,
        'help': "white std max"}}

SECTIONS['pvs'] = {
    'slice-start': {
        'type': int,
        'default': 0,
        'help': "Start slice to read for reconstruction"},
    'slice-end': {
        'type': int,
        'default': 1,
        'help': "End slice to read for reconstruction"},
    'theta_start': {
        'default': 0,
        'type': float,
        'help': "Angle step between projections in radians"},
    'theta_end': {
        'default': np.pi,
        'type': float,
        'help': "Angle step between projections in radians"},
    'last-file': {
        'default': '.',
        'type': str,
        'help': "Name of the last file used",
        'metavar': 'PATH'},
    'output-dir': {
        'default': '.',
        'type': str,
        'help': "Path to location or format-specified file path "
                "for storing reconstructed slices",
        'metavar': 'PATH'}}

SECTIONS['quality-checks'] = {
    'binning': {
        'type': str,
        'default': '0',
        'help': "Reconstruction binning factor as power(2, choice)",
        'choices': ['0', '1', '2', '3']},
    'filter': {
        'default': 'none',
        'type': str,
        'help': "Reconstruction filter",
        'choices': ['none', 'shepp', 'cosine', 'hann', 'hamming', 'ramlak', 'parzen', 'butterworth']},
    'axis': {
        'default': 1024,
        'type': float,
        'help': "Rotation axis position"},
    'dry-run': {
        'default': False,
        'help': "Reconstruct without writing data",
        'action': 'store_true'},
    'full-reconstruction': {
        'default': False,
        'help': "Full or one slice only reconstruction",
        'action': 'store_true'},
    'method': {
        'default': 'gridrec',
        'type': str,
        'help': "Reconstruction method",
        'choices': ['gridrec', 'fbp', 'mlem', 'sirt', 'sartfbp']}}

SECTIONS['tags'] = {
    'num-iterations': {
        'default': 10,
        'type': int,
        'help': "Maximum number of iterations"}}

ALL_PARAMS = ('consumer', 'data-tags', 'dependencies', 'limits', 'pvs', 'quality-checks', 'tags')

NICE_NAMES = ('General', 'Input', 'Flat field correction', 'Sinogram generation',
              'General reconstruction', 'Tomographic reconstruction',
              'Filtered backprojection',
              'Direct Fourier Inversion', 'Iterative reconstruction',
              'SART', 'SBTV', 'GUI settings', 'Estimation', 'Performance')

def get_config_name():
    """Get the command line --config option."""
    name = NAME
    for i, arg in enumerate(sys.argv):
        if arg.startswith('--config'):
            if arg == '--config':
                return sys.argv[i + 1]
            else:
                name = sys.argv[i].split('--config')[1]
                if name[0] == '=':
                    name = name[1:]
                return name

    return name


def parse_known_args(parser, subparser=False):
    """
    Parse arguments from file and then override by the ones specified on the
    command line. Use *parser* for parsing and is *subparser* is True take into
    account that there is a value on the command line specifying the subparser.
    """
    if len(sys.argv) > 1:
        subparser_value = [sys.argv[1]] if subparser else []
        config_values = config_to_list(config_name=get_config_name())
        values = subparser_value + config_values + sys.argv[1:]
    else:
        values = ""

    return parser.parse_known_args(values)[0]


def config_to_list(config_name=NAME):
    """
    Read arguments from config file and convert them to a list of keys and
    values as sys.argv does when they are specified on the command line.
    *config_name* is the file name of the config file.
    """
    result = []
    config = configparser.ConfigParser()

    if not config.read([config_name]):
        return []

    for section in SECTIONS:
        for name, opts in ((n, o) for n, o in SECTIONS[section].items() if config.has_option(section, n)):
            value = config.get(section, name)

            if value is not '' and value != 'None':
                action = opts.get('action', None)

                if action == 'store_true' and value == 'True':
                    # Only the key is on the command line for this action
                    result.append('--{}'.format(name))

                if not action == 'store_true':
                    if opts.get('nargs', None) == '+':
                        result.append('--{}'.format(name))
                        result.extend((v.strip() for v in value.split(',')))
                    else:
                        result.append('--{}={}'.format(name, value))

    return result


class Params(object):
    def __init__(self, sections=()):
        self.sections = sections + ('general', )

    def add_parser_args(self, parser):
        for section in self.sections:
            for name in sorted(SECTIONS[section]):
                opts = SECTIONS[section][name]
                parser.add_argument('--{}'.format(name), **opts)

    def add_arguments(self, parser):
        self.add_parser_args(parser)
        return parser

    def get_defaults(self):
        parser = argparse.ArgumentParser()
        self.add_arguments(parser)

        return parser.parse_args('')


def write(config_file, args=None, sections=None):
    """
    Write *config_file* with values from *args* if they are specified,
    otherwise use the defaults. If *sections* are specified, write values from
    *args* only to those sections, use the defaults on the remaining ones.
    """
    config = configparser.ConfigParser()

    for section in SECTIONS:
        config.add_section(section)
        for name, opts in SECTIONS[section].items():
            if args and sections and section in sections and hasattr(args, name.replace('-', '_')):
                value = getattr(args, name.replace('-', '_'))

                if isinstance(value, list):
                    value = ', '.join(value)
            else:
                value = opts['default'] if opts['default'] is not None else ''

            prefix = '# ' if value is '' else ''

            if name != 'config':
                config.set(section, prefix + name, value)

    with open(config_file, 'wb') as f:
        config.write(f)


def log_values(args):
    """Log all values set in the args namespace.

    Arguments are grouped according to their section and logged alphabetically
    using the DEBUG log level thus --verbose is required.
    """
    args = args.__dict__

    for section, name in zip(SECTIONS, NICE_NAMES):
        entries = sorted((k for k in args.keys() if k in SECTIONS[section]))

        if entries:
            LOG.debug(name)

            for entry in entries:
                value = args[entry] if args[entry] is not None else "-"
                LOG.debug("  {:<16} {}".format(entry, value))
