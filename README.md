# Hearthstone-Mercenaries-game-bot
```diff
- prevention: Bot is not ready and now on the development stage
```
<h3 align="center">Dev progress</h3>
<table>
  <tr>
    <td width=500vw>1920x1080</td>
  </tr>
  <tr>
    <td>
<ol>
<li>auto assembly of the group - ✓ </li>
<li>transition to Travel point selection - ✓</li>
<li>transition to Level/Bounty selection - ✓</li>
<li>transition between encounters - ✓ </li>
<li>choosing a treasure after passing a level - ✓</li> 
<li>putting heroes on the board - ✓</li>
<li>searching for suitable opponents - ✓</li>
<li>choosing abilities (the first one by default) - ✓</li>
<li>attacking opponents - ✓</li>
<li>collecting rewards for reaching the last level-  ✓</li>
<li>repeat from 1 point - ✓</li>
</ol>
    </td>
  </tr>
 </table>
 
 <h3 align="center">Supported game language</h3>
<table>
  <tr>
     <td width=300vw>English</td>
  </tr>
  <tr>
    <td>
      1920x1080
    </td>
    <td>
      ❌
    </td>
    <td>
      ✅
    </td>
    <td>
      In progress
    </td>
  </tr>
 </table>

<h3 align="center">PvP system work preview</h3>

<br>
[![Watch the video](https://user-images.githubusercontent.com/68296704/137970053-fe49c896-d237-49f1-8658-46d1477340d7.png)](https://www.youtube.com/watch?v=znt1P3KkrNg&t)


<br>
The main idea of  the bot is to automatically pass the levels for simultaneously pumping all your mercenaries level 1 to 30.
<br>

More information on <a href="https://github.com/Efemache/Mercenaries-Hearthstone-game-bot/wiki">wiki</a>

<br>

<h1 align="center">Installation</h1>
<h2 align="center">Warning</h1>
This a project is a fork of a previous one. So the branch "main" & "ForDeveloment" are the orginals ones (with some commits/code from me).
<br>
To use the new code, you need to use the "<href="https://github.com/Efemache/Mercenaries-Hearthstone-game-bot/tree/improve2">improve2</a>" branch  
<h2 align="center">Windows</h1>
<ul>
  <li>Download and install AutoHotKey (AHK) : https://www.autohotkey.com/</li>
  <li>Download the project</li>
  <li>Open Settings.ini and set your settings</li>
  <li>Start Hearthstone</li>
</ul>

![image](https://user-images.githubusercontent.com/68296704/138607261-d743018d-4c50-4482-a4e7-81091cb0f963.png)

<ul>
  <li>Start the game</li>
</ul>

<h2 align="center">Linux</h1>
<ul>
  <li>Install gir1.2-wnck-3.0 (sudo apt install gir1.2-wnck-3.0)</li>
  <li>Download the project</li>
  <li>Open Settings.ini and set your settings</li>
  <li>Start Hearthstone</li>
  <li>Run HSbotRunner.sh</li>

<br>
<h2 align="center">Demo</h1>
[![Watch the video](https://user-images.githubusercontent.com/68296704/138687982-0f6d971d-783d-4f35-a3a5-4f5d5a3e59af.png)](https://www.youtube.com/watch?v=nOZXCkrQ5fk)






<h1 align="center">Specification, Settings.ini file:</h1>
<img align="right" src="https://user-images.githubusercontent.com/68296704/137707877-189b3ca6-9981-4db8-b60d-42168c4cea7d.png"></img>


```diff
[BotSettings]
monitor=1 
bot_speed=0.5 
+0.1-the fastest mode , 5-the slowest (not recomending do faster then 0.5) 
[Hero1]
number = 1
colour = Red
[Hero2]
number = 2
colour = Green
[Hero3]
number = 3
colour = Blue
+3 main heroes that you will use for pumping other ones.List of heroes by numbers you can see in in HeroesList.txt

[NumberOfPages]
Red = 1
Green = 2
Blue = 2
+number of pages each colour(or type) in section Red - defenders , Green - warriors ,Blue - Wizards
[Resolution]
Monitor Resolution = 2560*1440
+could be 2560*1440 or 1920*1080

```

<br>
<br>
<br>
    

HeroList<br>
1 - Cariel Roame <br>
2 - Tyrande <br>
3 - Milhous Manostorm <br>

For contact, open issue on the first repo : 
