# Configuration 
## how-to choose travelpoint/bounty/level ?

You need to configure your [conf/user/settings.ini](https://github.com/Efemache/Mercenaries-Farm-bot/tree/main/doc/settings.md#settingsini)


## how-to configure mercenaries attacks ?

You need to edit your [conf/user/combo.ini](https://github.com/Efemache/Mercenaries-Farm-bot/tree/main/doc/settings.md#comboini)

## how-to change the group's name (default: Botwork) ?

Create your own screenshot (in-game, on "Choose a Party" screen) and put it in MFB directory, `conf/user/<resolution>/buttons/group_name.png`

The file has to be similar to `files/1920x1080/buttons/group_name.png`

# Starting the bot
## SetForegroundWindow error
There is another foregroung window from another process (like Window Menu launched with the "windows" key on keyboard).

## cp949 error
You're probably using a Korean Windows. Look at the solution in the issue [#154](https://github.com/Efemache/Mercenaries-Farm-bot/issues/154#issuecomment-1310417583) to solve this.


## AHK Not Installed
It's not a problem. AHK was used in previous versions and we keep it for our firsts users.

For new Windows users, MFB installs win32gui.


## error message "'pip' is not recognized as an internal or external command, operable program or batch file."

During Python installation, you need to select "Add Python [...] to PATH" as you can see below.
![Python Add PATH](https://user-images.githubusercontent.com/56414438/159332697-ed9249b2-ee82-442f-9c58-6bd72da4244f.png)

It's better to disable the long path limitation too.

## error : Settings file is missing section 'BotSettings'

Copy the
`conf/user/settings.sample.ini` into 
`conf/user/settings.ini`


Read the [settings doc page](https://github.com/Efemache/Mercenaries-Farm-bot/tree/main/doc/settings.md#settingsini) to configure user parameters and don’t forget to set the mandatory settings.


## the mouse pointer doesn't move at all (Windows)
Not an ideal solution but try to start the .bat as Admin (it works for some users).  
If it throws an error like [`No such file or directory`](https://github.com/Efemache/Mercenaries-Farm-bot/tree/main/doc/FAQ.md#no-such-file-or-directory), read the [Start as Admin](https://github.com/Efemache/Mercenaries-Farm-bot/tree/main/doc/FAQ.md#start-as-admin) section.

## No such file or directory
```
C:\Windows\system32>py -3.10 m pip install -r requirements_win.txt
ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements_win.txt'

C:\Windows\system32>py -3.10 main.py
C:\Users\user\AppData\Local\Programs\Python\Python310\python.exe: can't open file 'C:\Windows\system32\main.py': [Errno 2] No such file or directory
```
You probably started the bot as Admin. Try to start it as a regular user.  
If it doesn't work as regular user, read the section to [start it as Admin](https://github.com/Efemache/Mercenaries-Farm-bot/tree/main/doc/FAQ.md#start-as-admin)

## Start as Admin
[Start CMD as admin](https://grok.lsu.edu/article.aspx?articleid=18026&printable=y).  
In the Command Prompt: type `C:` if you installed MFB in "C:" (or use the correct drive letter if you installed it somewhere else)  
If you're in "C:\WINDOWS\system32", type `cd ..\..`  
*You need to be at the root of your drive ("C:" or "D:" or "E:" ...)*  
Go to MFB directory typing `cd \my\path\to\Mercenaries-Farm-Bot\` (replace **\\my\\path\\to\\Mercenaries-Farm-Bot\\** with your directory)  
Start the .bat from there (in the Command Prompt)

## the bot doesn't click on "mercenary" menu (or on "Play" button or on bounty or level or ...)
Only English lang (in Hearthstone) and 16:9 resolution are supported.

The bot uses images (in `files/<resolution>/` directory) to find where to click in Hearthstone window. The sizes of your hearthstone screen need to be quite similar.

If there is too much differences, the bot won't find where to click. That's why you need to have : 
- Hearthstone in fullscreen, with the same resolution than your screen/monitor

or
- Hearthstone in windowed mode, with a higher screen/monitor resolution (>HS_width x >HS_height)

# During Battle
## Mercenaries don't attack
*\<GameDir\>/Logs/Zone.log* (Heartsthone log file) is probably not filled during battle.

Read [these instructions](https://github.com/Efemache/Mercenaries-Farm-bot/tree/main/doc/settings.md#logconfig) and if it doesn’t work, follow instructions in issue [#146](https://github.com/Efemache/Mercenaries-Farm-bot/issues/146)

## Mercenaries use first ability (or default ability in conf/system/combo.ini). Combo.ini (combo settings) doesn't work

Your combo files (in `conf/user`) is probably named `combo.ini.ini` instead of `combo.ini`.  You can confirm it by right-clicking on the file and going into "Properties".  
It's because Windows hide your extension (the last 3 letters).

To solve this problem, 2 solutions: 
* delete the last .ini (to only see "combo"), as Windows is hiding extension, your file will be named `combo.ini`
* delete your file and use `combo.sample` file just by removing the `.sample` part in the name

# Features
## Stop / Pause MFB
[**For Supporters**](https://ko-fi.com/mercenariesfarm/posts), you can put the mouse in a corner of the screen.  
Next time the bot will try to move the mouse, it will be paused. You'll easily see how-to resume :)

OR  

**Windows**: you can alt+tab and then quickly ctrl+pause/break or ctrl+c to stop it

**Linux**: ctrl+z to pause (use `%1` to resume) or ctrl+c to stop it
## Season Pass / Reward Track
Yes, this feature is already available; the bot can wait to maximize XP earning.

Read info in [settings.ini](https://github.com/Efemache/Mercenaries-Farm-bot/tree/main/doc/settings.md#botsettings-section)


# Dev 
## How-to participate
1) Fork the repo on GitHub and create a branch based on `dev2` branch
2) Push to your own repo on Github (in your new branch)
3) Make a "Pull Request" in `dev2` => you'll find easily how-to do it on your repo (Github shows you a diff with the original repo and propose to make a PR)
4) I read and accept your code (in `dev2`)
5) After some testing (with others code), and when the bot is stable enough, I push to `main`
