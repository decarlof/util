#!/local/decarlo/conda/anaconda/bin/python

import os
import sys
import argparse
import logging
import time
import re
import config as config


LOG = logging.getLogger('dquality')


def init(args):
    if not os.path.exists(args.config):
        config.write(args.config)
    else:
        raise RuntimeError("{0} already exists".format(args.config))

def update(args):
    try:
        a = 1
        config.write(args.config)
        print("update")
        #gui.main(args)
    except ImportError as e:
        LOG.error(str(e))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', **config.SECTIONS['general']['config'])

    sino_params = ('consumer', 'data-tags')
    reco_params = ('dependencies', 'pvs')
    tomo_params = config.ALL_PARAMS
    gui_params = tomo_params

    print(tomo_params)
    
    cmd_parsers = [
        ('init',    init,   tomo_params,    "Create configuration file"),
        ('update',  update, tomo_params,    "Update configuration file"),
    ]

    subparsers = parser.add_subparsers(title="Commands", metavar='')

    for cmd, func, sections, text in cmd_parsers:
        cmd_params = config.Params(sections=sections)
        cmd_parser = subparsers.add_parser(cmd, help=text, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        cmd_parser = cmd_params.add_arguments(cmd_parser)
        cmd_parser.set_defaults(_func=func)

    args = config.parse_known_args(parser, subparser=True)

    log_level = logging.DEBUG if args.verbose else logging.INFO
    LOG.setLevel(log_level)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    LOG.addHandler(stream_handler)

    if args.log:
        file_handler = logging.FileHandler(args.log)
        file_handler.setFormatter(logging.Formatter('%(name)s:%(levelname)s: %(message)s'))
        LOG.addHandler(file_handler)

    try:
        config.log_values(args)
        args._func(args)
    except RuntimeError as e:
        LOG.error(str(e))
        sys.exit(1)


if __name__ == '__main__':
    main()

# vim: ft=python
