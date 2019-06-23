# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2019-06-23 15:55:06 alex>
#
# only for python v3

"""
SOLIDserver base object
"""

__all__ = ["Base"]


# just container class, no need for methods
# pylint: disable=R0903
class Base:
    """ standard class for all objects in SDS """
    # ---------------------------
    def __init__(self):
        """init the base object:
        """

    # ---------------------------
    def __str__(self):
        """return the string notation of the base object"""
        return "base"
