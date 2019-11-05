#
# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2019-10-06 16:32:08 alex>
#

"""
cli menu connect
"""

from __future__ import unicode_literals, print_function

import time

from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit import print_formatted_text
from prompt_toolkit.shortcuts import ProgressBar

from default import handle_global_command, get_value
from default import get_bool_value
from default import get_bottom_toolbar
from default import get_lexer

from SOLIDserverRest.Exception import SDSError


# ----------------------------------
def do_help():
    """local help command for connect"""
    print("connect menu")
    print_formatted_text(HTML(" <i>connect</i>: connect to SOLIDserver"))
    print_formatted_text(HTML(" <i>disconnect</i>:"
                              + " disconnect from SOLIDserver"))
    print_formatted_text(HTML(" <i>q</i>, <i>..</i>: menu up"))
    print_formatted_text(' parameters:')
    print_formatted_text(HTML('  <b>host</b> ipv4|ipv6|fqdn'))
    print_formatted_text(HTML('  <b>user</b> api user name'))
    print_formatted_text(HTML('  <b>password</b>'
                              + ' api user associated password'))
    print_formatted_text(HTML('  <b>ssl</b> true|false check certificate'))


# ----------------------------------
def local_header(connect_vars):
    """build the local header for the connect prompt"""
    header_str = '<b>connect</b>'
    header_str += " <skyblue>host</skyblue>:"
    if connect_vars['host'] == "":
        header_str += "<ansired>unset</ansired>"
    else:
        header_str += "<ansigreen>{}</ansigreen>".format(connect_vars['host'])

    header_str += " <skyblue>user</skyblue>:"
    if connect_vars['user'] == "":
        header_str += "<ansired>ukn</ansired>"
    else:
        header_str += "<ansigreen>{}</ansigreen>".format(connect_vars['user'])

    header_str += " <skyblue>password</skyblue>:"
    if connect_vars['password'] == "":
        header_str += "<ansired>ukn</ansired>"
    else:
        header_str += "<ansigreen>***</ansigreen>"

    header_str += " <skyblue>ssl</skyblue>:"
    if connect_vars['ssl']:
        header_str += "<ansigreen>check</ansigreen>"
    else:
        header_str += "<orange>no check</orange>"

    if connect_vars['do']:
        header_str += " <b><seagreen>[do]</seagreen></b>"

    return header_str


# ----------------------------------
def do_connect_iter(sds, connect_vars):
    """connect to SDS iterable"""

    yield 1
    sds['cnx'].set_server_ip(connect_vars['host'])
    sds['cnx'].set_credentials(user=connect_vars['user'],
                               pwd=connect_vars['password'])

    cert_file = None
    if connect_vars['ssl']:
        cert_file = 'ca.crt'

    yield 1
    try:
        sds['cnx'].connect(method="basicauth",
                           cert_file_path=cert_file,
                           timeout=3)
    except SDSError:
        print("connection error")
        return False

    yield 1
    sds['version'] = sds['cnx'].get_version()
    sds['connected'] = True

    yield 1
    return True


# ----------------------------------
def do_disconnect(sds, connect_vars):
    """disconnect to SDS"""
    print("disconnecting...")

    try:
        sds['cnx'].disconnect()
    except SDSError:
        print("disconnection error")
        return False

    sds['version'] = None
    sds['connected'] = False
    sds['space'] = None

    connect_vars['do'] = False

    return True


# ----------------------------------
def parse_local_command(user_input, connect_vars):
    """parse local parameters when not standard command"""
    shl = get_lexer(user_input)

    while True:
        arg = shl.get_token()
        if arg is None:
            break

        if arg == "host":
            value = connect_vars['host'] = get_value(shl)

        elif arg == "user":
            value = connect_vars['user'] = get_value(shl)

        elif arg == "password":
            value = connect_vars['password'] = get_value(shl)

        elif arg == "ssl":
            value = get_bool_value(shl, connect_vars['ssl'])
            connect_vars['ssl'] = value

        else:
            print("unknown parameter")
            continue

# ----------------------------------
def general_handle_connect(user_input, sds, connect_vars):
    """general menu option handling"""
    if handle_global_command(user_input, sds):
        return

    if user_input == '?':
        do_help()
        return

    parse_local_command(user_input, connect_vars)

# ----------------------------------
def menu_connect(cli_session, sds, header_str):
    """specific function connect"""
    connect_vars = {
        'host': "192.168.56.254",
        'user': "ipmadmin",
        'password': "admin",
        'ssl': False,
        'do': False,
    }

    completer_dis = WordCompleter(['connect',
                                   'host', 'login', 'password', 'ssl',
                                   '?', 'exit',
                                   'true', 'false'],
                                  ignore_case=True)

    completer_con = WordCompleter(['disconnect',
                                   '?', 'exit'],
                                  ignore_case=True)

    if header_str is not None:
        header_str += '\n'
    else:
        header_str = ''

    while 1:
        # check doable
        var_do = bool(connect_vars['host'] != "" and
                      connect_vars['user'] != "" and
                      connect_vars['password'] != "")

        print_formatted_text(HTML(header_str
                                  + local_header(connect_vars)))

        if sds['connected']:
            local_comp = completer_con
        else:
            local_comp = completer_dis

        user_input = cli_session.prompt('top/connect>',
                                        auto_suggest=AutoSuggestFromHistory(),
                                        completer=local_comp,
                                        bottom_toolbar=get_bottom_toolbar(sds))

        if user_input in ('..', 'q'):
            break

        if user_input == 'connect':
            if var_do:
                iterat = do_connect_iter(sds, connect_vars)
                with ProgressBar() as progressbar:
                    for _ in progressbar(iterat, total=4):
                        time.sleep(0.01)
                break
            else:
                print_formatted_text(HTML("<red>cannot do connection,"
                                          + "missing parameter</red>"))
            continue

        elif user_input == 'disconnect' and sds['connected']:
            do_disconnect(sds, connect_vars)
            break

        general_handle_connect(user_input, sds, connect_vars)
