import * as React from "react";
import { MprisPlayerState } from "../../mprisInterfase";
import { MediaArt } from "./MediaArt";
import { MediaControls } from "./MediaControls";
import { MediaInfo } from "./MediaInfo";

export function Player(playerState: MprisPlayerState) {
    const { artist, title, properties } = playerState;
    const {Metadata} = properties

    return (
    <div className="player">
        <MediaArt url={Metadata["mpris:artUrl"]}></MediaArt>
        <MediaInfo artist={artist} title={title} ></MediaInfo>
        <MediaControls playerState={playerState}></MediaControls>
    </div>
    )
}
