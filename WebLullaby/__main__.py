#!/usr/bin/env python3

import os
import sys
import logging
import argparse

from . import config
from .screensaver import run


def main():
    """
    :rtype: int
    """
    options = __parse_args()

    if options.debug:
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(name)s %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    return run(options.screensaver_url)


def __parse_args():
    """
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(prog=config.APP_NAME, description=config.APP_DESCRIPTION,
                                     formatter_class=_WideHelpFormatter)

    parser.add_argument('screensaver_url', action='store', nargs='?',
                        default='https://goo.gl/sJembB',
                        help='URL of the screensaver (default: %(default)s)')
    parser.add_argument('background_command', action='store', nargs='?',
                        help='URL of the screensaver (default: %(default)s)')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Show debug logs')

    parsed_args, _ = parser.parse_known_args()

    return parsed_args


class _WideHelpFormatter(argparse.RawDescriptionHelpFormatter):
    def __init__(self, prog, *args, **kwargs):
        indent_increment = 2
        max_help_position = 40
        width = int(os.getenv("COLUMNS", 120)) - 2

        super(_WideHelpFormatter, self).__init__(prog, indent_increment, max_help_position, width)


if __name__ == '__main__':
    sys.exit(main())
