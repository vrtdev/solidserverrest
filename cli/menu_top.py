#
# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2019-10-06 16:24:23 alex>
#

"""
cli menu top
"""

from __future__ import unicode_literals, print_function

from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter

from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import HTML

from default import handle_global_command
from default import get_bottom_toolbar
from default import get_cli_version

from menu_connect import menu_connect
from menu_space import menu_space


def toolbar():
    """standard toolbar"""
    msg = 'EfficientIP SOLIDserver CLI '+get_cli_version()

    return msg


def menu_top(cli_session, sds):
    """top menu of the cli"""
    completer = WordCompleter(['connect',
                               'space',
                               'version', 'exit'],
                              ignore_case=True)

    while 1:
        header_str = toolbar()
        print_formatted_text(HTML(header_str))
        user_input = cli_session.prompt('top>',
                                        auto_suggest=AutoSuggestFromHistory(),
                                        completer=completer,
                                        bottom_toolbar=get_bottom_toolbar(sds))

        handle_global_command(user_input, sds)

        if user_input == 'connect':
            menu_connect(cli_session, sds, None)

        elif user_input == 'space':
            if sds['connected']:
                menu_space(cli_session, sds, None)
