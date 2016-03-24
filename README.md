cerulean cloud city
===================
This repository auto-generates the a band website. The website contains a 

homepage with links to each album, and a page for each album. You can see a 

working example at http://ceruleancity.github.io.

usage
=====
```
usage: cerulean-cloud-city.py [-h] [--band-name BAND_NAME]
                              [--band-path BAND_PATH]
                              [--build-path BUILD_PATH]
                              [--binaries-path BINARIES_PATH]

generates a super awesome website based on a folder full of music

optional arguments:
  -h, --help            show this help message and exit
  --band-name BAND_NAME
                        name of the band
  --band-path BAND_PATH
                        folder containing the music
  --build-path BUILD_PATH
                        where to put the website
  --binaries-path BINARIES_PATH
                        root path to binaries for download/streaming
```

folder structure
----------------
```
band-path/
---------/description
---------/album1/
----------------/description
----------------/track1.mp3
----------------/track2.mp3
----------------/...
----------------/trackn.mp3
----------------/album1.zip
---------/album2/
----------------/track1.mp3
----------------/track2.mp3
----------------/...
----------------/trackn.mp3
----------------/album2.zip
---------/...
---------/albumn/
```
