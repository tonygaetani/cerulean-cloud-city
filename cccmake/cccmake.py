#!/usr/bin/env python

import os
project_root = os.environ['PROJECT_ROOT']

import sys
sys.path.append( "{0}/cerulean-cloud-city".format(project_root))
sys.path.append( "{0}/sctrackid".format(project_root))
from ceruleancc import CccBand
from sctrackid import *

templates_root = project_root + '/cccmake/templates'
band_root = os.environ['GIT_REPO']
build_dir = os.getenv('BUILD_DIR', 'build')

band = CccBand(band_root)

# always clean html files
try:
    cleanup_files = [html_file for html_file in os.listdir(build_dir) if html_file.endswith('.html')]
    for html_file in cleanup_files:
        os.remove(build_dir + '/' + str(html_file))
except OSError:
    # if there's nothing there then make the directory
    os.makedirs(build_dir)

with open("{0}/index.html".format(build_dir), 'w') as index:
    with open("{0}/header.template.html".format(templates_root), 'r') as header_template:
        for line in [template_line.replace('~~BAND~~', band.name) for template_line in header_template.readlines()]:
            index.write(line)
    with open("{0}/band.template.html".format(templates_root), 'r') as band_template:
        for line in [template_line.replace('~~BAND~~', band.name) for template_line in band_template.readlines()]:
            index.write(line)
    with open("{0}/description.template.html".format(templates_root), 'r') as description_template:
        for line in [template_line.replace('~~DESCRIPTION~~', band.description) for template_line in description_template.readlines()]:
            index.write(line)
    for album in band.albums:
        album_page_name = "{0}.html".format(album.name.replace(' ', '-'))
        album_page_path = "{0}/{1}".format(build_dir, album_page_name)
        with open("{0}/album.template.html".format(templates_root), 'r') as album_template:
            for line in album_template.readlines():
                line = line.replace('~~ALBUM~~', album.name)
                line = line.replace('~~ALBUM_PATH~~', album_page_name)
                line = line.replace('~~ALBUM_DOWNLOAD_LINK~~', band.metadata['git_root'] + album.path[album.path.find(band.name + '/')+len(band.name):] + '/' + album.name.replace(' ', '%20') + '.zip')
                index.write(line)
        with open("{0}/description.template.html".format(templates_root), 'r') as description_template:
            for line in [template_line.replace('~~DESCRIPTION~~', album.description) for template_line in description_template.readlines()]:
                index.write(line)
        with open(album_page_path, 'w') as album_page:
            with open("{0}/header.template.html".format(templates_root), 'r') as header_template:
                for line in [template_line.replace('~~BAND~~', band.name) for template_line in header_template.readlines()]:
                    album_page.write(line)
            with open("{0}/band.template.html".format(templates_root), 'r') as band_template:
                for line in [template_line.replace('~~BAND~~', band.name) for template_line in band_template.readlines()]:
                    album_page.write(line)
            with open("{0}/album.template.html".format(templates_root), 'r') as album_template:
                for line in album_template.readlines():
                    line = line.replace('~~ALBUM~~', album.name)
                    line = line.replace('~~ALBUM_PATH~~', album_page_name)
                    line = line.replace('~~ALBUM_DOWNLOAD_LINK~~', band.metadata['git_root'] + album.path[album.path.find(band.name + '/')+len(band.name):] + '/' + album.name.replace(' ', '%20') + '.zip')
                    album_page.write(line)
            with open("{0}/description.template.html".format(templates_root), 'r') as description_template:
                for line in [template_line.replace('~~DESCRIPTION~~', album.description) for template_line in description_template.readlines()]:
                    album_page.write(line)
            for track in album.tracks:
                    trackid = getid(track.name)
                    with open("{0}/track.template.html".format(templates_root), 'r') as track_template:
                        for line in track_template.readlines():
                            line = line.replace('~~TRACK_TITLE~~', track.name)
                            line = line.replace('~~TRACK_NUMBER~~', str(track.number))
                            line = line.replace('~~TRACK_ID~~', trackid)
                            download_link = band.metadata['git_root'] + track.path[track.path.find(band.name + '/')+len(band.name):]
                            line = line.replace('~~TRACK_DOWNLOAD_LINK~~', download_link)
                            album_page.write(line)
            with open("{0}/footer.template.html".format(templates_root), 'r') as footer_template:
                for line in footer_template.readlines():
                    album_page.write(line)
    with open("{0}/footer.template.html".format(templates_root), 'r') as footer_template:
        for line in footer_template.readlines():
            index.write(line)
