# AutoAFK
AFK Arena Automation

# What is it?
AutoAFK is a proof of concept platform to automate tasks in AFK Arena running in BlueStacks, all actions are done through ADB which 
means the window does not need to be in focus and you can continue to use your computer as normal while it runs.

# What does it do?
The current version will run the absolute minimum in order to complete the dailies quests:
* collectAFKRewards
* collectMail
* collectCompanionPoints
* collectFastRewards
* attemptCampaign
* handleBounties
* handleArenaOfHeroes
* handleKingsTower
* collectInnGifts
* handleGuildHunts
* collectQuests

# How do I run it?
* Launch Bluestacks with ADB enabled
* Launch and connect ADB
* Edit the line "device = adb.device("localhost:5575")" in `tools.py` to the name of your connected device in ADB
* Run `main.py`
