#!/usr/bin/env python

import os
import shutil
import urllib
import re
from argparse import ArgumentParser

#
# global functions
#

def filter_album_names(path, name):
    if '.git' in name:
        return False
    elif name == '.ignore':
        return False
    return os.path.isdir(os.path.join(path, name))


def filter_tracks(filename):
    return True if '.mp3' in filename else False


def clean_track_name(filename):
    name = filename.replace('.mp3', '')
    while re.match(r'[0-9].*', name):
        name = name[1:]
    while re.match(r'.*[0-9]$', name):
        name = name[:-1]
    return name.replace('_', ' ').strip()


def album_download_link(band_metadata, album):
    album_name = urllib.quote(album['name'])
    return band_metadata['git_root'] + album['name'] + '/' + album_name + '.zip'


def track_download_link(band_metadata, album, track):
    track_filename = urllib.quote(track['path'][track['path'].rfind('/'):])
    return band_metadata['git_root'] + urllib.quote(album['name']) + '/' + track_filename


def get_metadata(path, band_name, git_root):
    try:
        with open(os.path.join(path, 'description'), 'r') as desc:
            description = desc.read()
    except Exception:
        description = ''
    metadata = {'name': band_name,
                'description': description,
                'albums': [],
                'git_root': git_root}
    for album_name in filter(lambda a: filter_album_names(path, a), os.listdir(path)):
        album_path = os.path.join(path, album_name)
        try:
            with open(os.path.join(album_path, 'description'), 'r') as desc:
                album_description = desc.read()
        except Exception:
            album_description = 'Shorts are comfy and easy to wear!'
        tracks = []
        track_number = 1
        for track in filter(filter_tracks, os.listdir(album_path)):
            track_name = clean_track_name(track)
            tracks.append({'number': track_number,
                           'name': track_name,
                           'path': os.path.join(album_path, track)})
            track_number += 1
        metadata['albums'].append({'name': album_name,
                                   'path': album_path,
                                   'tracks': tracks,
                                   'description': album_description})
    return metadata

#
# main program
#

def main(templates_path, args):
    # get the band metadata
    band_metadata = get_metadata(args.band_path, args.band_name, args.binaries_path)
    # always clean html files
    try:
        cleanup_files = [html_file for html_file in os.listdir(args.build_path) if html_file.endswith('.html')]
        for html_file in cleanup_files:
            os.remove(args.build_path + '/' + str(html_file))
    except OSError:
        # if there's nothing there then make the directory
        os.makedirs(args.build_path)
    # build the site
    with open("{}/index.html".format(args.build_path), 'w') as index:
        with open("{}/band.header.template.html".format(templates_path), 'r') as header_template:
            for line in [template_line.replace('~~BAND~~', band_metadata['name']) for template_line in header_template.readlines()]:
                index.write(line)
        with open("{}/band.template.html".format(templates_path), 'r') as band_template:
            for line in [template_line.replace('~~BAND~~', band_metadata['name']) for template_line in band_template.readlines()]:
                index.write(line)
        with open("{}/description.template.html".format(templates_path), 'r') as description_template:
            for line in [template_line.replace('~~DESCRIPTION~~', band_metadata['description']) for template_line in description_template.readlines()]:
                index.write(line)
        for album_index, album in enumerate(band_metadata['albums']):
            album_page_name = "{}.html".format(urllib.quote(album['name'].replace(' ', '-')))
            album_page_path = "{}/{}".format(args.build_path, album_page_name)
            with open("{}/album.template.html".format(templates_path), 'r') as album_template:
                for line in album_template.readlines():
                    line = line.replace('~~ALBUM~~', album['name'])
                    line = line.replace('~~ALBUM_PATH~~', album_page_name)
                    line = line.replace('~~ALBUM_DOWNLOAD_LINK~~', album_download_link(band_metadata, album))
                    index.write(line)
            with open("{}/description.template.html".format(templates_path), 'r') as description_template:
                for line in [template_line.replace('~~DESCRIPTION~~', album['description']) for template_line in description_template.readlines()]:
                    index.write(line)
            with open(album_page_path, 'w') as album_page:
                with open("{}/album.header.template.html".format(templates_path), 'r') as header_template:
                    for line in header_template.readlines():
                        line = line.replace('~~BAND~~', band_metadata['name'])
                        line = line.replace('~~ALBUM~~', album['name'])
                        line = line.replace('~~ALBUM_PATH~~', album_page_name)
                        line = line.replace('~~ALBUM_DOWNLOAD_LINK~~', album_download_link(band_metadata, album))
                        line = line.replace('~~DESCRIPTION~~', album['description'])
                        line = line.replace('~~FIRST_TRACK_DOWNLOAD_LINK~~', track_download_link(band_metadata, album, album['tracks'][0]))
                        line = line.replace('~~FIRST_TRACK_TITLE~~', album['tracks'][0]['name'])
                        album_page.write(line)
                for track in album['tracks']:
                    with open("{}/track.template.html".format(templates_path), 'r') as track_template:
                        for line in track_template.readlines():
                            line = line.replace('~~ALBUM~~', album['name'])
                            line = line.replace('~~TRACK_TITLE~~', track['name'])
                            line = line.replace('~~TRACK_DOWNLOAD_LINK~~',
                                                track_download_link(band_metadata, album, track))
                            album_page.write(line)
                with open("{}/album.end.template.html".format(templates_path), 'r') as album_end_template:
                    album_page.write(album_end_template.read())
                with open("{}/footer.template.html".format(templates_path), 'r') as footer_template:
                    album_page.write(footer_template.read())
        with open("{}/footer.template.html".format(templates_path), 'r') as footer_template:
            index.write(footer_template.read())


if __name__ == '__main__':
    project_root = os.path.dirname(os.path.realpath(__file__))
    parser = ArgumentParser(
        description='generates a super awesome website based on a folder full of music',
        epilog='see http://github.com/tonygaetani/cerulean-cloud-city for more details')
    parser.add_argument('--band-name', default='Cerulean', help='name of the band')
    parser.add_argument('--band-path', default=project_root + '/../cerulean', help='folder containing the music')
    parser.add_argument('--build-path', default='build', help='where to put the website')
    parser.add_argument('--binaries-path', default='https://raw.githubusercontent.com/marshzor/cerulean/master/',
                        help='root path to binaries for download/streaming')
    main(project_root + '/templates', parser.parse_args())
