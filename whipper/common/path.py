# -*- Mode: Python; test-case-name: whipper.test.test_common_path -*-
# vi:si:et:sw=4:sts=4:ts=4

# Copyright (C) 2009 Thomas Vander Stichele

# This file is part of whipper.
#
# whipper is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# whipper is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with whipper.  If not, see <http://www.gnu.org/licenses/>.

import re
import os.path

DEFAULT_TRACK_TEMPLATE = u'%r/%A - %d/%t. %a - %n'
DEFAULT_DISC_TEMPLATE = u'%r/%A - %d/%A - %d'

TEMPLATE_DESCRIPTION = '''
Tracks are named according to the track template, filling in the variables
and adding the file extension.  Variables exclusive to the track template are:
 - %t: track number
 - %a: track artist
 - %n: track title
 - %s: track sort name

Disc files (.cue, .log, .m3u) are named according to the disc template,
filling in the variables and adding the file extension. Variables for both
disc and track template are:
 - %A: album artist
 - %S: album sort name
 - %d: disc title
 - %y: release year
 - %r: release type, lowercase
 - %R: Release type, normal case
 - %x: audio extension, lowercase
 - %X: audio extension, uppercase

'''

SPECIAL_CHARACTER_FILTER = r'[\*\?&!\'\"\$\(\)`{}\[\]<>]'
FAT_CHARACTERS_FILTER = r'[:\*\?"<>|"]'


def filter_path(path):
    # replace separators with a space-hyphen or hyphen
    path = re.sub(r'[:]', ' -', path, re.UNICODE)
    path = re.sub(r'[\|]', '-', path, re.UNICODE)

    if config.getboolean('main', 'path_filter_special'):
        path = re.sub(SPECIAL_CHARACTERS_FILTER, '_', path, re.UNICODE)

    if config.getboolean('main', 'path_filter_fat'):
        path = re.sub(FAT_CHARACTERS_FILTER, '_', path, re.UNICODE)

    return path


def result_path(outdir, template, mbdiscid, metadata, track_number=None):
    v = {}
    v['A'] = 'Unknown Artist'
    # XXX what happens when it's None?
    v['d'] = mbdiscid  # fallback for title
    v['r'] = 'unknown'
    v['R'] = 'Unknown'
    v['B'] = ''  # barcode
    v['C'] = ''  # catalog number
    v['x'] = 'flac'
    v['X'] = v['x'].upper()
    v['y'] = '0000'
    if track_number is not None:
        v['a'] = v['A']
        v['t'] = '%02d' % track_number
        if track_number == 0:
            v['n'] = 'Hidden Track One Audio'
        else:
            v['n'] = 'Unknown Track %d' % track_number

    if metadata:
        release = metadata.release or '0000'
        v['y'] = release[:4]
        v['A'] = filter_path(metadata.artist)
        v['S'] = filter_path(metadata.sortName)
        v['d'] = filter_path(metadata.title)
        v['B'] = metadata.barcode
        v['C'] = metadata.catalogNumber
        if metadata.releaseType:
            v['R'] = metadata.releaseType
            v['r'] = metadata.releaseType.lower()
        if track_number > 0:
            v['a'] = filter_path(metadata.tracks[track_number - 1].artist)
            v['s'] = filter_path(metadata.tracks[track_number - 1].sortName)
            v['n'] = filter_path(metadata.tracks[track_number - 1].title)
        elif track_number == 0:
            # htoa defaults to disc's artist
            v['a'] = filter_path(metadata.artist)

    template = re.sub(r'%(\w)', r'%(\1)s', template)
    try:
        template = template % v
    except KeyError, e:
        raise ValueError('invalid template: unknown argument %' + str(e))

    return os.path.join(outdir, template)
