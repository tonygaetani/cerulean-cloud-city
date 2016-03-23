#!/usr/bin/env python

import os
import soundcloud
import urllib
import Levenshtein
import re


#
# global Variables
#

project_root = os.getenv('PROJECT_ROOT', os.path.dirname(os.path.realpath(__file__)))
templates_root = os.getenv('TEMPLATES_ROOT', project_root + '/templates')
band_root = os.getenv('BAND_ROOT', project_root + '/../cerulean')
build_root = os.getenv('BUILD_ROOT', 'build')

soundcloud_client_id = os.environ['SOUNDCLOUD_CLIENT_ID']
soundcloud_client_secret = os.environ['SOUNDCLOUD_CLIENT_SECRET']
soundcloud_username = os.environ['SOUNDCLOUD_USERNAME']
soundcloud_password = os.environ['SOUNDCLOUD_PASSWORD']

# get a soundcloud client
client = soundcloud.Client(
    client_id=soundcloud_client_id,
    client_secret=soundcloud_client_secret,
    username=soundcloud_username,
    password=soundcloud_password,
)

track_title_2_id = {}
for track in client.get('/users/ceruleancity/tracks', limit=65):
    track_title_2_id[track.title] = track.id

#
# global functions
#

def get_track_id(name):
    try:
        ret = track_title_2_id[name]
    except KeyError:
        best = None
        for title in track_title_2_id.keys():
            score = Levenshtein.distance(str(title), str(name))
            if best is None or best[1] > score:
                best = (title, score)
        ret = track_title_2_id[best[0]]
    return str(ret)

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
    return band_metadata['git_root'] + album_name + '/' + album_name + '.zip'

def track_download_link(band_metadata, album, track):
    track_filename = urllib.quote(track['path'][track['path'].rfind('/'):])
    return band_metadata['git_root'] + urllib.quote(album['name']) + '/' + track_filename


#
# main program
#

def main(templates_path, albums_path, build_path):
    band_metadata = {'name': 'Cerulean City',
                     'description': 'Awesome music by Andrew Lake, Kieran McCoobery and Tony Gaetani',
                     'albums': [],
                     'git_root': 'https://raw.githubusercontent.com/marshzor/cerulean/master/'}
    for album_name in filter(lambda a: filter_album_names(albums_path, a), os.listdir(albums_path)):
        album_path = os.path.join(albums_path, album_name)
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
        band_metadata['albums'].append({'name': album_name,
                                        'path': album_path,
                                        'tracks': tracks,
                                        'description': album_description})
    # always clean html files
    try:
        cleanup_files = [html_file for html_file in os.listdir(build_path) if html_file.endswith('.html')]
        for html_file in cleanup_files:
            os.remove(build_path + '/' + str(html_file))
    except OSError:
        # if there's nothing there then make the directory
        os.makedirs(build_path)

    with open("{0}/index.html".format(build_path), 'w') as index:
        with open("{0}/header.template.html".format(templates_path), 'r') as header_template:
            for line in [template_line.replace('~~BAND~~', band_metadata['name']) for template_line in header_template.readlines()]:
                index.write(line)
        with open("{0}/band.template.html".format(templates_path), 'r') as band_template:
            for line in [template_line.replace('~~BAND~~', band_metadata['name']) for template_line in band_template.readlines()]:
                index.write(line)
        with open("{0}/description.template.html".format(templates_path), 'r') as description_template:
            for line in [template_line.replace('~~DESCRIPTION~~', band_metadata['description']) for template_line in description_template.readlines()]:
                index.write(line)
        for album_index, album in enumerate(band_metadata['albums']):
            album_page_name = "{0}.html".format(album['name'].replace(' ', '-'))
            album_page_path = "{0}/{1}".format(build_path, album_page_name)
            with open("{0}/album.template.html".format(templates_path), 'r') as album_template:
                for line in album_template.readlines():
                    line = line.replace('~~ALBUM~~', album['name'])
                    line = line.replace('~~ALBUM_PATH~~', album_page_name)
                    line = line.replace('~~ALBUM_DOWNLOAD_LINK~~', album_download_link(band_metadata, album))
                    index.write(line)
            with open("{0}/description.template.html".format(templates_path), 'r') as description_template:
                for line in [template_line.replace('~~DESCRIPTION~~', album['description']) for template_line in description_template.readlines()]:
                    index.write(line)
            with open(album_page_path, 'w') as album_page:
                with open("{0}/header.template.html".format(templates_path), 'r') as header_template:
                    for line in [template_line.replace('~~BAND~~', band_metadata['name']) for template_line in header_template.readlines()]:
                        album_page.write(line)
                with open("{0}/band.template.html".format(templates_path), 'r') as band_template:
                    for line in [template_line.replace('~~BAND~~', band_metadata['name']) for template_line in band_template.readlines()]:
                        album_page.write(line)
                with open("{0}/album.template.html".format(templates_path), 'r') as album_template:
                    for line in album_template.readlines():
                        line = line.replace('~~ALBUM~~', album['name'])
                        line = line.replace('~~ALBUM_PATH~~', album_page_name)
                        line = line.replace('~~ALBUM_DOWNLOAD_LINK~~', album_download_link(band_metadata, album))
                        album_page.write(line)
                with open("{0}/description.template.html".format(templates_path), 'r') as description_template:
                    for line in [template_line.replace('~~DESCRIPTION~~', album['description']) for template_line in description_template.readlines()]:
                        album_page.write(line)
                for track in album['tracks']:
                    with open("{0}/track.template.html".format(templates_path), 'r') as track_template:
                        for line in track_template.readlines():
                            line = line.replace('~~TRACK_TITLE~~', track['name'])
                            line = line.replace('~~TRACK_NUMBER~~', str(track['number']))
                            line = line.replace('~~TRACK_ID~~', get_track_id(track['name']))
                            line = line.replace('~~TRACK_DOWNLOAD_LINK~~', track_download_link(band_metadata, album, track))
                            album_page.write(line)
                with open("{0}/footer.template.html".format(templates_path), 'r') as footer_template:
                    for line in footer_template.readlines():
                        album_page.write(line)
        with open("{0}/footer.template.html".format(templates_path), 'r') as footer_template:
            for line in footer_template.readlines():
                index.write(line)


if __name__ == '__main__':
    main(templates_root, band_root, build_root)
