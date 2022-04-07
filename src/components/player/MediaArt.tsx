import * as React from "react";

export interface MediaArtProps {
    url: string
}

// TODO: Animate transition

export function MediaArt(props: MediaArtProps) {
    return <div className="media_art" style={{ backgroundImage: `url(${props.url})` }}></div>
}
