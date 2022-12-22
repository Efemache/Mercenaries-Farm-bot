# Mercenaries Farm Bot (for Hearthstone)
MFB official URL : https://github.com/Efemache/Mercenaries-Farm-bot/

# Free & Tip: 2 ways starting 2022-11-07
<details><summary>Click here if you want some context</summary>

## Context
* I started to actively work on this bot (november 2021) because **I thought doing it open source, some devs would come** too to improve MFB so it would be a win/win
* Too few devs came (**big thanks to those who participated**) and they, generally, added a feature or two or fixed a bug but none staied on a long term or to globally help
* A lot of users asked for : features, doc update, videos, bugs fix (a lot of them didn't even impact me), help because they misconfigured MFB, help on their setup which wasn't even offically supported and I helped each time I could :
  * **Only 4 people made a donation**
  * A donation is like "Great job" or "Hey, you helped me, thanks, let me buy you a beer or a coffee" (especially when I spent 1 hour or more to help someone)
* Finally, it was way too much work for me "alone" and a lose/win for me

## In conclusion 
</details>

To continue to work on and maintain the bot : 
* MFB remains **free and open source** but updates will be **delivered 3-4 weeks later**
* For those who **help** (in coding) **and** those who **[give a tip](#if-you-want-to-support-or-thank-us) (at least 10$)**, updates will be **delivered 3-4 weeks before others**

 **Pull Request are still accepted**: if you have a bug or want a new feature, code it if you know how-to do it and send a PR.

> **Note**:  
> Look at the [changelog](https://ko-fi.com/mercenariesfarm/posts) to see what is already available in the supporters version and release dates for github.


# Purpose
The purpose of this bot is to automatically pass the bounty levels to level up your mercenaries, win somes coins and complete campfire tasks.

There is a [```main```](https://github.com/Efemache/Mercenaries-Farm-bot) branch to use daily. [```dev2```](https://github.com/Efemache/Mercenaries-Farm-bot/tree/dev2) branch is used for PR (Pull Request) only.

> **Note**:  
> Up to "Murder at Castle Nathria" expansion, MFB works to complete a lot of campfire tasks and somes bounties.

**If you like the bot, think about [giving a tip](#if-you-want-to-support-or-thank-us)**.


# PvE preview (video)
[![Watch the video](https://user-images.githubusercontent.com/56414438/156830161-924cf85c-64a2-4215-870d-d0d005d28adc.jpg)](https://youtu.be/ZQ3xCL9_4Yo)


# If you want to support (or thank) us
## Buy us a coffee, a beer or more 😄 
|    Platform           | Address |  
| :------------         | :-------------:|
|Ko-Fi       | [mercenariesfarm](https://ko-fi.com/mercenariesfarm) |


## Or send crypto

|    Platform           | Address | QR Code | 
| :------------         | :-------------:|  :-------------:|  
| Bitcoin (BTC)         | 3L4MJh6JVrnHyDDrvrkZQNtUytYNjop18f | <img src="https://user-images.githubusercontent.com/56414438/162740117-eeebb1ef-2971-40d3-8e8f-a39fa51e8c6e.png" alt="BTC" width="200" /> |
|Ethereum (ETH) or <br />Binance Smart Chain (BNB/BUSD) (*)| 0x6Db162daDe8385608867A3B19CF1465e0ed7c0e2 | <img src="https://user-images.githubusercontent.com/56414438/162740147-39c72409-94f3-4871-b9e5-a782ab9c2522.png" alt="ETH-BSC" width="200" /> |

 (\*) *yes, BSC and ETH addresses are the same*

 (\*) *on Ethereum blockchain you can send any ERC-20 token (let us know if you send token other than ETH)*

 (\*) *on BSC blockchain you can send any BEP-20 token (let us know if you send another token than BNB or BUSD)*


## Just a "Thanks"
|    Platform           | Address |
| :------------         | :-------------:|
| "Thank you"           | [<img src="https://user-images.githubusercontent.com/56414438/163575703-d249c687-1fd4-4c4d-b549-e27b01bb022b.png" alt="twitter" width="35rem">](https://twitter.com/MercenariesFarm) [<img src="https://user-images.githubusercontent.com/56414438/163575713-a5b96683-f788-4d48-b598-a838e7e97b8b.png" alt="youtube" width="35rem">](https://www.youtube.com/channel/UCye37bX5PJnPgChWvzjTqKg) [<img src="https://user-images.githubusercontent.com/56414438/163575692-c6d78ec2-ae37-46e9-84ca-fd650d3835c2.png" alt="discord" width="35rem">](https://discord.gg/ePghxaUBEK)| |

# Installation
## When the bot is running
* don't move the Hearthstone window
* don't put another window in front of Hearthstone
* don't touch your mouse (except if you want to bypass the bot)
* don't resize the Hearthstone window or change the resolution


## Windows
* Install [Python 3.10](https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64-webinstall.exe) (⚠️ select the "Add Python 3.10 to PATH" during installation) 
* Download the project
* Open conf/user/settings.ini and set your [settings](https://github.com/Efemache/Mercenaries-Farm-bot/wiki/Settings#settingsini-confusersettingsini) (⚠️ don't forget to set "GameDir" to your Hearthstone directory)
* Edit your Hearthstone [log.config file](https://github.com/Efemache/Mercenaries-Farm-bot/wiki/Settings#logconfig)
* Start Hearthstone (with same resolution as set in settings.ini)
* Create a group of mercenaries named "Botwork" (and go back to main menu)
* Run HSbotRunner.bat


## Linux
* Install gir1.2-wnck-3.0 (`sudo apt install gir1.2-wnck-3.0`)
* Install - if needed - libharfbuzz-gobject0 (`sudo apt install libharfbuzz-gobject0`)
* Download the project
* Open conf/user/settings.ini and set your [settings](https://github.com/Efemache/Mercenaries-Farm-bot/wiki/Settings#settingsini-confusersettingsini) (⚠️ don't forget to set "GameDir" to your Hearthstone directory)
* Edit your Hearthstone [log.config file](https://github.com/Efemache/Mercenaries-Farm-bot/wiki/Settings#logconfig)
* Start Hearthstone (with same resolution as set in settings.ini)
* Create a group of mercenaries named "Botwork" (and go back to main menu)
* Run HSbotRunner.sh


## Bot Installation/Configuration Video
[![Watch the video](https://user-images.githubusercontent.com/56414438/190275041-fb8933ce-cee1-4257-ab06-fdd0419c9ad6.png)](https://youtu.be/Nh73f-YXUjg)


# News & contact 
More informations in [Wiki](https://github.com/Efemache/Mercenaries-Farm-Bot/wiki)

For news, follow us on Twitter : [@MercenariesFarm](https://twitter.com/MercenariesFarm)

For videos (news, settings, ...), subscribe on YouTube : [MercenariesFarm Channel](https://www.youtube.com/channel/UCye37bX5PJnPgChWvzjTqKg)

If you have any issue with the bot, please, read first the [FAQ (Frequently Asked Questions)](https://github.com/Efemache/Mercenaries-Farm-bot/wiki/FAQ) before posting any question on discord or opening an issue on Github.

For bugs, open an [issue](https://github.com/Efemache/Mercenaries-Farm-Bot/issues)

To discuss with the community, go to discord : [Mercenaries Farm server](https://discord.gg/ePghxaUBEK) (⚠️ don't ask in private message)


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
|1. transition to Travel point selection | ✓|
|2. transition to Level/Bounty selection | ✓|
|3. transition between encounters | ✓ |
|4. prioritize the mysterious node | ✓|
|    * Bonus Treasure | ✓|
|    * Cursed Treasure | ✓|
|5. prioritize the spirit healer  | ✓|
|6. put mercs on board | ✓|
|7. search for suitable opponents | ✓|
|8. choose abilities :  | ✓|
|    * for each mercenary (using [combo.ini](https://github.com/Efemache/Mercenaries-Farm-bot/wiki/Settings#comboini-confusercomboini) files) | ✓|
|    * or the first abilities by default (if no configuration exists) | ✓|
|    * ⚠️ the bot can't point an ability to a specific mercenary  by name | x|
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
* MFB can't target a specific Mercenary by name
* MFB can't target a friendly minion/merc with an ability which, usually, point to an enemy


