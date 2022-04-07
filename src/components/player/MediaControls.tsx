import * as React from "react";
import { MprisPlayerState, nextSong, playPause, prevSong, mprisBool } from "../../mprisInterfase";

const PLAY_ICON = 
    <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" className="bi bi-play-fill" viewBox="0 0 16 16">
        <path d="m11.596 8.697-6.363 3.692c-.54.313-1.233-.066-1.233-.697V4.308c0-.63.692-1.01 1.233-.696l6.363 3.692a.802.802 0 0 1 0 1.393z"/>
    </svg>
            

const PAUSE_ICON = 
    <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" className="bi bi-pause-fill" viewBox="0 0 16 16">
        <path d="M5.5 3.5A1.5 1.5 0 0 1 7 5v6a1.5 1.5 0 0 1-3 0V5a1.5 1.5 0 0 1 1.5-1.5zm5 0A1.5 1.5 0 0 1 12 5v6a1.5 1.5 0 0 1-3 0V5a1.5 1.5 0 0 1 1.5-1.5z"/>
    </svg>

export interface MediaControlsProps {
    playerState: MprisPlayerState
}

export function MediaControls(props: MediaControlsProps) {
    const { id, playbackStatus, properties } = props.playerState;
    const { CanGoNext, CanGoPrevious } = properties

    const onPlayPauseClick = (_event: any) => {
        playPause(id);
    }

    const onPrevClick = (_event: any) => {
        prevSong(id);
    }

    const onNextClick = (_event: any) => {
        nextSong(id);
    }

    return (
        <div className="media_controls">
            <button onClick={onPrevClick} className="media_button" disabled={CanGoPrevious === 0}>
                    <svg viewBox="0 0 14 16" fill="currentColor" version="1.1" id="svg6">
                    <path
                        d="M 0.66666673,4 C 0.2973333,4 0,4.2973332 0,4.6666666 v 6.6666654 c 0,0.369333 0.2973333,0.666666 0.66666673,0.666666 H 1.3333334 c 0.3693333,0 0.6666667,-0.297333 0.6666667,-0.666666 V 8.7747383 L 7.0273442,11.916665 C 7.1201822,11.965708 7.2210335,12 7.3333336,12 c 0.36819,0 0.6666666,-0.298476 0.6666666,-0.666666 V 8.7526029 L 13.027344,11.916665 C 13.120184,11.965708 13.221034,12 13.333334,12 13.701523,12 14,11.701524 14,11.333334 V 4.6666666 C 14,4.2984768 13.701523,4 13.333334,4 c -0.1123,0 -0.213152,0.034291 -0.30599,0.083333 L 8.0000002,7.2473953 V 4.6666666 C 8.0000002,4.2984768 7.7015236,4 7.3333336,4 7.2210335,4 7.1201823,4.034291 7.0273442,4.0833329 L 2.0000001,7.2252599 V 4.6666666 C 2.0000001,4.2973332 1.7026667,4 1.3333334,4 Z"
                        id="path980-3" />
                    </svg>
                </button>
            <button onClick={onNextClick} className="media_button" disabled={CanGoNext === 0}>
                    <svg viewBox="2 0 14 16" fill="currentColor" version="1.1" id="svg6">
                    <path
                        d="M 15.333333,4 C 15.702667,4 16,4.2973332 16,4.6666666 v 6.6666654 c 0,0.369333 -0.297333,0.666666 -0.666667,0.666666 H 14.666667 C 14.297333,11.999998 14,11.702665 14,11.333332 V 8.7747383 L 8.9726558,11.916665 C 8.8798178,11.965708 8.7789665,12 8.6666664,12 8.2984764,12 7.9999998,11.701524 7.9999998,11.333334 V 8.7526029 L 2.972656,11.916665 C 2.879816,11.965708 2.778966,12 2.666666,12 2.298477,12 2,11.701524 2,11.333334 V 4.6666666 C 2,4.2984768 2.298477,4 2.666666,4 c 0.1123,0 0.213152,0.034291 0.30599,0.083333 L 7.9999998,7.2473953 V 4.6666666 C 7.9999998,4.2984768 8.2984764,4 8.6666664,4 8.7789665,4 8.8798177,4.034291 8.9726558,4.0833329 L 14,7.2252599 V 4.6666666 C 14,4.2973332 14.297333,4 14.666667,4 Z"
                        id="path980-3" />
                    </svg>
                </button>
            <button onClick={onPlayPauseClick} className="media_button play_button">
                {playbackStatus === "Playing" ? PAUSE_ICON : PLAY_ICON }
            </button>
        </div>
    )
}
