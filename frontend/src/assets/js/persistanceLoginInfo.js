export function onConnect(isAuth, isManager, playerName) {
  // TODO maybe a token instead of isAuth ?
  let player = {
    isLogged: isAuth,
    isManager: isManager,
    name: playerName,
  };

  localStorage.setItem("player", JSON.stringify(player));
}

export function onDisconnect() {
  localStorage.removeItem("player");
}

export function getConnectedInfo() {
  let player = JSON.parse(localStorage.getItem("player"));

  if (player == null) {
    player = {
      isLogged: false,
      isManager: false,
      name: "",
    };
  }

  return player;
}

export default { onConnect, onDisconnect, getConnectedInfo };
