# AutoAFK
A Python based tool to automate Bluestacks games via ADB using Python and OpenCV. The bot supports image recognition with fuzzy matching, as well as pixel recognition to automate actions. While the bot is designed for AFK Arena the core logic will work for anything rendered in Bluestacks.

Issues/Comments/Suggestions? [Join the Discord server!](https://discord.gg/pfU7UB5A)

# What is it?
AutoAFK is a proof of concept platform to automate tasks in AFK Arena. All actions are done through ADB which 
means the window does not need to be in focus and you can continue to use your computer as normal while it runs.

# What does it do?
The current Alpha version will run the absolute minimum in order to complete the dailies quests:
* Collect AFK rewards twice
* Collect mail if there is a notification !
* Send/Recieve companion points if there is a notification !
* Collect Fast Rewards if available (The amount of times can be configured)
* Load and exit a campaign battle
* Collect and optionally dispatch bounty quests
* Load and battle in the Arena of Heroes (Amount of times configurable)
* Load and exit a tower battle
* Collect daily gifts from the inn
* Auto battle available Guild Hunts
* Collect available daily and weekly quest chests

# How do I run it?
Make sure that your Bluestacks is running in 1920x1080 and 240DPI

Download the release and run AutoAFK.exe.

# I'm having an issue
Note that the bot is currently in Alpha and stability is still being worked into the functions. If you are receiving ADB errors you may need to manually connect your device using `./adb.exe connect localhost:xxxx` where xxxx is the port listed in Bluestacks ADB settings
