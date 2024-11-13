import struct
import os
import xbmc
import xbmcgui

UTF_16 = 'UTF-16-LE'

class DBError(Exception):
    pass


class Field(object):
    def __init__(self, name, dtype, to_py=None, to_db=None):
        self.name = name
        self.dtype = dtype
        self.to_py = to_py
        self.to_db = to_db

        self.value = None

    def __setattr__(self, key, value):
        if key == 'value' and self.to_py and value is not None:
            value = self.to_py(value)
        self.__dict__[key] = value

    @staticmethod
    def wchar_to_str(b):
        s = b.decode(UTF_16)
        return s.rstrip('\0')

    @staticmethod
    def str_to_wchar(s, pad=64):
        b = s.encode(UTF_16)
        while len(b) < pad:
            b += '\0'.encode(UTF_16)
        return b


class DBStruct(object):
    def __init__(self, db):
        self.f = db.f
        self.fields = []
        self.data = []

    def _add_field(self, name, dtype='I', n=1, **kwargs):
        field = None
        for i in xrange(n):
            field = Field(name, dtype, **kwargs)
            self.fields.append(field)
        if n == 1:
            return field
        else:
            return self.fields[-n:]

    def read(self, offset):
        self.f.seek(offset)
        self.data = list(
            struct.unpack(self.format, self.f.read(self.size)))
        for field, value in zip(self.fields, self.data):
            field.value = value
        return self.data

    @property
    def format(self):
        return ' '.join(field.dtype for field in self.fields)

    @property
    def size(self):
        return struct.calcsize(self.format)


class Header(DBStruct):
    def __init__(self, db):
        super(Header, self).__init__(db)
        self.field_magic = self._add_field('magic')
        self.field_count_albums = self._add_field('count_albums')
        self.field_next_album_id = self._add_field('next_album_id')
        self.field_album_ids = self._add_field('album_id', n=100)
        self.field_next_track_id = self._add_field('next_track_id')
        self.read(0)


class Album(DBStruct):
    def __init__(self, db, offset):
        super(Album, self).__init__(db)
        self.field_magic = self._add_field('magic')
        self.field_album_id = self._add_field('album_id')
        self.field_count_tracks = self._add_field('count_tracks')
        self.field_track_group_ids = self._add_field('track_group_id', n=84)
        self.field_album_length_ms = self._add_field('album_length_ms')
        self.field_album_name = self._add_field('name', dtype='64s',
                                                to_py=Field.wchar_to_str,
                                                to_db=Field.str_to_wchar)
        self.read(offset)

        self.hex_id = '{:04x}'.format(self.field_album_id.value)

        self.path = os.path.join(db.root, self.hex_id)
        if not os.path.exists(self.path):
            raise DBError('directory "{}" does not exist for album "{}"'
                          .format(self.path, self.field_album_name.value))

        self.track_groups = {}
        self.tracks = {}

    def __repr__(self):
        return '<{}> {}'.format(self.hex_id, self.field_album_name.value)


class TrackGroup(DBStruct):
    def __init__(self, db, offset):
        super(TrackGroup, self).__init__(db)
        self.db = db
        self.field_magic = self._add_field('magic')
        self.field_album_id = self._add_field('album_id')
        self.field_track_group_id = self._add_field('track_group_id')
        self.field_padding = self._add_field('padding')
        self.field_track_id = self._add_field('track_id', n=6)
        self.field_track_length_ms = self._add_field('track_length_ms', n=6)
        self.field_track_name = self._add_field('track_name', dtype='64s', n=6,
                                                to_py=Field.wchar_to_str,
                                                to_db=Field.str_to_wchar)
        self.read(offset)

        self.uid = '{:04x}{:04x}'.format(self.field_album_id.value,
                                         self.field_track_group_id.value)
        self.tracks = {}

    def __repr__(self):
        return '<{}>'.format(self.uid)


