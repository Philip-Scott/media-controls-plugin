import * as React from "react";
import { getPlayers, MprisPlayerState } from "../mprisInterfase";

import "./../assets/scss/App.scss";

import { Player } from "./player/Player";

let loopId = -1

function MediaControls() {
  const [mprisPlayers, setMprisPlayers] = React.useState<MprisPlayerState[]>([]);
  const fetchData = async () => {
    setMprisPlayers(await getPlayers());
  }

  React.useEffect(() => {
    fetchData().catch()
  }, []);

  React.useEffect(() => {
    window.addEventListener('focus', (_event) => {
      loopId = window.setInterval(fetchData, 1000);
    });

    window.addEventListener('blur', (_event) => {
      window.clearInterval(loopId);
    });

    loopId = window.setInterval(fetchData, 1000);
  }, [])

  const players = mprisPlayers.map ((player) => {
    return Player(player)
  })

  return (
    <div className="app">
      {players}
    </div>
  );
}

export default (MediaControls);
