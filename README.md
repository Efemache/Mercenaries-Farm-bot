# Mercenaries-Farm-Bot for Hearthstone
MFB official URL : https://github.com/Efemache/Mercenaries-Farm-bot/
```diff
Bot is on a development stage but it already works to do some "Tasks" and run low level bounties
```
## Purpose
The purpose of this bot is to automatically pass the bounty levels to level up your heros, win somes coins and complete campfire tasks.

There is a branch [```main```](https://github.com/Efemache/Mercenaries-Farm-bot) to use daily and a branch [```dev2```](https://github.com/Efemache/Mercenaries-Farm-bot/tree/dev2) with new features but not well tested (and can be broke somtimes).

If you only want a version working with the last Hearthstone patch, I recommend to use the [last tagged version](https://github.com/Efemache/Mercenaries-Farm-bot/tags).


## News & contact 
More informations in [Wiki](https://github.com/Efemache/Mercenaries-Farm-Bot/wiki)

For contact, open an [issue](https://github.com/Efemache/Mercenaries-Farm-Bot/issues)

For news, follow us on Twitter : [@MercenariesFarm](https://twitter.com/MercenariesFarm)

For videos (news, settings, ...), subscribe to [YouTube MercenariesFarm Channel](https://www.youtube.com/channel/UCye37bX5PJnPgChWvzjTqKg)

To discuss with the community, go to discord [Mercenaries Farm server](https://discord.gg/ePghxaUBEK)

## To support us (if you want)

|    Platform    | Address | QR Code | 
| :------------ | :-------------:|  :-------------:|  
|    Patreon    | [mercenaries_farm](https://www.patreon.com/mercenaries_farm) | |
| Bitcoin (BTC) | 3L4MJh6JVrnHyDDrvrkZQNtUytYNjop18f | <img src="https://user-images.githubusercontent.com/56414438/162740117-eeebb1ef-2971-40d3-8e8f-a39fa51e8c6e.png" width="200" /> |
|Ethereum (ETH) | 0x6Db162daDe8385608867A3B19CF1465e0ed7c0e2 | <img src="https://user-images.githubusercontent.com/56414438/162740147-39c72409-94f3-4871-b9e5-a782ab9c2522.png" width="200" /> |
| Binance Smart Chain (BNB/BUSD/...) | 0x6Db162daDe8385608867A3B19CF1465e0ed7c0e2 | <img src="https://user-images.githubusercontent.com/56414438/162740147-39c72409-94f3-4871-b9e5-a782ab9c2522.png" width="200" /> | 
| Thank you | [Twitter](https://twitter.com/MercenariesFarm) [Youtube](https://www.youtube.com/channel/UCye37bX5PJnPgChWvzjTqKg) [Discord](https://discord.gg/ePghxaUBEK)| |


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
|    * ⚠️ the bot doesn't recognize abilities like "Choose One"  | x|
|    * ⚠️ the bot can't point an ability to your mercs (like Healing)  | x|
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
* Install [Python 3.9](https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64-webinstall.exe) (⚠️ select the "Add Python 3.9 to PATH" during installation) 
* ~~Download and install AutoHotKey (AHK) : https://www.autohotkey.com/~~ (Skip this step. We switched to win32gui)
* Download the project
* Open settings.ini and set your [settings](https://github.com/Efemache/Mercenaries-Farm-bot/wiki/Settings#settingsini) (⚠️ don't forget to set "GameDir" to your Hearthstone directory)
* Edit your Hearthstone [log.config file](https://github.com/Efemache/Mercenaries-Farm-bot/wiki/Settings#logconfig)
* Start Hearthstone
* Create a group of mercenaries named "Botwork" (and go back to main menu)
* Run HSbotRunner.bat


### Linux
* Install gir1.2-wnck-3.0 (sudo apt install gir1.2-wnck-3.0)
* Download the project
* Open settings.ini and set your [settings](https://github.com/Efemache/Mercenaries-Farm-bot/wiki/Settings#settingsini) (⚠️ don't forget to set "GameDir" to your Hearthstone directory)
* Edit your Hearthstone [log.config file](https://github.com/Efemache/Mercenaries-Farm-bot/wiki/Settings#logconfig)
* Start Hearthstone
* Create a group of mercenaries named "Botwork" (and go back to main menu)
* Run HSbotRunner.sh

### Python Installation
(removed due to google reference problem; I'll post a new video later)

### FAQ
A new [FAQ](https://github.com/Efemache/Mercenaries-Farm-bot/wiki/FAQ) is created and will be filled
