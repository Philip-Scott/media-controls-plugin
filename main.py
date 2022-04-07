import subprocess
import dbus
import sys
from collections import deque

# Backend shamelessly copied from https://github.com/airtower-luna/mpris-python/blob/main/mpris.py
# Frontend from: https://codepen.io/JavaScriptJunkie/pen/qBWrRyg
class MprisService:
    """Class representing an MPRIS2 compatible media player"""

    mpris_base = 'org.mpris.MediaPlayer2'
    player_interface = mpris_base + '.Player'
    tracklist_interface = mpris_base + '.TrackList'
    playlists_interface = mpris_base + '.Playlists'
    # see http://dbus.freedesktop.org/doc/dbus-specification.html#standard-interfaces-properties # noqa
    properties_interface = 'org.freedesktop.DBus.Properties'

    def __init__(self, servicename):
        """Initialize an MprisService object for the specified service name"""
        bus = dbus.SessionBus()
        self.name = servicename
        self.proxy = bus.get_object(self.name, '/org/mpris/MediaPlayer2')
        self.player = dbus.Interface(
            self.proxy, dbus_interface=self.player_interface)
        # tracklist is an optional interface, may be None depending on service
        self.tracklist = dbus.Interface(
            self.proxy, dbus_interface=self.tracklist_interface)
        # playlists is an optional interface, may be None depending on service
        self.playlists = dbus.Interface(
            self.proxy, dbus_interface=self.playlists_interface)
        self.properties = dbus.Interface(
            self.proxy, dbus_interface=self.properties_interface)
        # check if optional interfaces are available
        try:
            self.get_playlists_property('PlaylistCount')
        except dbus.exceptions.DBusException:
            self.playlists = None
        try:
            self.get_tracklist_property('CanEditTracks')
        except dbus.exceptions.DBusException:
            self.tracklist = None

    def base_properties(self):
        """Get all basic service properties"""
        return self.properties.GetAll(self.mpris_base)

    def player_properties(self):
        """Get all player properties"""
        return self.properties.GetAll(self.player_interface)

    def get_player_property(self, name):
        """Get the player property described by name"""
        return self.properties.Get(self.player_interface, name)

    def get_playlists_property(self, name):
        """Get the playlists property described by name"""
        return self.properties.Get(self.playlists_interface, name)

    def get_tracklist_property(self, name):
        """Get the tracklist property described by name"""
        return self.properties.Get(self.tracklist_interface, name)

def get_services():
    """Get the list of available MPRIS2 services
    :returns: a list of strings
    """
    services = []
    bus = dbus.SessionBus()
    for s in bus.list_names():
        if s.startswith(MprisService.mpris_base):
            services.append(s)
    return services

def _open_service(services, select):
    # try to open a service from the given list "services" by number
    # or dbus name in "select"
    service = None
    try:
        no = int(select)
        service = MprisService(services[no])
    except IndexError:
        print(f'MPRIS2 service no. {no} not found.')
    except ValueError:
        # no number provided, try name matching
        for s in services:
            if s.endswith(select):
                service = MprisService(s)
        if service is None:
            print(f'MPRIS2 service "{args.service}" not found.')
    return service

class Plugin:
    # The name of the plugin. This string will be displayed in the Plugin menu
    name = "Media Controls"
    # The name of the plugin author
    author = "Philip-Scott"

    main_view_html = "index.html"

    # The HTML that will be used to display a widget in the plugin main page
    tile_view_html = ""

    hot_reload = False

    async def __main(self):
        tile_view_html = ""


    async def get_player(self):
        services = get_services()

        players = []
        for service_id in services:
            defaultPlayer = MprisService(service_id)

            playbackStatus = defaultPlayer.get_player_property('PlaybackStatus')
            meta = defaultPlayer.get_player_property('Metadata')
            
            title = meta.get('xesam:title') or meta.get('xesam:url')
            artist = '[Unknown]'
            artists = meta.get('xesam:artist')

            if artists:
                artists = deque(artists)
                artist = artists.popleft()
                while len(artists) > 0:
                    artist = artist + ', ' + artists.popleft()
            
            baseProps = defaultPlayer.base_properties()
            player_properties = defaultPlayer.player_properties()

            players.append({"id": service_id,"playbackStatus": playbackStatus, "title": title, "artist": artist, "baseProps": baseProps, "properties": player_properties})

        return players

    async def playPause(self, **kwargs):
        service = MprisService(kwargs["playerId"])
        service.player.PlayPause()
    
    async def prevSong(self, **kwargs):
        service = MprisService(kwargs["playerId"])
        service.player.Previous()

    async def nextSong(self, **kwargs):
        service = MprisService(kwargs["playerId"])
        service.player.Next()
