# AutoAFK


> [!CAUTION]
> I have stopped playing AFK Arena so this project likely won't see any more updates, @Hamman is running a fork with bugfixes and new features etc here: https://github.com/Hammanek/AutoAFK

AutoAFK is a tool to automate AFK Arena tasks via ADB using Python, OpenCV and scrcpy. The bot uses image recognition with fuzzy matching, as well as single pixel recognition to automate actions. All actions are done through ADB which means the window does not need to be in focus (you don't even need a monitor attached) and you can continue to use your computer as normal while it runs.

While the bot is designed for AFK Arena the core logic will work for any Android program on an ABD enabled device.

![image](https://github.com/Fortigate/AutoAFK/assets/46250387/ba5608ae-d78f-4345-be6c-f8f7b2867de6)

Issues/Comments/Suggestions? Check out the #autoafk-help channel on the [AFK Arena Crowsource server](https://dsc.gg/cero-crowdsource)

# What does it do?
In the current release you can select from the following tasks:

## Dailies Tasks
* Collects AFK rewards
* Collects mail
* Send/Recieve companion points
* Dispatch mercs
* Collect Fast Rewards if available
* Start a Campaign battle
* Collect and Dispatch selected bounty resources
* Battle in the Arena of Heroes
* Collect Gladiator Coins
* Collect Fountain of Time rewards
* Collect Treasure Scramble rewards
* Start a King's Tower battle
* Run or sweep Arcane Labyrinth
* Collect daily gifts from the inn
* Battle Guild Hunts
* Battle Twisted Realm
* Make customizable daily store purchases
* Collect daily and weekly quest chests
* Clear Merchant menu free gifts & !'s

* As well as these it can handle the daily quests for Fight of Fates, Battle of Blood, Heroes of Esperia etc

## Activities selector
From the dropdown you can select these tasks and a number of battles to do:
* Arena of Heroes
* Battle of Blood
* Fight of Fates
* Heroes of Esperia
* Arcane Labyrinth (just the once)
 
## Auto push
You can select from campaign and the available towers that day. The bot then runs loads the formations and after victory reloads the formation for the next stage.


# How do I run it?
Configure your device so that:
* ADB is enabled
* Resolution is 1920x1080 (other 16:9 resolutions are technically supported but may cause issues)
* AFK's in-game language is set to English (I'd love to support other languages but all image files are taken from the English version)

Then download the latest [release](https://github.com/Fortigate/AutoAFK/releases), unzip and run AutoAFK.exe.

# Road map
The following features are broadly planned for some time in the future.
* Push Temporal Rift
* Discord notification on success/failure
* Purchase selected Dimensional Gear
* Run Misty Valley

# I'm having an issue
Note that the bot is currently in Beta and stability is still being worked into the functions. If you having issues please create an issue here or ask on the Discord server.
