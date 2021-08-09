"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self,playlist_name : str,playlist_items : list ):
        self._playlist_name = playlist_name
        self._playlist_items = playlist_items
    @property
    def playlist_name(self) -> str:
        return self._playlist_name

    @property
    def playlist_items(self) -> list:
        return list(self._playlist_items)