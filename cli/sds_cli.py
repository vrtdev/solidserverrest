#!/usr/bin/env python
#
# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2019-10-06 16:30:40 alex>
#

"""
SOLIDserver cli

"""

from __future__ import unicode_literals, print_function

import sys
import os

from prompt_toolkit.history import FileHistory
from prompt_toolkit import PromptSession

from menu_top import menu_top

sys.path.append(os.getcwd())

import SOLIDserverRest.adv as sdsadv

CLI_SESSION = PromptSession(history=FileHistory('.sds_cli.txt'))

if __name__ == '__main__':
    SDS = {
        'cnx': sdsadv.SDS(),
        'connected': False,
        'version': None,
        'load_stats_time': 0,
        'space': None,
    }

    try:
        menu_top(CLI_SESSION, SDS)
    except EOFError:
        exit()
    except KeyboardInterrupt:
        exit()
