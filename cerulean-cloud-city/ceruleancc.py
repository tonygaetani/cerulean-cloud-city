__author__ = 'tonygaetani'

import sys
import os
import yaml

__METADATA_FILE__ = 'metadata.yaml'
def create_metadata(path):
    try:
        with open(os.path.join(path,__METADATA_FILE__), 'r') as file_metadata:
            return yaml.safe_load(file_metadata)
    except IOError:
        return None

def get_metadata(metadata, key):
    if not metadata:
        return ''
    try:
        return metadata[key]
    except KeyError:
        return ''

class CccBand:
    """An object representing a cerulean cloud city band

    The object is built by parsing the metadata and other contents of a
    cerulean cloud city compliant git repository

    Attributes:
        path (string): path to metadata file
        metadata (hash): album metadata
        name (string):         the band name
        description (string):       description of the band
        albums (Set of CccAlbum):   collection of albums belonging to the band
    """

    def __init__(self, path):
        self.path = path
        self.metadata = create_metadata(path)
        self.name = get_metadata(self.metadata, 'name')
        # TODO more of this inference stuff
        # fall back to directory name if there is no name in metadata
        if self.name == '':
            self.name = os.path.basename(path)
        self.description = get_metadata(self.metadata, 'description')
        self.albums = []
        for album_name in [x for x in os.listdir(path) if '.git' not in x and os.path.isdir(os.path.join(path, x))]:
            self.albums.append(CccAlbum(os.path.join(path, album_name)))

    def __str__(self):
        output = ""
        for album in self.albums:
            output = output + str(album)
            for track in album.tracks:
                output = output + "\t" + str(track)
        return output

class CccAlbum:
    """An object representing a cerulean cloud city album

    The object is built by parsing the metadata and other contents of a
    cerulean cloud city compliant git repository

    Attributes:
        path (string): path to metadata file
        metadata (hash): album metadata
        name (string): album name
        tracks (set of CccTracks): collection of tracks on the album
        artwork (string): path to artwork png file
    """

    def __init__(self, path):
        self.path = path
        self.metadata = create_metadata(path)
        self.tracks = []
        if self.metadata is None:
            # TODO implement directory structure inference
            sys.stderr.write("no metadata found at {0}".format(path))
            return
        for track in self.metadata['tracks']:
            self.tracks.append(CccTrack(os.path.join(path, track['file']), track['name'], track['number']))
        self.name = get_metadata(self.metadata, 'name')
        self.description = get_metadata(self.metadata, 'description')

    def __str__(self):
        output = ""
        output = output + "album: {0}\n".format(self.name)
        output = output + "description: {0}\n".format(self.description)
        return output

class CccTrack:
    """An object representing a cerulean cloud city album track

    Attributes:
        path (string): path to the audio file on disk
        name (string): track name
        number (string): track number
    """

    def __init__(self, path, name, number):
        self.path = path
        self.name = name
        self.number = number

    def __str__(self):
        return "track {0}: {1}\n".format(self.number, self.name)
