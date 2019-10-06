#
# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2019-10-06 16:31:51 alex>
#

"""
cli menu site / space
"""

from __future__ import unicode_literals, print_function

from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit import print_formatted_text
# from prompt_toolkit.shortcuts import ProgressBar

from default import handle_global_command, get_value
# from default import get_bool_value
from default import get_bottom_toolbar
from default import get_lexer

# from SOLIDserverRest.Exception import SDSError
from SOLIDserverRest.Exception import SDSEmptyError

import SOLIDserverRest.adv as sdsadv


# ----------------------------------
def do_help():
    """local help command for site/space menu"""
    print("space menu")
    print_formatted_text(HTML(" <i>connect</i>: connect to the SOLIDserver"))


# ----------------------------------
def local_header(space_vars):
    """local prompt"""

    header_str = " <skyblue>name</skyblue>:"
    if space_vars['name'] == "":
        header_str += "<ansired>unset</ansired>"
    else:
        header_str += "<ansigreen>{}</ansigreen>".format(space_vars['name'])

    return header_str


# ----------------------------------
def parse_local_command(user_input, space_vars, sds):
    """parse local parameters when not standard command"""
    shl = get_lexer(user_input)

    while True:
        arg = shl.get_token()
        if arg is None:
            break

        if arg == "name":
            value = space_vars['name'] = get_value(shl)
            if value == '':
                sds['space'] = None
                space_vars['name'] = ''
            else:
                sds['space'] = sdsadv.Space(sds=sds['cnx'], name=value)
                try:
                    sds['space'].refresh()
                except SDSEmptyError:
                    sds['space'] = None
                    space_vars['name'] = ''
                    print_formatted_text(HTML("<ansired>"
                                              + "error</ansired>:"
                                              + "space not known"))

        else:
            print("unknown parameter")
            continue


# ----------------------------------
def menu_space(cli_session, sds, header_str):
    """specific function space"""
    space_vars = {
        'name': '',
    }

    completer = WordCompleter(['name',
                               '?', 'exit',
                               ],
                              ignore_case=True)

    while 1:
        local_header_str = local_header(space_vars)
        if header_str is not None:
            print_formatted_text(HTML(header_str + '\n' + local_header_str))
        else:
            print_formatted_text(HTML(local_header_str))

        user_input = cli_session.prompt('top/space>',
                                        auto_suggest=AutoSuggestFromHistory(),
                                        completer=completer,
                                        bottom_toolbar=get_bottom_toolbar(sds))

        if handle_global_command(user_input, sds):
            continue

        if user_input in ('..', 'q'):
            return

        if user_input == '?':
            do_help()

        parse_local_command(user_input, space_vars, sds)