class Track(object):
    def __init__(self, group, index):
        self.field_track_id = group.field_track_id[index]
        self.field_track_name = group.field_track_name[index]
        self.field_track_length_ms = group.field_track_length_ms[index]
        self.field_track_group_id = group.field_track_group_id
        self.field_album_id = group.field_album_id

        self.fields = (
            self.field_track_id,
            self.field_track_name,
            self.field_track_length_ms,
            self.field_track_group_id)

        self.hex_id = '{:08x}'.format(self.field_track_id.value)

        self.name = '{}.wma'.format(self.hex_id)
        self.path = os.path.join(
            group.db.root, self.hex_id[:4], self.name)

        if not os.path.exists(self.path):
            raise DBError('file "{}" does not exist for track "{}"'
                          .format(self.path, self.field_track_name.value))

    def __repr__(self):
        return '<{}> {}'.format(self.name, self.field_track_name.value)


class STDB:
    block_size = 512

    def __init__(self, path):
        self.f = open(path, 'rb')  # Open for reading only
        self.path = path
        self.root = os.path.dirname(path)

        self.header = Header(self)

        self.albums = self._get_albums()
        self.track_groups = self._get_track_groups()
        self.tracks = self._get_tracks()

    def _get_albums(self):
        albums = {}

        count = self.header.field_count_albums.value
        for offset in xrange(self.block_size,
                             self.block_size * count + self.block_size,
                             self.block_size):

            album = Album(self, offset)
            album_id = album.field_album_id.value

            albums[album_id] = album

        return albums

    def _get_track_groups(self):
        self.f.seek(0, 2)
        f_len = self.f.tell()

        group_beg = self.block_size * 101  # header + 100 soundtracks
        group_end = f_len  # EOF

        groups = {}
        for i, offset in enumerate(
                xrange(group_beg, group_end, self.block_size)):

            group = TrackGroup(self, offset)
            group_id = group.field_track_group_id.value
            album_id = group.field_album_id.value

            groups[group.uid] = group
            self.albums[album_id].track_groups[group_id] = group

        return groups

    def _get_tracks(self):
        tracks = {}
        for group in self.track_groups.itervalues():
            for i, field_id in enumerate(group.field_track_id):
                track_id = field_id.value
                if not track_id:
                    continue  # not sure if always consecutive

                track = Track(group, i)
                album_id = track.field_album_id.value

                tracks[track_id] = track
                group.tracks[track_id] = track
                self.albums[album_id].tracks[track_id] = track

        return tracks

def main():
    # Open the file selection dialog for user to choose the ST.DB file
    file_path = xbmcgui.Dialog().browse(1, "Select ST.DB file", 'files', '.db', False, False, '')
    
    if not file_path:  # If the user cancels or doesn't choose a file
        xbmcgui.Dialog().ok("Error", "No file selected. Exiting.")
        return
    
    try:
        db = STDB(file_path)
    except DBError as e:
        xbmcgui.Dialog().ok("Error", str(e))
        return
    
    # Display albums and tracks without any modifications
    album_names = {album.field_album_id.value: album.field_album_name.value for album in db.albums.values()}
    album_list = [album_name for album_name in album_names.values()]
    
    selected_album_index = xbmcgui.Dialog().select("Select an Album", album_list)
    
    if selected_album_index == -1:  # User cancelled
        xbmcgui.Dialog().ok("Cancelled", "No album selected. Exiting.")
        return
    
    selected_album_name = album_list[selected_album_index]
    selected_album_id = list(album_names.keys())[list(album_names.values()).index(selected_album_name)]
    
    album = db.albums.get(selected_album_id)
    
    if album:
        xbmcgui.Dialog().ok("Album Info", "Album: {}\nTracks: {}".format(album.field_album_name.value, len(album.tracks)))
    else:
        xbmcgui.Dialog().ok("Error", "No album data found.")

if __name__ == '__main__':
    main()
