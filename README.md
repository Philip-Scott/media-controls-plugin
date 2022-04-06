# Media Controls Plugin

This is very WIP plugin for adding the native (MPRIS) media controls to the [SteamOS Plugin Loader](https://github.com/SteamDeckHomebrew/PluginLoader).

![Plugin image](./.images/plugin.png)


## Changes Required to the Plugin Loader

To load the plugin, I had to do the following changes to the `plugin_loader.service` from the Plugin Loader in order to be able to connect to the User's info instead of the Root's. Hopefully this won't be required for future versions

```
[Service]
User=deck
Group=deck
Environment=DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
...
```