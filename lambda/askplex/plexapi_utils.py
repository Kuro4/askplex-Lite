from typing import Optional, List
from plexapi.library import MusicSection
from plexapi.server import PlexServer
from plexapi.audio import Artist, Track, Album
from plexapi.exceptions import NotFound
from plexapi.playlist import Playlist

def get_artist(section: MusicSection, name: str) -> Optional[Artist]:
    """
    MusicSection からアーティスト名を検索して取得する。

    Args:
        section (MusicSection): 検索対象の MusicSection。
        name (str): 検索したいアーティスト名。

    Returns:
        Optional[Artist]: 検索したアーティスト。取得できなければ None。
    """

    matches = section.searchArtists(title=name)
    if matches:
        return matches[0]

    match = section.searchArtists(title__icontains=name)
    if match:
        return match[0]

    match = section.searchArtists(titleSort__icontains=name)
    if match:
        return match[0]

    return None

def get_track(artist: Artist, title: str) -> Optional[Track]:
    """
    Artist から曲名を検索して Track を取得する。

    Args:
        artist (Artist): 曲を検索するアーティスト。
        title (str): 検索したい曲名。

    Returns:
        Optional[Track]: 検索したトラック。取得できなければ None。
    """

    try:
        track = artist.track(title=title)
        return track
    except NotFound:
        pass

    match = artist.tracks(title__icontains=title)
    if match:
        return match[0]

    return None

def get_album(artist: Artist, title: str) -> Optional[Album]:
    """
    Artist からアルバム名を検索して Album を取得する。

    Args:
        artist (Artist): アルバムを検索するアーティスト。
        title (str): 検索したいアルバム名。

    Returns:
        Optional[Album]: 検索したアルバム。取得できなければ None。
    """

    try:
        album = artist.album(title=title)
        return album
    except NotFound:
        pass

    albums = artist.albums(title__icontains=title)
    if albums:
        return albums[0]
        
    return None

def get_playlist(server: PlexServer, title: str) -> Optional[Playlist]:
    """
    PlexServer からプレイリスト名を検索して Playlist を取得する。

    Args:
        server (PlexServer): 検索対象のサーバ。
        title (str): 検索したプレイリスト名。
    
    Returns:
        Optional[Playlist]: 検索したプレイリスト。取得できなければNone。
    """

    try:
        return server.playlist(title)
    except NotFound:
        pass

    playlists = server.search(query=title, mediatype="playlist")
    if playlists:
        return playlists[0]
    
    return None

def get_random_tracks(section: MusicSection, maxresults: int) -> List[Track]:
    """
    MusicSection からランダムに Track を取得する。

    Args:
        section (MusicSection): 対象の MusicSection。
        maxresults (int): 取得するトラック数。

    Returns:
        List[Artist]: 取得したトラック。
    """

    return section.searchTracks(sort="random", maxresults=maxresults)

def get_random_tracks_by_artist(section: MusicSection, maxresults: int, artist: Artist) -> List[Track]:
    """
    MusicSection から指定したアーティストの Track をランダムに取得する。

    Args:
        section (MusicSection): 対象の MusicSection。
        maxresults (int): 取得するトラック数。
        artist (Artist): 対象のアーティスト。

    Returns:
        List[Artist]: 取得したトラック。
    """

    return section.search(
        libtype='track',
        sort='random',
        maxresults=maxresults,
        filters={'artist.id': artist.ratingKey}
    )

def get_random_tracks_by_genre(section: MusicSection, maxresult: int, genre: str) -> List[Track]:
    """
    MusicSection から指定したジャンルの Track をランダムに取得する。

    Args:
    section (MusicSection): 対象の MusicSection。
    maxresults (int): 取得するトラック数。
    genre (str): 対象のジャンル。

    Returns:
        List[Artist]: 取得したトラック。
    """
    section.searchTracks(sort='random', maxresults=maxresult, style=genre)