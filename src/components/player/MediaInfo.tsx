import * as React from "react";

export interface MediaInfoProps {
    artist: string,
    title: string
}

export interface TextProps {
    text: string,
}

const Artist = (props: TextProps): JSX.Element => <span className="song_artist">{props.text}</span>;
const Title = (props: TextProps): JSX.Element => <span className="song_title">{props.text}</span>;

export function MediaInfo(props: MediaInfoProps) {
    return (
        <div className="media_info">
            <Title text={props.title} />
            <Artist text={props.artist} />
        </div>
    )
}
