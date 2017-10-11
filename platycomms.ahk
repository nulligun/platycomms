; These are your keybinds, see this page for a list of valid keys/button names:
; https://autohotkey.com/docs/KeyList.htm

; Put a semi colon (;) in front of the line to disable it

; NOTE: if you are typing in text chat, the binds could trigger the voice chat. You can SUSPEND the bot by pressing F9, and then press it again to re-enable

; The asterix in front of each keybind means ANY modifier can be used while you press the key, so if you are holding shift it will still work.
; For a list of all modifiers see this link:
; https://autohotkey.com/docs/Hotkeys.htm#Symbols
; * = All modifiers
; ! = Alt
; ^ = Control
; + = Shift

JumpCheckKey = *H
ItsMeKey = *J
SuspendKey = *NumpadAdd

ImDownKey = *NumpadHome
ImDeadKey = *NumpadPgUp
HesDownKey = *NumpadEnd
HesDeadKey = *NumpadPgDn

NorthKey = *NumpadUp
SouthKey = *NumpadDown
EastKey = *NumpadRight
WestKey = *NumpadLeft

HelloKey = *NumpadMult
Yes = *NumpadIns
No = *NumpadDot
CancelKey = *NumpadClear
AfkKey = *NumpadSub
SteamOverlayKey = ~+Tab

; These probably should not be changed, unless you know what you are doing
ServerName := "Minecraft Sunday"
PlayerName := "Nulligun"
SecretKey := "123zxc"
EndPoint := "https://www.dandelopia.com/plat/web/client.php"

; The rest of this is code, no need to change anything down here

HotKey,~%SuspendKey%,DoSuspend
Hotkey, IfWinActive, Rust
HotKey,~%JumpCheckKey%,DoJumpCheck
HotKey,~%ItsMeKey%,DoItsMe
HotKey,~%ImDownKey%,DoImDown
HotKey,~%ImDeadKey%,DoImDead
HotKey,~%HesDownKey%,DoHesDown
HotKey,~%HesDeadKey%,DoHesDead
HotKey,~%NorthKey%,DoNorth
HotKey,~%SouthKey%,DoSouth
HotKey,~%EastKey%,DoEast
HotKey,~%WestKey%,DoWest
HotKey,~%HelloKey%,DoHello
HotKey,~%YesKey%,DoYes
HotKey,~%NoKey%,DoNo
HotKey,~%CancelKey%,DoNo
HotKey,~%AfkKey%,DoAfk
HotKey,~%SteamOverlayKey%,DoSteamOverlay
HotKey,~*ESC,DoCloseSteamOverlay

OverlayOpen := False

DoJumpCheck:	
  TriggerVoice("jump_check")
Return

DoItsMe:
  TriggerVoice("its_me")
Return

DoImDown:
  TriggerVoice("im_down")
Return

DoImDead:
  TriggerVoice("im_dead")
Return

DoHesDown:
  TriggerVoice("hes_down")
Return

DoHesDead:
  TriggerVoice("hes_dead")
Return

DoNorth:
  TriggerVoice("north")
Return

DoEast:
  TriggerVoice("east")
Return

DoWest:
  TriggerVoice("west")
Return

DoSouth:
  TriggerVoice("south")
Return

DoHello:
  TriggerVoice("hello")
Return

DoYes:
  TriggerVoice("yes")
Return

DoNo:
  TriggerVoice("no")
Return

DoCancel:
  TriggerVoice("cancel")
Return

DoAfk:
  TriggerVoice("afk")
Return

DoSteamOverlay:
  global OverlayOpen
  OverlayOpen:= !OverlayOpen
Return

DoCloseSteamOverlay:
  global OverlayOpen
  OverlayOpen := False
Return

DoSuspend:
  Suspend,Permit
  if (A_IsSuspended == 0) {
    SoundBeep, 500, 100
    SoundBeep, 400, 100
    SoundBeep, 250, 100
  }
  if (A_IsSuspended == 1) {
    SoundBeep, 250, 100	
    SoundBeep, 400, 100
    SoundBeep, 500, 100
  }
  Suspend
Return

TriggerVoice(command)
{
  global ServerName, PlayerName, SecretKey, EndPoint, overlayOpen
  if !OverlayOpen {
    oHttp := ComObjCreate("WinHttp.Winhttprequest.5.1")
    oHttp.open("GET", EndPoint . "?server_name=" . ServerName . "&player_name=" . PlayerName . "&secret_key=" . SecretKey . "&command=" . command)
    oHttp.send()
  }
}
