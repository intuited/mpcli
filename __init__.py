#!/usr/bin/env python
# Copyright (C) 2010 Ted Tibbetts
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, see <http://www.gnu.org/licenses/>
#
# To contact the author, write to "intuited" at the domain gmail dot com.
"""Thin command line interface to mpd."""

from pprint import PrettyPrinter as _PrettyPrinter

class PPIt(_PrettyPrinter):
    """PrettyPrinter which drains and dumps iterators.
    
    Iterators are dumped as lists.
    """
    def _format(self, object, *args, **kwargs):
        from collections import Iterator
        if isinstance(object, Iterator):
            object = list(object)
        return _PrettyPrinter._format(self, object, *args, **kwargs)

class format_results(object):
    """
    format_results(results) -> iter(strings)
    Return types for various values of _commands[command]:
        _fetch_none -> None
        None -> None
        _fetch_item -> str
        _fetch_object -> dict
        _fetch_outputs -> iter(dict)
        _fetch_list -> iter(strings)
        _fetch_songs -> iter(dict)
        _fetch_database -> iter(dict)
        _fetch_playlist -> iter(strings)
        _fetch_changes -> iter(dict)

        These are not yet being used in any real detail.

        The current implementation just pretty-prints the result,
          dumping iterators as lists.
    """
    from collections import Iterator, Mapping
    pformat = classmethod(_PrettyPrinter(indent=2).pformat)
    def __new__(cls, results):
        for line in PPIt(indent=2).pformat(results).split('\n'):
            yield line

def main(argv, stdin, mpd, stdout, stderr):
    mpc = mpd.MPDClient()
    mpc.iterate = True
    mpc.connect('localhost', '6600')
    try:
        try:
            command = getattr(mpc, argv[1])
        except IndexError:
            command = getattr(mpc, 'commands')
        ret = command(*argv[2:])
        for result in format_results(ret):
            print result
    finally:
        mpc.close()
        mpc.disconnect()
    

if __name__ == "__main__":
    from sys import argv, stdin, stdout, stderr
    import mpd
    main(argv, stdin, mpd, stdout, stderr)
