# Welcome to -= Hearthstone Mercenaries Farm bot =- Wiki

/!\ 2023 June - This bot is no longer maintain and shouldn't work with the last HS updates


## News

Find information about new features [on twitter](https://twitter.com/MercenariesFarm)

## Frequently Asked Question

Check the [FAQ](https://github.com/Efemache/Mercenaries-Farm-bot/tree/main/doc/FAQ.md) before posting any question.

## New bot/code

Use the [supporters version](https://github.com/Efemache/Mercenaries-Farm-bot#free--tip-2-ways-starting-2022-11-07) if you want the last feature, support and bufixes.  
Use branch [main](https://github.com/Efemache/Mercenaries-Farm-bot) daily if you want last well tested version opened to the HS community.  
Use branch [dev](https://github.com/Efemache/Mercenaries-Farm-bot/tree/dev2) if you want to send a PR.

## The bot is not ready for every pc but it works with limited support

* 16:9 resolution windowed (screen resolution need to be higher than HS resolution for width AND height) and fullscreen
* Linux and Windows (but I only can test on Linux)
* Language : only English (because there is some screenshots with Hearhtstone English text ~~but I'm working on a new version to support multi-languages~~)

## What I stopped to support

* groups creation

Why ? I don't have time to test it and I think it's easier for users to create a group in Hearthstone than to modify a setting.ini to put some heroes number AND this feature takes time to maintain ... so require time for no added value (to users).  
(and the Tavern - to manage your groups - is often bugged. It could be a nightmare to try to manage anything in here)

## Any help is welcome and needed. There is a lot of things to do

* tests (start bot with hearthstone and fill issues),
* code


Feel free to help !

## What I won't support

* PvP

Why ? Because it's just a bot to help you level-up your mercenaries and win coins, that's all.  
I won't work on something to beat other (real) players.


## What I'd like to implement (Bug / Feature / Improvement)

### Bugs to solve

- encounter : ~~there is some bugs~~ ~~there is one last bug when you met Mysterious Stranger just before the boss~~
- encounter : ~~wait when a completed task is shown or (sometimes) the bot get stuck~~
- battle : ~~there is some bugs when trying to find an enemy so the bot doesn't attack~~ ✓


### New features

- campfire : ~~configure the bot to do tasks in campfire (heroes coins/equipements reward)~~ ✓
- encounter : ~~prioritize to look for [Mysterious Stranger](https://cdn.hearthstonetopdecks.com/wp-content/uploads/2021/10/featured-mercenaries-mysterious-stranger.jpg)~~ ✓
- encounter : ~~avoid "legendary" battle because, most of the time, the bot will lose some mercenaries~~ ✓ (since july 23, 2022)
- encounter : ~~avoid "upgrades" (sometimes it helps the final Boss)~~  ✓ 
- battle : detect & attack taunt
- battle : ~~detect Mercenaries on board (actually it doesn't, it does it only for three and it's like hard coded. A lot of code are necessary to change it)~~ ✓
- battle : ~~better attacks selection (try to support all heroes) (need to use conf files, for each hero, instead of hard code)~~ ✓
- battle : better AI
- gui : 
    - stop/start/pause the bot
    - configure the bot (lang, resolution, travel point and level supported selection, ...)
- support : multi-language support (only need to load image in memory, add a "LANG=" in settings, and load image from "/files/LANG/....png" if it exists or "files/all/...png" if it don't) (better to use a lot of images without text)
- support : ~~multi-resolution. Potentially possible in memory to resize images (to avoid images in 3 resolutions)~~ ✓
- version : alert user if a new bot version exists
- version : alert user if a new Hearthstone version exists and we're not sure the bot will work with


### Improvement

- encounter : ~~try to find a battle ("Play" button) after each click on the map~~ ✓
- code : ~~continue to make the code easier to read and add comments. A lot of cleanup necessary in find_ellements(), abilicks(), rand(), battlefind(), battle(), ...~~ ✓
- ~~group : stop to use "page" configuration in settings.ini => only need to check the UI to detect if the page is for Protector, Fighter or Caster~~ (canceled)


