# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division, print_function

import click

from . import plocate


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--all', '-A', is_flag=True, default=False,
              help='only print entries that match all patterns')
@click.option('--basename', '-b', 'match', flag_value='basename',
              help='match only the base name of path names')
@click.option('--count', '-c', is_flag=True, default=False,
              help='only print number of found entries')
@click.option('--database', '-d',
              type=click.File(mode='rb'), metavar='DBPATH',
              default='/var/lib/mlocate/mlocate.db', show_default=True,
              help='use DBPATH instead of default database')
@click.option('--existing', '-e', is_flag=True, default=False,
              help='only print entries for currently existing files')
@click.option('--follow', '-L', 'follow', is_flag=True,
              help='follow trailing symbolic links when checking file existence (default)')
@click.option('--ignore-case', '-i', is_flag=True, default=False,
              help='ignore case distinctions when matching patterns')
@click.option('--limit', '-l', '-n', metavar='LIMIT', type=int,
              help='limit output (or counting) to LIMIT entries')
@click.option('--nofollow', '-P', '-H', 'follow', is_flag=True, default=True,
              help='don\'t follow trailing symbolic links when checking file')
@click.option('--type', '-t', 'type',
              type=click.Choice(['all', 'file', 'dir']), default='all',
              help='match only specific type of entries')
@click.option('--wholename', '-w', 'match', flag_value='wholename', default=True,
              help='match whole path name (default)')
@click.option('--null', '-0', is_flag=True, default=False,
              help='separate entries with NUL on output')
@click.argument('patterns', metavar='PATTERNS', nargs=-1)
def main(**kwargs):
    """Search for entries in a mlocate database."""
    res = plocate.locate(**kwargs)
    if kwargs['count']:
        click.echo(res)
    else:
        sep = '\0' if kwargs['null'] else '\n'
        for entry in res:
            click.echo(entry, nl=False)
            click.echo(sep, nl=False)


if __name__ == "__main__":
    main()
