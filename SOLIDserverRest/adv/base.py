# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2019-09-27 15:00:02 alex>
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

        # if true, modification on object are pushed to SDS
        self.in_sync = True

    # ---------------------------
    def set_sync(self):
        """set the object modification sync with SDS"""
        self.in_sync = True

    # ---------------------------
    def set_async(self):
        """set the object modification async with SDS,
           calling update() required"""
        self.in_sync = False

    # ---------------------------
    def __str__(self):
        """return the string notation of the base object"""
        return " sync: {}".format(self.in_sync)
