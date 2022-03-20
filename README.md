# Mercenaries-Farm-Bot for Hearthstone
```diff
Bot is on a development stage but it already works to do some "Tasks" and run low level bounties
```
```diff
In the last version (0.4.0), you need to modify your Hearthstone log.config :
C:\Users\YOURUSER\AppData\Local\Blizzard\Hearthstone\log.config
and add :
[Zone]
LogLevel=1
FilePrinting=true
ConsolePrinting=false
ScreenPrinting=false
```
## Purpose
The purpose of this bot is to automatically pass the levels to level up your heros, win somes coins and do some campfire tasks 

It started as a fork of (and a collaboration to) a previous project but after being the only dev and going with a different point of view, I decided to make a new project.

(the purpose of the previous project was to autogroup heroes to level them up to 30)

There is a branch main to use and a branch for dev with new features but not well tested.


## News & contact 
More informations in [Wiki](https://github.com/Efemache/Mercenaries-Farm-Bot/wiki)

For contact, open an [issue](https://github.com/Efemache/Mercenaries-Farm-Bot/issues)

For news, follow us on Twitter : [@MercenariesFarm](https://twitter.com/MercenariesFarm)

To discuss with the community, go to discord [Mercenaries Farm server](https://discord.gg/ePghxaUBEK)

## Dev progress
|               |  1920x1080 (windowed mode) |
| :------------ | :-------------:| 
|1. transition to Travel point selection | ✓|
|2. transition to Level/Bounty selection | ✓|
|3. transition between encounters | ✓ |
|4. choosing a treasure after passing a level | ✓|
|5. prioritize the mysterious stranger  | ✓|
|6. prioritize the spirit healer  | ✓|
|7. putting heroes on the board | ✓|
|8. searching for suitable opponents | ✓|
|9. choosing abilities :  | ✓|
|    * for each mercenary (using configuration in conf/combo.ini) | ✓|
|    * or the first abilities by default (if no configuration exists) | ✓|
|    * /!\ the bot doesn't recognize abilities like "Choose One"  | x|
|    * /!\ the bot can't point an ability to your mercs (like Healing)  | x|
|10. attacking opponents (if ability requires it) | ✓|
|11. collecting rewards for reaching the last level|  ✓|
|12. repeat from 1 point | ✓|
 
## Supported game language & resolution
|               |     English    |
| :------------ | :-------------:| 
|1920x1080 screen resolution (with HS in windowed mode)   |        ✅      |

## Battle limitation (will change in future releases)
* bot doesn't work with ability like "choose one" with 2 choices (ex: Malfurion, but works for Rexxar)
* bot doesn't work with ability which need to point to one of your mercenaries (ex: impossible to use healing with Xyrella)
* ~~bot doesn't use minions on board which are not a mercenary~~ ✓ (ok since 0.4.0 release)

## PvE system work preview (demo)
[![Watch the video](https://user-images.githubusercontent.com/56414438/156830161-924cf85c-64a2-4215-870d-d0d005d28adc.jpg)](https://youtu.be/ZQ3xCL9_4Yo)

## When the bot is running
* don't move the Hearthstone window
* don't put another window in front of Hearthstone
* don't touch your mouse (except if you want to bypass the bot)
* don't resize the Hearthstone window or change the resolution

## Installation
### Windows
* Install [Python 3.9](https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64-webinstall.exe) (/!\ select the "Add Python 3.9 to PATH" during installation) 
* Download and install AutoHotKey (AHK) : https://www.autohotkey.com/
* Download the project
* Edit your Hearthstone log.config file (C:\Users\YOURUSER\AppData\Local\Blizzard\Hearthstone\log.config) and add these lines :
[Zone]
LogLevel=1
FilePrinting=true
ConsolePrinting=false
ScreenPrinting=false
* Open settings.ini and set your [settings](https://github.com/Efemache/Mercenaries-Farm-bot/wiki/Settings) (/!\ don't forget to set "GameDir" to your Hearthstone directory)
* Start Hearthstone
* Create a group of mercenaries named "Botwork" (and go back to main menu)
* Run HSbotRunner.bat


### Linux
* Install gir1.2-wnck-3.0 (sudo apt install gir1.2-wnck-3.0)
* Download the project
* Open settings.ini and set your [settings](https://github.com/Efemache/Mercenaries-Farm-bot/wiki/Settings) (/!\ don't forget to set "GameDir" to your Hearthstone directory)
* Edit your Hearthstone log.config file ([...]/drive_c/users/YOURUSER/Local Settings/Application Data/Blizzard/Hearthstone/log.config) and add these lines :
[Zone]
LogLevel=1
FilePrinting=true
ConsolePrinting=false
ScreenPrinting=false
* Start Hearthstone
* Create a group of mercenaries named "Botwork" (and go back to main menu)
* Run HSbotRunner.sh

### Python Installation
(removed due to google reference problem; I'll post a new video later)

