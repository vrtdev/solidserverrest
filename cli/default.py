#
# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2019-10-06 16:31:03 alex>
#

"""
cli default functions
"""

import sys
import os
import datetime
import time
import shlex

from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import HTML

sys.path.append(os.getcwd())

from SOLIDserverRest.Exception import SDSEmptyError


def handle_global_command(user_input, sds):
    """ all global commands are here """
    if user_input == 'exit':
        exit()

    if user_input == 'version':
        if not sds['connected']:
            print_formatted_text(HTML('<red>not connected</red>'))
            return False

        try:
            version = sds['cnx'].get_version()
            msg = 'SOLIDserver version <green>{}</green>'.format(version)
            print_formatted_text(HTML(msg))
            return True
        except SDSEmptyError:
            print_formatted_text(HTML('<red>get version error</red>'))

    return False


def get_value(shl):
    """get the next token as a value"""
    value = shl.get_token()
    if value == "=":
        return get_value(shl)
    if value is None:
        value = ""
    return value


def get_bool_value(shl, old=None):
    """get the next token as a boolean value"""
    value = shl.get_token()

    if value is None:
        if old is not None:
            return not old
        return False
    if value == "true":
        return True
    if value == "false":
        return False

    return False


def get_cli_version():
    """return the version of this cli module"""
    return 'v0.1'


def get_bottom_toolbar(sds):
    """return the content of the botom toolbar for prompt"""
    msg = '<b>SDS</b> CLI '+get_cli_version()

    msg += ' {:%H:%M}'.format(datetime.datetime.now())

    if sds['connected']:
        msg += ' <i><green>connected</green></i>'
        msg += ' {}'.format(sds['version'])

        if time.time() > sds['load_stats_time']:
            sds['load_stats'] = sds['cnx'].get_load()
            sds['load_stats_time'] = time.time() + 30

        msg += ' [<u>cpu</u>:{:.1f}'.format(sds['load_stats']['cpu'])
        msg += ' <u>io</u>:{:d}%'.format(sds['load_stats']['ioload'])
        msg += ' <u>mem</u>:{:d}%'.format(sds['load_stats']['mem'])
        msg += ' <u>hdd</u>:{:d}%]'.format(sds['load_stats']['hdd'])

        if sds['space'] is not None:
            msg += ' <b>space</b>: {}'.format(sds['space'].params['site_name'])

    return HTML(msg)


def get_lexer(user_input):
    """build the lexer for input analysis"""
    shl = shlex.shlex(user_input, posix=True)
    shl.wordchars += ":."
    shl.whitespace += "=,"
    return shl
