declare function call_plugin_method(methodName: string, arguments: {}): Promise<any>

export type playbackStatus = "Paused" | "Playing"
export type mprisBool = 0 | 1

export interface MprisPlayerState {
    id: string,
    artist: string,
    title: string,
    playbackStatus: playbackStatus,
    baseProps: {
        CanQuit: mprisBool,
        CanRaise: mprisBool,
        CanSetFullscreen: mprisBool,
        DesktopEntry: string,
        Fullscreen: mprisBool,
        HasTrackList: mprisBool,
        Identity: string,
    },
    properties: {
        CanControl: mprisBool,
        CanGoNext: mprisBool,
        CanGoPrevious: mprisBool,
        CanPause: mprisBool,
        CanPlay: mprisBool,
        CanSeek: mprisBool,
        LoopStatus: "None" | "Repeat",
        MaximumRate: number,
        Metadata: {
            "mpris:artUrl": string,
            "mpris:length": number,
            "mpris:trackid": string,
            "xesam:album": string,
            "xesam:artist": [string],
            "xesam:title": string,
        },
        MinimumRate: 1,
        PlaybackStatus: playbackStatus,
        Position: number,
        Rate: number,
        Shuffle: number,
        Volume: number,
    }
}

export async function playPause(playerId: string) {
    await call_plugin_method("playPause", { playerId });
}

export async function prevSong(playerId: string) {
    await call_plugin_method("prevSong", { playerId });
}

export async function nextSong(playerId: string) {
    await call_plugin_method("nextSong", { playerId });
}

export async function getPlayers(): Promise<MprisPlayerState[]> {
    return await call_plugin_method("get_player", {});
}
