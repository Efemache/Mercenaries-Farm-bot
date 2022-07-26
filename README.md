# Mercenaries Farm Bot (for Hearthstone)
MFB official URL : https://github.com/Efemache/Mercenaries-Farm-bot/
```
Bot is on a development stage but it already works to complete a lot of "Tasks" and some bounties.
```

## Purpose
The purpose of this bot is to automatically pass the bounty levels to level up your mercenaries, win somes coins and complete campfire tasks.

There is a [```main```](https://github.com/Efemache/Mercenaries-Farm-bot) branch to use daily and a [```dev2```](https://github.com/Efemache/Mercenaries-Farm-bot/tree/dev2) branch with new features but not well tested (and can be broke sometimes).

If you only want a version working with the last Hearthstone patch, and are not interested in new feature, I recommend to use the [last tagged version](https://github.com/Efemache/Mercenaries-Farm-bot/tags).


## PvE preview (video)
[![Watch the video](https://user-images.githubusercontent.com/56414438/156830161-924cf85c-64a2-4215-870d-d0d005d28adc.jpg)](https://youtu.be/ZQ3xCL9_4Yo)


## If you want to support (or thank) us
|    Platform    | Address | QR Code | 
| :------------ | :-------------:|  :-------------:|  
|    Patreon    | [mercenaries_farm](https://www.patreon.com/mercenaries_farm) | |
|     Ko-Fi     | [mercenariesfarm](https://ko-fi.com/mercenariesfarm) | |
| Bitcoin (BTC) | 3L4MJh6JVrnHyDDrvrkZQNtUytYNjop18f | <img src="https://user-images.githubusercontent.com/56414438/162740117-eeebb1ef-2971-40d3-8e8f-a39fa51e8c6e.png" alt="BTC" width="200" /> |
|Ethereum (ETH) or <br />Binance Smart Chain (BNB/BUSD)| 0x6Db162daDe8385608867A3B19CF1465e0ed7c0e2 | <img src="https://user-images.githubusercontent.com/56414438/162740147-39c72409-94f3-4871-b9e5-a782ab9c2522.png" alt="ETH-BSC" width="200" /> |
| "Thank you" | [<img src="https://user-images.githubusercontent.com/56414438/163575703-d249c687-1fd4-4c4d-b549-e27b01bb022b.png" alt="twitter" width="35rem">](https://twitter.com/MercenariesFarm) [<img src="https://user-images.githubusercontent.com/56414438/163575713-a5b96683-f788-4d48-b598-a838e7e97b8b.png" alt="youtube" width="35rem">](https://www.youtube.com/channel/UCye37bX5PJnPgChWvzjTqKg) [<img src="https://user-images.githubusercontent.com/56414438/163575692-c6d78ec2-ae37-46e9-84ca-fd650d3835c2.png" alt="discord" width="35rem">](https://discord.gg/ePghxaUBEK)| |

 (\*) yes, BSC and ETH addresses are the same

 (\*) on Ethereum blockchain you can send any ERC-20 token (let us know if you send token other than ETH)

 (\*) on BSC blockchain you can send any BEP-20 token (let us know if you send another token than BNB or BUSD)


## Installation
### When the bot is running
* don't move the Hearthstone window
* don't put another window in front of Hearthstone
* don't touch your mouse (except if you want to bypass the bot)
* don't resize the Hearthstone window or change the resolution


### Windows
* Install [Python 3.9](https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64-webinstall.exe) (⚠️ select the "Add Python 3.9 to PATH" during installation) 
* Download the project
* Open settings.ini and set your [settings](https://github.com/Efemache/Mercenaries-Farm-bot/wiki/Settings#settingsini) (⚠️ don't forget to set "GameDir" to your Hearthstone directory)
* Edit your Hearthstone [log.config file](https://github.com/Efemache/Mercenaries-Farm-bot/wiki/Settings#logconfig)
* Start Hearthstone (in 1920x1080)
* Create a group of mercenaries named "Botwork" (and go back to main menu)
* Run HSbotRunner.bat


### Linux
* Install gir1.2-wnck-3.0 (sudo apt install gir1.2-wnck-3.0)
* Download the project
* Open settings.ini and set your [settings](https://github.com/Efemache/Mercenaries-Farm-bot/wiki/Settings#settingsini) (⚠️ don't forget to set "GameDir" to your Hearthstone directory)
* Edit your Hearthstone [log.config file](https://github.com/Efemache/Mercenaries-Farm-bot/wiki/Settings#logconfig)
* Start Hearthstone (in 1920x1080)
* Create a group of mercenaries named "Botwork" (and go back to main menu)
* Run HSbotRunner.sh


### Bot Installation/Configuration Video
[![Watch the video](https://user-images.githubusercontent.com/56414438/171742740-ef583e7a-e773-46f8-8baf-7100d84ced87.png)](https://youtu.be/azOptPolsIM)


## News & contact 
More informations in [Wiki](https://github.com/Efemache/Mercenaries-Farm-Bot/wiki)

For bugs, open an [issue](https://github.com/Efemache/Mercenaries-Farm-Bot/issues)

For news, follow us on Twitter : [@MercenariesFarm](https://twitter.com/MercenariesFarm)

For videos (news, settings, ...), subscribe on YouTube : [MercenariesFarm Channel](https://www.youtube.com/channel/UCye37bX5PJnPgChWvzjTqKg)

To discuss with the community, go to discord : [Mercenaries Farm server](https://discord.gg/ePghxaUBEK)

If you have an issue with the bot, please, read the [FAQ](https://github.com/Efemache/Mercenaries-Farm-bot/wiki/FAQ) before posting any question on discord.


## Dev progress
### Language & resolution supported
|               |     English    |
| :------------ | :-------------:|
|   1920x1080   |       ✅      |


### Support
|               |  1920x1080 |
| :------------ | :-------------:|
|1. transition to Travel point selection | ✓|
|2. transition to Level/Bounty selection | ✓|
|3. transition between encounters | ✓ |
|4. prioritize the mysterious stranger  | ✓|
|    * Cursed Treasure is not supported | x|
|5. prioritize the spirit healer  | ✓|
|6. put mercs on the board | ✓|
|7. search for suitable opponents | ✓|
|8. choose abilities :  | ✓|
|    * for each mercenary (using `combo.ini` files) | ✓|
|    * or the first abilities by default (if no configuration exists) | ✓|
|    * ⚠️ the bot can't point an ability to a specific mercenary  by name | x|
|9. attack opponents (if ability requires it) | ✓|
|10. choose a treasure after passing a level | ✓|
|11. collect rewards for reaching the last level|  ✓|
|12. claim packs, coins and equipments from completed tasks  | ✓|
|13. repeat from 1 point | ✓|


### Battle limitation (will change in future releases)
* ~~bot doesn't work with ability like "choose one" with 2 choices (ex: Malfurion, but works for Rexxar)~~ ✓ (ok since May 23, 2022)
* ~~bot doesn't work with ability which need to point to one of your mercenaries (ex: impossible to use healing with Xyrella)~~ ✓ (ok since May 23, 2022)
  * ~~bot doesn't work with ability targeting a specific type of mercenary like Dragon, Beast, ...~~ ✓ (ok since Jul. 08, 2022)
* ~~bot doesn't use minions on board which are not a mercenary~~ ✓ (ok since 0.4.0 release) / Feb. 18, 2022
* MFB can't target a specific Mercenary by name
* MFB can't target a friendly minion/merc with an ability which, usually, point to an enemy


