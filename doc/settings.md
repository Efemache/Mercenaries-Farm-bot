# settings.ini (conf/user/settings.ini)

## creation
Copy or move `conf/user/settings.sample.ini` to `conf/user/settings.ini` (just delete the ".sample" in the file's name).

⚠️ Set, at least, `GameDir` to your Heartstone installation directory.

## usage
`#` is used to disable a line. Delete `#` at the beginning of a line to enable the option.  
You need to have **only one** `location`, `level`, `mode`, ...


## [BotSettings] section
`monitor` : `1` if you have only one monitor or if you want to use your first monitor. Change this number to use another monitor.

`Resolution` : set it to Hearthstone resolution value. `1920x1080` is the default resolution (and the only officially supported) but you are able to use other 16:9 resolutions

~~`bot_speed` : if you change it, some bot actions will be slower/faster~~ (disabled since july 25, 2022 because it wasn't really working)

`MouseSpeed` : you can change the mouse speed. Don't put a low value like ```0```

`location` : use the name of the Travel point (```Barrens```, ```Felwood```, ```Blackrock```, ...)  
`mode` : `Normal` or `Heroic`  
`level` : put the level you want to start in the selected Bounty.  
When there are several levels with the same difficulty level (like `30`), you can check in the "file/1920x1080/levels" directory to find the right image for your level and use its name as a level like : `30b` or `30c` etc...

`GameDir` : (⚠️ Mandatory) set your Hearthstone installation directory because the bot will check for a logfile in Heartstone\Logs directory to find which mercenaries are on your board during a battle.  
For Windows users, it should be something like this `C:\Program Files (x86)\Hearthstone`

`WaitForEXP` : the bot will wait "WaitForEXP" seconds during a battle.  
The battle will take longer (if not `0`) and will give your more XP for the Hearthstone reward track

`quitBeforeBossFight`:  (`False` by default) (⚠️ don't set `stopAtBossFight` and `quitBeforeBossFight` to `True` together)  
Set it to `True` if you want to quit the bounty just before the final boss. When you always select the same level bounty, there is a good chance that it doesn't bring you coins that you will use (because your mercenaries are already maxed). Sometimes you prefer to quit the bounty because your coins rewards will be random and not for a specific mercenary.

`stopAtBossFight`: (`False` by default) (⚠️ don't set `stopAtBossFight` and `quitBeforeBossFight` to `True` together)  
Set it to `True` if you want the bot to stop before the final boss (so, you can do it yourself for example). 

`preferprotector`: (`False` by default)  
Set it to `True` will make the bot prioritize Protector (red) battle when it has a choice beetween 2 battles.  
`preferfighter`: (`False` by default)  
Set it to `True` will make the bot prioritize Fighter (green) battle when it has a choice beetween 2 battles.  
`prefercaster`: (`False` by default)  
Set it to `True` will make the bot prioritize Caster (blue) battle when it has a choice beetween 2 battles.

`preferelite`: (`False` by default)  
Set it to `True` will make the bot prioritize Elite battle when it has a choice beetween 2 battles.   
`preferbooncaster`: (`False` by default)  
Set it to `True` will make the bot prioritize Caster (blue) Boon when it has a choice beetween 2 battles.   
`preferboonfighter`: (`False` by default)  
Set it to `True` will make the bot prioritize Fighter (green) Boon when it has a choice beetween 2 battles.   
`preferboonprotector`: (`False` by default)  
Set it to `True` will make the bot prioritize Protector (red) Boon when it has a choice beetween 2 battles.   

`notificationURL`: use the URL you want to notify when the bot stops. For example, use [ifttt](https://ifttt.com/) to create the webhook notification.  
When the bot stops it will send the POST HTTP request to the webhook URL with the message body.

# log.config

MFB uses `<GameDir>/Logs/Zone.log` file (filled by Hearthstone during battle) to find your mercenaries on board.

Let's open or create log.config file with the correct info. Its default location is:
* Win 7-10 / WINE: `USER\AppData\Local\Blizzard\Hearthstone\`  (Paste `%LocalAppData%/Blizzard/Hearthstone` in the run dialog - Win+R to open)
* Win XP / WINE: `USER\Local Settings\Application Data\Blizzard\Hearthstone\`
* Mac: `~/Library/Preferences/Blizzard/Hearthstone/`

To be filled, you need to add these lines in your *log.config* and restart Hearthstone : 
```
[Zone]
LogLevel=1
FilePrinting=true
ConsolePrinting=false
ScreenPrinting=false
```

If this file doesn't exist : 
1. Go to its default location (as explained above)
2. Copy [this file](https://github.com/Efemache/Mercenaries-Farm-bot/blob/main/tools/log.config) in the previous directory
3. Restart Hearthstone



# combo.ini (conf/user/combo.ini)

Copy or move `conf/user/combo.sample.ini` to `conf/user/combo.ini` (just delete the ".sample" in the file's name).

<details><summary><i>Click here to find an example file</i></summary>

```
[Mercenary]
Alexstrasza=1,3
Anduin Wrynn=1,2
Antonidas=1
Aranna Starseeker=2,3,1
Baine Bloodhoof=1
#Balinda Stonehearth=2,3:chooseone=2
Balinda Stonehearth=1
Baron Geddon=2
Blademaster Samuro=1,3
Blink Fox=1,1,2
Brann Bronzebeard=1,2,3
Brightwing=1
Bru'kan=1,1,3
C'Thun=1,2
Cairne Bloodhoof=1
Captain Galvangar=1,3,2
Captain Hooktusk=1,2,3
Cariel Roame=2,1
Chi-Ji=1,1,3
Cookie, the Cook=1
Cornelius Roame=1,2,2
Deathwing=1,2,3
Diablo=1,2,3,2,3,2,3
Edwin, Defias Kingpin=1,2,3
Elise Starseeker=1,2,3
Eudora=1,2
Fathom-Lord Karathress=1,2
Kazakus, golem shaper=1
Garona Halforcen=1,2,3
Garrosh Hellscream=1,3
Genn Greymane=2,3,1
Gruul=1,2,3
Grommash Hellscream=2,3
Guff Runetotem=2
Illidan Stormrage=1,3,2
Jaina Proudmoore=1,3,2
King Krush=1,2,3
King Mukla=1,3
Kurtrus Ashfallen=1,3,2,3,2
Lady Anacondra=1
Lady Vashj=1,2,3
Leeroy Jenkins=1,2,3
Lokholar the Ice Lord=1
Long'xin=1
Lord Jaraxxus=3,2,1
Lord Slitherspear=1,2,3
Lorewalker Cho=1,2,3
Malfurion=1
Mannoroth=1,3
Millhouse Manastorm=1,2,3
Morgl the Oracle=1,2,1,2,1,2
Mr. Smite=1
Murky=1,3
Mutanus=1,2,2,2,2,2,2,2
Natalie Seline=1,3
Neeru Fireblade=1,1,3
Nefarian=1,3
Nemsy Necrofizzle=1,3,2
Niuzao=1,3
Patches the Pirate=1,2,3
Prince Malchezaar=1,2,3
Old Murk-Eye=1,2,3,2,3,2,3
Onyxia=1,3
Prophet Velen=1,3
Queen Azshara=1,2,3
Ragnaros=2
Rathorian=1,2,3
Rattlegore=1,2,3
Rokara=1,3
Scabbs Cutterbutter=1,2:chooseone=2
Sir Finley=1,3,2
Sinestra=1,3,2
Sky Admiral Rogers=1,3
Sneed=1,2
Sylvanas Windrunner=1,1,3
Tamsin Roame=1
Tavish Stormpike=1
Tess Greymane=1,2,3
The lich king=1,2
Thrall=1
Tidemistress Athissa=1,1,3,3
Trigore the Lasher=2
Tyrael=1,3,2
Tyrande Whisperwind=1,2
Valeera Sanguinar=1,2,3
Vanessa VanCleef=1
Vanndar Stormpike=1,1,3
Varden Dawngrasp=1
Varian Wrynn=3
Varok Saurfang=1,2
Vol'jin=1,2
War Master Voone=1,2,3
Wrathion=1,2,3
Yogg-Saron=1,2
Yu'lon=2
Xuen=1,3
Xyrella=1,3
Yrel=1,2,3
Ysera=1,2,3
Y'Shaarj=1,2
Uther Lightbringer=1,3,2
Zar'jira, the Sea Witch=1,3,2

[Neutral]
#Bladehand Berserker=1
Boggy=0
#Devilsaur=1
#Dragonmaw Poacher=1
#Drakonid=1
#Eudora's Cannon=0
#Elementium Terror=1
#Fathom Guard=1
#Fel Infernal=0
#Felfin Navigator=1
#Giantfin=1
#Greater Golem=1
#Grounding Totem=0
#Hozen Troublemaker=1
#Huffer=1
#Hulking Overfiend=1
#Hungry Naga=1
#Imp Familiar=2
#Jade Golem=0
#Lesser Fire Elemental=2
#Lesser Water Elemental=1
#Marching Murlocs=1
#Misha=1
#Mogu Conqueror=1
#Mukla's big brother=0
#Nightmare Viper=1
#Patchling=1
#Pufferfisher=1
#Saurok Raider=1
#Spawn of N'Zoth=1
#Spud M.E.=1
#Stonemaul Banner=2
#Superior Golem=1
#Void Consumer=1
#Water Elemental=1
#Warlord Parjesh=0
#Wavethrasher=0
```
</details>

This file is used to configure mercenaries' attacks. You need to edit it (with notepad for example).  
`#` is used to disable a line. Delete `#` at the beginning of a line to enable the mercenary.

Each battle round is seperated by a `,`.  
`1` means "use the first ability"  
`2` means "use the second ability"  
`3` means "use the third ability"  
`0` means "don't attack"  

At the end of the line, the bot will go back at the beginning ("first round" ability then "second", ...).


For example : 

```
Deathwing=0,1,3
#Leeroy Jenkins=3
```
Deathwing :  
- won't attack on the first round
- will use first ability on the second round
- third ability on third round
- won't attack on fourth round
- will use first ability on the fifth round
- etc...

Leeroy Jenkins is "disabled" (or "not configured") by user so the bot will use its first ability every time if it is not configured in MFB (conf/system/combo.ini).

## Target a friendly Mercenary/Minion selected by name
For abilities which can target an ally (find them in `attacks.json` with the "friend" tag), you can select the minion to target with the `name=` in combo.ini. Find an example below:  
```
Lady Anacondra=2:name=Nightmare Viper
```


## Choose One ability
To choose the card after a "Choose One" ability, use `:chooseone=2` to select the second card. Here, find an example: 
```
Balinda Stonehearth=1,3:chooseone=2,2
```
On the second turn, Balinda will use the third (`3`) ability, which is a "choose one" ability, requiring to make a choice between 2 cards. In this example above, Balinda will choose the second card (`:chooseone=2`).

On third turn , Balinda will use the second (`2`) ability (`,` is the separator).
On fourth turn, the bot start from the beginning (start of the line), so Balinda will use the first (`1`) ability

Example of mercenaries supporting it : `Balinda, Cho, Long'Xin, Malfurion, Murky, Rexxar, Scabbs, Kazakus`

## Select Mercenaries to put on board
By default, the bot clicks on "fight" button and Hearthstone takes the first, second and third cards (on the left) to put on board.  
You should have this feature in mind when you create your mercenaries group.  

If you want to select other Mercenaries to put on board, use `_handselection=`.  
The Mercenaries are separated by `+` (because some Mercenaries have a `,` in their names).  

This feature is useful to have a default group to start the bounty (using 1st, 2nd and 3rd cards) and select another group (3 other mercenaries) for the Boss Battle.
Example:
```
_handselection=Balinda Stonehearth+Baron Geddon+Ragnaros
```

## Set combo to fight a Boss
Add a new section with the boss'name between `[` and `]`.  
Find an example below (you can copy/paste it in combo.ini) :  
```
# CLiiuzESEU5ldGhlcnNwaXRlIEZyb3N0GAEiSgoJCCYQjgEYUiABCgsI+wEQiwIYugMgAQoKCGEQkgEYzgEgAAoLCPkBEIQCGLADIAAKCghjEJUBGNQBIAAKCwiVARDgARiMAiAAKJsB
[Netherspite]
_handselection=Balinda Stonehearth+Lokholar the Ice Lord+Jaina Proudmoore
Balinda Stonehearth=1,3:chooseone=1
Jaina Proudmoore=2
```

