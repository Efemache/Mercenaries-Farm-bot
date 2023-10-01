# Mercenaries Farm Bot (for Hearthstone)
MFB official URL : https://github.com/Efemache/Mercenaries-Farm-bot/


> [!WARNING]  
> Blizzard pushed the last major update for Mercenary mode (February 14, 2023) and it was well supported by MFB (even in community version) until April, 2023.  
> So I decided to no longer maintain it (no more update).  
> At the end of May, Blizzard pushed an Hearthstone update which doesn't work anymore with this bot.  


# Purpose
The purpose of this bot is to automatically pass the bounty levels to level up your mercenaries, win somes coins and complete campfire tasks.

There is a [```main```](https://github.com/Efemache/Mercenaries-Farm-bot) branch to use daily.  
Tags are not used anymore; instead, download and use main branch.

> [!NOTE]  
> Up to "March of the Lich King" expansion (and Mini-set "Returns to Naxxramas") release, MFB works to complete a lot of campfire tasks and somes bounties.  


# PvE preview (video)
[![Watch the video](https://user-images.githubusercontent.com/56414438/156830161-924cf85c-64a2-4215-870d-d0d005d28adc.jpg)](https://youtu.be/ZQ3xCL9_4Yo)


# Installation
## When the bot is running
* don't move the Hearthstone window
* don't put another window in front of Hearthstone
* don't touch your mouse (except if you want to bypass the bot)
* don't resize the Hearthstone window or change the resolution


## Windows
* Install [Python 3.11](https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64-webinstall.exe) (⚠️ select the "Add Python 3.11 to PATH" during installation) 
* Download the project
* Open conf/user/settings.ini and set your [settings](https://github.com/Efemache/Mercenaries-Farm-bot/tree/main/doc/settings.md#settingsini-confusersettingsini) (⚠️ don't forget to set "GameDir" to your Hearthstone directory)
* Edit your Hearthstone [log.config file](https://github.com/Efemache/Mercenaries-Farm-bot/tree/main/doc/settings.md#logconfig)
* Start Hearthstone (with same resolution as set in settings.ini)
* Create a group of mercenaries named "Botwork" (and go back to main menu)
* Run HSbotRunner.bat


## Linux
* Install python3-venv (`sudo apt install python3.11-venv`)
* Install gir1.2-wnck-3.0 (`sudo apt install gir1.2-wnck-3.0`)
* Install - if needed - libharfbuzz-gobject0 (`sudo apt install libharfbuzz-gobject0`)
* Download the project
* Open conf/user/settings.ini and set your [settings](https://github.com/Efemache/Mercenaries-Farm-bot/tree/main/doc/settings.md#settingsini-confusersettingsini) (⚠️ don't forget to set "GameDir" to your Hearthstone directory)
* Edit your Hearthstone [log.config file](https://github.com/Efemache/Mercenaries-Farm-bot/tree/main/doc/settings.md#logconfig)
* Start Hearthstone (with same resolution as set in settings.ini)
* Create a group of mercenaries named "Botwork" (and go back to main menu)
* Run HSbotRunner.sh


## Bot Installation/Configuration Video
[![Watch the video](https://user-images.githubusercontent.com/56414438/190275041-fb8933ce-cee1-4257-ab06-fdd0419c9ad6.png)](https://youtu.be/Nh73f-YXUjg)


# News & contact 
No more news!

For videos (news, settings, ...), watch on YouTube (no new video) : [MercenariesFarm Channel](https://www.youtube.com/channel/UCye37bX5PJnPgChWvzjTqKg)

If you have any issue with the bot, please, read first the [FAQ (Frequently Asked Questions)](https://github.com/Efemache/Mercenaries-Farm-bot/tree/main/doc/FAQ.md).

~~For bugs, open an [issue](https://github.com/Efemache/Mercenaries-Farm-Bot/issues)~~

~~To discuss with the community, go to discord : [Mercenaries Farm server](https://discord.gg/ePghxaUBEK) (⚠️ don't ask in private message)~~


# Dev progress

## Language & resolution
⚠️ 1920x1080 is the only resolution "officially supported" (meaning, I can only test this resolution) but the other mentionned resolutions work too

⚠️ windowed : monitor needs to have a higher resolution than Hearthstone for both width AND height

| Resolution | English |
| :------------------- | :-------------:|
| 1920x1080 fullscreen <sup>1</sup> |        ✅      |
| 1920x1080 windowed  |        ✅      |
|  16:9 fullscreen  <sup>1</sup> <sup>2</sup> |        ✅      |
|  16:9 windowed  <sup>2</sup> |        ✅      |

(1)
* *for fullscreen mode, Hearthstone resolution and screen resolution need to be the same (example : 1920x1080 for both)*

(2)
* *16:9 resolution should work if at least 960x540 (960x540, 1024x576, 1280x720, 1600x900, ...)*
* *higher (than 1920x1080) 16:9 resolution has been tested with 2560x1440*

## Support
|                                        |   |
| :------------------------------------- | :-------------:|
|0. start from Battle.net | 1080 screen res. |
|1. transition to Travel point selection | ✓|
|    * new travel point portal | ✓|
|    * Boss Rush support | x|
|2. transition to Level/Bounty selection | ✓|
|3. transition between encounters | ✓|
|4. prioritize the spirit healer  | ✓|
|5. prioritize the mysterious node | ✓|
|6. put mercs on board | ✓|
|7. search for suitable opponents | ✓|
|8. choose abilities :  | ✓|
|    * for each mercenary (using [combo.ini](https://github.com/Efemache/Mercenaries-Farm-bot/tree/main/doc/settings.md#comboini-confusercomboini) files) | ✓|
|    * or the first abilities by default (if no configuration exists) | ✓|
|    * ability targetting friendly minion selected by Type, Faction or by Name| ✓|
|    * taunt, stealth, divine shield, attack, health, ... detection | x|
|9. attack opponents (if ability requires it) | ✓|
|10. choose a treasure after passing a level | ✓|
|11. collect rewards for reaching the last level|  ✓|
|12. claim packs, coins and equipments from completed tasks | ✓|
|13. repeat from 1 point | ✓|

## AI
### Battles
MFB uses a simple AI which can be described as : 
* Red (Protector) > Green (Fighter) > Blue (Caster) > Red (Protector)
* It doesn't know about taunt, devine shield, stealth, attack, health, ...

## Battle limitation (will change in future releases)
* ~~bot doesn't work with ability like "choose one" with 2 choices (ex: Malfurion, but works for Rexxar)~~ ✓ (ok since May 23, 2022)
* ~~bot doesn't work with ability which need to point to one of your mercenaries (ex: impossible to use healing with Xyrella)~~ ✓ (ok since May 23, 2022)
  * ~~bot doesn't work with ability targeting a specific type of mercenary like Dragon, Beast, ...~~ ✓ (ok since Jul. 08, 2022)
* ~~bot doesn't use minions on board which are not a mercenary~~ ✓ (ok since 0.4.0 release) / Feb. 18, 2022
* ~~MFB can't target a specific Mercenary by name~~ ✓ (ok since Feb. 06, 2023)
* MFB can't target a friendly minion/merc with an ability which, usually, point to an enemy


