#!/usr/bin/env python

# brizzy - just a pore PhD student's plotting package
# Copyright (c) 2016-2017 Darrin T. Schultz. All rights reserved.
#
# This file is part of brizzy.
#
# brizzy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# brizzy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with brizzy.  If not, see <http://www.gnu.org/licenses/>.

# I took this code from https://github.com/arq5x/poretools/. Check it out. - DTS

import sys
import os.path
import argparse

import brizzy.version
# This class is used in argparse to expand the ~. This avoids errors caused on
# some systems.


class FullPaths(argparse.Action):
    """Expand user- and relative-paths"""

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest,
                os.path.abspath(os.path.expanduser(values)))

class FullPathsList(argparse.Action):
    """Expand user- and relative-paths when a list of paths is passed to the
    program"""

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest,
                [os.path.abspath(os.path.expanduser(value)) for value in values])


def run_subtool(parser, args):
    if args.command == 'capture':
        import brizzy.capture as submodule
    # run the chosen submodule.
    submodule.run(args)

class ArgumentParserWithDefaults(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(ArgumentParserWithDefaults, self).__init__(*args, **kwargs)
        self.add_argument("-q", "--quiet", help="Do not output warnings to stderr",
                          action="store_true",
                          dest="QUIET")

def main():

    #########################################
    # create the top-level parser
    #########################################
    parser = argparse.ArgumentParser(
        prog='brizzy', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-v", "--version", help="Installed brizzy version",
                        action="version",
                        version="%(prog)s " + str(brizzy.version.__version__))
    subparsers = parser.add_subparsers(
        title='[sub-commands]', dest='command', parser_class=ArgumentParserWithDefaults)

    #########################################
    # create the individual tool parsers
    #########################################

    #############
    # capture
    #############
    parser_capture = subparsers.add_parser('capture',
                                          help='easily capture a spectrum, save, plot.')
    parser_capture.add_argument("-d", "--directory",
                        action = FullPaths,
                        help="""The directory in which to save the spectra text
                        files and plots. If you don't specify it just saves
                        everything in the current directory.""")
    parser_capture.add_argument("-p", "--prefix",
                        help="""The prefix name for the spectra plots and text
                        files. If you don't specify, it just saves everything as
                        'spectrum'.""")
    parser_capture.add_argument("-i", "--integration_time",
                        required = True,
                        type = int,
                        help="""The integration time in milliseconds to take a
                        spectrum. This is required.""")
    parser_capture.add_argument("-m", "--monitor",
                        action = "store_true",
                        help="""The integration time in milliseconds to take a
                        spectrum. This is required.""")
    parser_capture.set_defaults(func=run_subtool)

    #######################################################
    # parse the args and call the selected function
    #######################################################

    args = parser.parse_args()

    # If there were no args, print the help function
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # If there were no args, but someone selected a program,
    #  print the program's help.
    commandDict = {'capture': parser_capture.print_help}

    if len(sys.argv) == 2:
        commandDict[args.command]()
        sys.exit(1)

    if args.QUIET:
        logger.setLevel(logging.ERROR)

    try:
        args.func(parser, args)
    except IOError as e:
        if e.errno != 32:  # ignore SIGPIPE
            raise

if __name__ == "__main__":
    main()
