# Platycomms

A discord bot for Rust that allows the user to trigger voice queues using AutoHotkey

## How to setup Autohotkey script

First, you need to download and install [Auto Hotkey](https://autohotkey.com/download/ahk-install.exe)

After it's installed you need to download the [platycomms.ahk](https://raw.githubusercontent.com/stevemulligan/platycomms/master/platycomms.ahk) script. When the script is downloaded, you need to configure a few things before you use it. Right click on the script you just downloaded and choose "Edit Script". Scroll down to "Server Name" and change the value match the name of your Discord server. You'll also want to change PlayerName to match the name of the player that will trigger the hotkeys.  And set SecretKey and EndPoint to the values given to you by the person that configured the bot.

You can also comment out or change the default keybinds.  There are instructions in the file that tell you where to find key names and what symbols to use for modifiers like Shift and Control.  Save the file and then right click it and choose "Compile Script". You can launch the script and keep it running. It will only send commands to the server when Rust is the active window. NumLock must be OFF for the default keybinds to work. The + key will suspend or resume the hotkey script. You'll want to use this if you type in chat.
