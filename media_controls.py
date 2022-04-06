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

    main_view_html = """
        <html>
            <head>
                <link rel="stylesheet" href="/steam_resource/css/2.css">
                <link rel="stylesheet" href="/steam_resource/css/39.css">
                <link rel="stylesheet" href="/steam_resource/css/library.css">
                <style>
                    .player {
                        box-shadow: 0px 15px 35px -5px rgb(50 88 130 / 32%);
                        border-radius: 6px;
                        height: 254px;
                        margin: 12px 12px;
                        padding: 8px;
                        display: flex;
                        flex-direction: column;
                        position: relative;
                        background: rgb(237 235 247);
                    }

                    .media_art {
                        width: 170px;
                        height: 170px;
                        margin-top: 4px;
                        margin-left: -20px;
                        flex-shrink: 0;
                        position: relative;
                        border-radius: 18px;
                        background-size: cover;
                        background-position: center;
                        z-index: 1;
                    }

                    .media_art:before {
                        content: "";
                        background: inherit;
                        width: 100%;
                        height: 100%;
                        box-shadow: 0px 10px 40px 0px rgb(76 70 124 / 50%);
                        display: block;
                        z-index: 1;
                        position: absolute;
                        top: 28px;
                        transform: scale(0.8);
                        filter: blur(10px);
                        opacity: 0.9;
                        border-radius: 24px;
                    }

                    .media_art:after {
                        content: "";
                        background: inherit;
                        width: 100%;
                        height: 100%;
                        box-shadow: 4px 4px 11px 0px rgb(76 70 124 / 50%);
                        display: block;
                        z-index: 2;
                        position: absolute;
                        border-radius: 15px;
                    }


                    .media_info {
                        position: absolute;
                        top: 200px;
                        color: black;
                        display: flex;
                        flex-direction: column;
                        width: 95%; 
                        z-index: 1;
                    }

                    .song_title {
                        font-weight: 600;
                        margin: 5px;
                        white-space: nowrap;
                        overflow: hidden;
                        display: block;
                        text-overflow: ellipsis;
                        white-space: nowrap;
                    }

                    .song_artist {
                        margin: 0px 5px;
                        font-weight: lighter;
                        white-space: nowrap;
                        overflow: hidden;
                        display: block;
                        text-overflow: ellipsis;
                        white-space: nowrap;
                    }

                    .spacer {
                        flex-grow: 1;
                    }

                    .blur {
                        filter: blur(15px);
                        overflow: hidden;
                        width: 100%;
                    }
                    
                    .media_controls {
                        position: absolute;
                        display: flex;
                        top: 96px;
                        right: 8px;
                        flex-direction: column;
                        align-items: center;
                        justify-content: center;
                        text-align: center;
                        height: 51px;
                        z-index: 1;
                    }

                    .media_button {
                        color: #3d3d3d;
                        border-radius: 50%;
                        border: none;
                        background: transparent;
                        width: 44px;
                        height: 44px;
                        margin-bottom: 8px;
                        display: inline-block;
                    }

                    .media_button.play_button {
                        background: transparent;
                        margin: 0 8px 0 6px;
                        border-radius: 50%;
                        border: solid 4px currentColor;
                        padding: 4px;
                        width: 68px;
                        height: 68px;
                        display:inline-block;
                    }

                </style>
                <script>
                    String.format = function (format) {
                        var args = Array.prototype.slice.call (arguments, 1);
                        return format.replace (/{(\d+)}/g, function (match, number) {
                        return typeof args[number] != 'undefined'
                            ? args[number]
                        : match;
                        });
                    };

                    const PLAYER_TITLE = `<div class="quickaccessmenu_Title_34nl5">{0}</div>`
                    
                    const PLAYER = `
                        <div class="player">
                            <div class="media_art" style="background-image: url({2})"></div>
                            <div class="media_info">
                                {0}
                            </div>

                            <div class="media_controls">
                                {1}
                            </div>
                        </div>
                    `;

                    const MEDIA_INFO = `
                        <span class="song_title" >{0}</span>
                        <span class="song_artist" >{1}</span>
                    `

                    const BACK_BUTTON = `
                        <button onclick="prevSong('{0}')" class="media_button" {1}>
                            <?xml version="1.0" encoding="UTF-8" standalone="no"?>
                            <svg viewBox="0 0 16 16" version="1.1" id="svg6">
                            <defs
                                id="defs10" />
                            <path
                                d="M 0.66666673,4 C 0.2973333,4 0,4.2973332 0,4.6666666 v 6.6666654 c 0,0.369333 0.2973333,0.666666 0.66666673,0.666666 H 1.3333334 c 0.3693333,0 0.6666667,-0.297333 0.6666667,-0.666666 V 8.7747383 L 7.0273442,11.916665 C 7.1201822,11.965708 7.2210335,12 7.3333336,12 c 0.36819,0 0.6666666,-0.298476 0.6666666,-0.666666 V 8.7526029 L 13.027344,11.916665 C 13.120184,11.965708 13.221034,12 13.333334,12 13.701523,12 14,11.701524 14,11.333334 V 4.6666666 C 14,4.2984768 13.701523,4 13.333334,4 c -0.1123,0 -0.213152,0.034291 -0.30599,0.083333 L 8.0000002,7.2473953 V 4.6666666 C 8.0000002,4.2984768 7.7015236,4 7.3333336,4 7.2210335,4 7.1201823,4.034291 7.0273442,4.0833329 L 2.0000001,7.2252599 V 4.6666666 C 2.0000001,4.2973332 1.7026667,4 1.3333334,4 Z"
                                id="path980-3" />
                            </svg>
                        </button>
                    `

                    const PLAY_PAUSE_BUTTON = `
                        <button onclick="playPause('{0}')" class="media_button play_button">
                            {1}
                        </button>
                    `

                    const NEXT_BUTTON = `
                        <button onclick="nextSong('{0}')" class="media_button" {1}>
                            <svg viewBox="0 0 16 16" fill="currentColor" version="1.1" id="svg6">
                            <defs
                                id="defs10" />
                            <path
                                d="M 15.333333,4 C 15.702667,4 16,4.2973332 16,4.6666666 v 6.6666654 c 0,0.369333 -0.297333,0.666666 -0.666667,0.666666 H 14.666667 C 14.297333,11.999998 14,11.702665 14,11.333332 V 8.7747383 L 8.9726558,11.916665 C 8.8798178,11.965708 8.7789665,12 8.6666664,12 8.2984764,12 7.9999998,11.701524 7.9999998,11.333334 V 8.7526029 L 2.972656,11.916665 C 2.879816,11.965708 2.778966,12 2.666666,12 2.298477,12 2,11.701524 2,11.333334 V 4.6666666 C 2,4.2984768 2.298477,4 2.666666,4 c 0.1123,0 0.213152,0.034291 0.30599,0.083333 L 7.9999998,7.2473953 V 4.6666666 C 7.9999998,4.2984768 8.2984764,4 8.6666664,4 8.7789665,4 8.8798177,4.034291 8.9726558,4.0833329 L 14,7.2252599 V 4.6666666 C 14,4.2973332 14.297333,4 14.666667,4 Z"
                                id="path980-3" />
                            </svg>
                        </button>
                    `      

                    const MUSIC_ICON_SVG = `
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-music-note" viewBox="0 0 16 16">
                            <path d="M9 13c0 1.105-1.12 2-2.5 2S4 14.105 4 13s1.12-2 2.5-2 2.5.895 2.5 2z"/>
                            <path fill-rule="evenodd" d="M9 3v10H8V3h1z"/>
                            <path d="M8 2.82a1 1 0 0 1 .804-.98l3-.6A1 1 0 0 1 13 2.22V4L8 5V2.82z"/>
                        </svg>
                    `;

                    const PLAY_ICON = `
                    <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-play-fill" viewBox="0 0 16 16">
                        <path d="m11.596 8.697-6.363 3.692c-.54.313-1.233-.066-1.233-.697V4.308c0-.63.692-1.01 1.233-.696l6.363 3.692a.802.802 0 0 1 0 1.393z"/>
                    </svg>
                    `

                    const PAUSE_ICON = `
                    <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-pause-fill" viewBox="0 0 16 16">
                        <path d="M5.5 3.5A1.5 1.5 0 0 1 7 5v6a1.5 1.5 0 0 1-3 0V5a1.5 1.5 0 0 1 1.5-1.5zm5 0A1.5 1.5 0 0 1 12 5v6a1.5 1.5 0 0 1-3 0V5a1.5 1.5 0 0 1 1.5-1.5z"/>
                    </svg>
                    `

                    function makePlayer (player, showTitle) {
                        properties = player.properties

                        let html = ''

                        if (showTitle) {
                            html +=  String.format (PLAYER_TITLE, player.baseProps.Identity)
                        }

                        let mediaControls = ''

                        mediaControls += String.format (BACK_BUTTON, player.id, properties.CanGoPrevious === 1 ? '' : 'disabled')
                        mediaControls += String.format (NEXT_BUTTON, player.id, properties.CanGoNext === 1 ? '' : 'disabled')
                        mediaControls += String.format (PLAY_PAUSE_BUTTON, player.id, player.playbackStatus === 'Paused' ? PLAY_ICON: PAUSE_ICON)

                        const mediaInfo = String.format (MEDIA_INFO, player.title, player.artist)

                        html += String.format (PLAYER, mediaInfo, mediaControls, properties.Metadata["mpris:artUrl"]) 
                        
                        return html
                    }

                    async function updateUi() {
                        console.log ("update")
                        const players = await call_plugin_method("get_player", {});

                        let html = ''

                        const playersHtml = players.map (player => {
                            return makePlayer(player, players.length > 1)
                        })

                        html += playersHtml

                        const pluginRoot = document.getElementById('MPRIS_PLAYER');
                        console.log (players)

                        pluginRoot.innerHTML = html
                    }

                    async function playPause (playerId) {
                        const players = await call_plugin_method("playPause", { playerId });
                    }

                    async function prevSong (playerId) {
                        const players = await call_plugin_method("prevSong", { playerId });
                    }

                    async function nextSong (playerId) {
                        const players = await call_plugin_method("nextSong", { playerId });
                    }

                    async function startLoop () {
                        window.setInterval(myCallback, 500);
                    }

                    let loopId = -1;

                    async function init () {
                        window.addEventListener('focus', (event) => {
                            loopId = window.setInterval(updateUi, 1000);
                        });

                        window.addEventListener('blur', (event) => {
                            window.clearInterval(loopId);
                        });                        
                        
                        loopId = window.setInterval(updateUi, 1000);
                        
                        updateUi();
                    }

                </script>
            </head>
            <body onload="init()">
                <div id="MPRIS_PLAYER"></div>
            </body>
        </html>
    """

    # The HTML that will be used to display a widget in the plugin main page
    tile_view_html = ""

    hot_reload = True

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
