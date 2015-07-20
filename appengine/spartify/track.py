import json
from urllib import quote_plus as quote

from google.appengine.api.urlfetch import fetch

import config


class Track:
    sid = None
    uri = None
    title = ''
    artist = ''
    album = ''
    length = ''
    image = ''
    _metadata_set = False

    def __init__(self, uri):
        self.uri = uri

        # derive the Spotify ID from the uri for now
        sid = uri.split(':')[2]
        self.sid = sid

    def set_metadata(self, title, artist, album, length, image):
        self.title = title
        self.artist = artist
        self.album = album
        self.length = length
        self.image = image
        self._metadata_set = True

    def lookup(self):
        if not self._metadata_set:
            try:
                #url = '%slookup/1/.json?uri=%s' % (config.SPOTIFY_BASE_URL,
                #        self.uri)
                url = '%sv1/tracks/%s' % (config.SPOTIFY_BASE_URL,
                        self.sid)
                res = fetch(url)
                res = json.loads(res.content)
                self.set_metadata(
                    res['name'],
                    res['artists'][0]['name'],
                    res['album']['name'],
                    (res['duration_ms'] / 1000),
                    res['album']['images'][2]['url'])
            except:
                pass

    def to_dict(self):
        return {
                'uri': self.uri,
                'title': self.title,
                'artist': self.artist,
                'album': self.album,
                'length': self.length,
                'image': self.image,
                }

    def __hash__(self):
        return hash(self.uri)
