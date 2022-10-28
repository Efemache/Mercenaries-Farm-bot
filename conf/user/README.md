# Use your own mercenaries group name
In Hearthstone, go to the group selection screen ("Choose a Party") and take a screnshot of your mercenaries group name.

Name it "group_name.png", then put in in `conf/user/<resolution>/buttons/`.


# User Configuration
This folder is for your custom settings.

Rename the sample file into .ini file (you just hve to delete the `.sample` part) in this directory :
* settings.sample.ini -> settings.ini (for your bot settings)
* combo.sample.ini -> combo.ini (to manage your Mercenaries abilities during battle)

Edit the file matching the settings file you want to change and add just the settings you want to edit here.

Example with user/conf/combo.ini:
```ini
# conf/user/combo.ini
[Mercenary]
Chi-Ji=1,1,3
Baron Geddon=2
Ragnaros=2
```

This will override any existing values for those specific mercenaries in `conf/system/combo.ini` while keeping all the other values the same.
