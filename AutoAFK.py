from activities import *
from tools import *
import customtkinter
import threading
import sys
import configparser
import os
from datetime import datetime, timezone
import argparse
import requests

global settings

currenttime = datetime.now()
currenttimeutc = datetime.now(timezone.utc)
cwd = os.path.dirname(__file__) # We prefix all file calls with cwd so we can call from other directories (I.E via batch or cron)
config = configparser.ConfigParser()
customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", metavar="CONFIG", default = "settings.ini", help = "Define alternative settings file to load")
# parser.add_argument("-a", "--activity", metavar="ACTIVITY", help = "Define Activity")
# parser.add_argument("-p", "--push", metavar="PUSH", help = "Path to your input image")
parser.add_argument("-d", "--dailies", action = 'store_true', help = "Run the Dailies function")
parser.add_argument("-at", "--autotower", action = 'store_true', help = "Run the Auto-Towers function")
parser.add_argument("-tower", "--tower", choices=['lb', 'lightbringer', 'm', 'mauler', 'w', 'wilder', 'gb', 'graveborn', 'cele', 'celestial', 'hypo', 'hypogean', 'kt', 'kingstower'], help = "Select and run the given tower")
parser.add_argument("-t", "--test", action = 'store_true', help = "Auto-launch Test server")
parser.add_argument("-l", "--logging", action = 'store_true', help = "Log output to text file")
args = vars(parser.parse_args())

if args['config']:
    settings = os.path.join(cwd, args['config'])
else:
    settings = os.path.join(cwd, 'settings.ini')
config.read(settings)

repo_releases = requests.get('https://api.github.com/repos/Fortigate/AutoAFK/releases/latest')
json = repo_releases.json() if repo_releases and repo_releases.status_code == 200 else None
if json != None:
    latest_release = json.get('name')
else:
    latest_release = 'Cannot retrieve!'


version = "0.15.6"

#Main Window
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("AutoAFK " + version)
        self.geometry(f"{800}x{600}")
        self.wm_iconbitmap(os.path.join(cwd, 'img', 'auto.ico'))

        # Dailies Frame
        self.dailiesFrame = customtkinter.CTkFrame(master=self, height=170, width=180)
        self.dailiesFrame.place(x=10, y=20)

        # Dailies button
        self.dailiesButton = customtkinter.CTkButton(master=self.dailiesFrame, text="Run Dailies", command=lambda: threading.Thread(target=dailiesButton).start())
        self.dailiesButton.place(x=20, y=10)
        # Activities button
        self.activitiesButton = customtkinter.CTkButton(master=self.dailiesFrame, text="Configure Dailies", fg_color=["#3B8ED0", "#1F6AA5"], width=120, command=self.open_activitywindow)
        self.activitiesButton.place(x=30, y=50)
        # Shop button
        self.dailiesShopButton = customtkinter.CTkButton(master=self.dailiesFrame, text="Store Options", fg_color=["#3B8ED0", "#1F6AA5"], width=120, command=self.open_shopwindow)
        self.dailiesShopButton.place(x=30, y=90)
        # Advanced button
        self.advancedButton = customtkinter.CTkButton(master=self.dailiesFrame, text="Advanced Options", fg_color=["#3B8ED0", "#1F6AA5"], width=120, command=self.open_advancedwindow)
        self.advancedButton.place(x=30, y=130)

        # PvP Frame
        self.arenaFrame = customtkinter.CTkFrame(master=self, height=130, width=180)
        self.arenaFrame.place(x=10, y=200)

        # Activities button
        self.arenaButton = customtkinter.CTkButton(master=self.arenaFrame, text="Run Activity", command=lambda: threading.Thread(target=activityManager).start())
        self.arenaButton.place(x=20, y=15)
        # Activities Dropdown
        self.activityFormationDropdown = customtkinter.CTkComboBox(master=self.arenaFrame, values=["Arena of Heroes", "Arcane Labyrinth", "Fight of Fates", "Battle of Blood", "Heroes of Esperia"], width=160)
        self.activityFormationDropdown.place(x=10, y=55)
        # Activities Entry
        self.pvpLabel = customtkinter.CTkLabel(master=self.arenaFrame, text='How many battles', fg_color=("gray86", "gray17"))
        self.pvpLabel.place(x=10, y=90)
        self.pvpEntry = customtkinter.CTkEntry(master=self.arenaFrame, height=20, width=40)
        self.pvpEntry.insert('end', config.get('ACTIVITY', 'activitybattles'))
        self.pvpEntry.place(x=130, y=92)

        # Push Frame
        self.pushFrame = customtkinter.CTkFrame(master=self, height=180, width=180)
        self.pushFrame.place(x=10, y=340)

        # Push Button
        self.pushButton = customtkinter.CTkButton(master=self.pushFrame, text="Auto Push", command=lambda: threading.Thread(target=push).start())
        self.pushButton.place(x=20, y=10)
        # Push Entry
        self.pushLocationDropdown = customtkinter.CTkComboBox(master=self.pushFrame,  values=["Campaign"], width=160)
        self.pushLocationDropdown.place(x=10, y=50)
        # Push Formation
        self.pushLabel = customtkinter.CTkLabel(master=self.pushFrame, text='Which formation?', fg_color=("gray86", "gray17"))
        self.pushLabel.place(x=10, y=80)
        self.pushFormationDropdown = customtkinter.CTkComboBox(master=self.pushFrame, values=["1st", "2nd", "3rd", "4th", "5th"], width=80)
        self.pushFormationDropdown.set(config.get('PUSH', 'formation'))
        self.pushFormationDropdown.place(x=10, y=110)
        # Push Artifacts y/n
        self.useArtifactsLabel = customtkinter.CTkLabel(master=self.pushFrame, text='Copy Artifacts', fg_color=("gray86", "gray17"))
        self.useArtifactsLabel.place(x=10, y=145)
        self.useArtifactsCheckbox = customtkinter.CTkCheckBox(master=self.pushFrame, text=None, onvalue=True, offvalue=False, command=self.updateArtifacts)
        self.useArtifactsCheckbox.place(x=150, y=145)
        # Select useArtifacts button if enabled
        if config.getboolean('PUSH', 'useartifacts'):
            self.useArtifactsCheckbox.select()

        # Quit button
        self.quitButton = customtkinter.CTkButton(master=self, text="Close", fg_color=["#B60003", "#C03335"], width=180, command=lambda: threading.Thread(target=cleanExit).start())
        self.quitButton.place(x=10, y=550)

        def cleanExit():
            closeADB()
            self.destroy()

        # Textbox Frame
        self.textbox = customtkinter.CTkTextbox(master=self, width=580, height=560)
        self.textbox.place(x=200, y=20)
        self.textbox.configure(text_color='white', font=('Arial', 14))
        self.textbox.tag_config("error", foreground="red")
        self.textbox.tag_config('warning', foreground='yellow')
        self.textbox.tag_config('green', foreground='lawngreen')
        self.textbox.tag_config('blue', foreground='cyan')
        self.textbox.tag_config('purple', foreground='#af5ac9')
        self.textbox.tag_config('yellow', foreground='yellow')
        self.textbox.insert('end', 'Welcome to AutoAFK!\n', 'green')
        self.textbox.insert('end', 'Github: ', 'purple')
        self.textbox.insert('end',  'Github.com/Fortigate/AutoAFK/\n')
        self.textbox.insert('end', 'Discord DM: ', 'purple')
        self.textbox.insert('end',  'Jc.2\n')
        self.textbox.insert('end', 'Discord Server: ', 'purple')
        self.textbox.insert('end',  'dsc.gg/cero-crowdsource in #autoafk-help\n\n')
        if latest_release.split(' ')[1] != version and latest_release.split(' ')[1] != 'retrieve!':
            if not version.split('.')[1] >= latest_release.split('.')[1]: # If minor version is above release don't display (suppress for pre-releases generally)
                self.textbox.insert('end', 'Newer version available (' + latest_release.split(' ')[1] + '), please update!\n\n', 'yellow')
        if (args['config']) != 'settings.ini':
            self.textbox.insert('end', (args['config']) + ' loaded\n\n', 'yellow')
        if not args['dailies']:
            sys.stdout = STDOutRedirector(self.textbox)

        # Configure windows so we can reference them
        self.shop_window = None
        self.activity_window = None
        self.advanced_window = None
        self.summons_window = None

    # For updating the artifact setting when the checkbox is selected/unselected
    def updateArtifacts(self):
        if self.useArtifactsCheckbox.get() == 1:
            config.set('PUSH', 'useartifacts', 'True')
        else:
            config.set('PUSH', 'useartifacts', 'False')
        updateSettings()

    def open_advancedwindow(self):
        if self.advanced_window is None or not self.advanced_window.winfo_exists():
            self.advanced_window = advancedWindow(self)  # create window if its None or destroyed
            self.advanced_window.focus()
        else:
            self.advanced_window.focus()  # if window exists focus it

    def open_shopwindow(self):
        if self.shop_window is None or not self.shop_window.winfo_exists():
            self.shop_window = shopWindow(self)  # create window if its None or destroyed
            self.shop_window.focus()
        else:
            self.shop_window.focus()  # if window exists focus it

    def open_activitywindow(self):
        if self.activity_window is None or not self.activity_window.winfo_exists():
            self.activity_window = activityWindow(self)  # create window if its None or destroyed
            self.activity_window.focus()
        else:
            self.activity_window.focus()  # if window exists focus it

# Shop Window
class activityWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("745x560")
        self.title('Dailies Configuration')
        self.attributes("-topmost", True)

        # Activity Frame
        self.activityFrame = customtkinter.CTkFrame(master=self, width=235, height=500)
        self.activityFrame.place(x=10, y=10)
        self.label = customtkinter.CTkLabel(master=self.activityFrame, text="Activities:", font=("Arial", 15, 'bold', 'underline'))
        self.label.place(x=20, y=5)

        # Campaign Screen
        # AFK Rewards Collect
        self.collectRewardsLabel = customtkinter.CTkLabel(master=self.activityFrame, text='Collect AFK Rewards', fg_color=("gray86", "gray17"))
        self.collectRewardsLabel.place(x=10, y=40)
        self.collectRewardsCheckbox = customtkinter.CTkCheckBox(master=self.activityFrame, text=None, onvalue=True, offvalue=False, command=self.activityUpdate)
        self.collectRewardsCheckbox.place(x=200, y=40)
        # Mail Collect
        self.collectMailLabel = customtkinter.CTkLabel(master=self.activityFrame, text='Collect Mail', fg_color=("gray86", "gray17"))
        self.collectMailLabel.place(x=10, y=70)
        self.collectMailCheckbox = customtkinter.CTkCheckBox(master=self.activityFrame, text=None, onvalue=True, offvalue=False, command=self.activityUpdate)
        self.collectMailCheckbox.place(x=200, y=70)
        # Companion Points Collect
        self.companionPointsLabel = customtkinter.CTkLabel(master=self.activityFrame, text='Send/Receive Companion Points', fg_color=("gray86", "gray17"))
        self.companionPointsLabel.place(x=10, y=100)
        self.companionPointsCheckbox = customtkinter.CTkCheckBox(master=self.activityFrame, text=None, onvalue=True, offvalue=False, command=self.activityUpdate)
        self.companionPointsCheckbox.place(x=200, y=100)
        # Send Mercs
        self.lendMercsLabel = customtkinter.CTkLabel(master=self.activityFrame, text='Auto lend mercs?', fg_color=("gray86", "gray17"))
        self.lendMercsLabel.place(x=40, y=130)
        self.lendMercsCheckbox = customtkinter.CTkCheckBox(master=self.activityFrame, text=None, onvalue=True, offvalue=False, command=self.activityUpdate)
        self.lendMercsCheckbox.place(x=200, y=130)
        # Fast Rewards
        self.fastRewardsLabel = customtkinter.CTkLabel(master=self.activityFrame, text='Fast Rewards', fg_color=("gray86", "gray17"))
        self.fastRewardsLabel.place(x=10, y=160)
        self.fastrewardsEntry = customtkinter.CTkEntry(master=self.activityFrame, height=20, width=25)
        self.fastrewardsEntry.insert('end', config.get('DAILIES', 'fastrewards'))
        self.fastrewardsEntry.place(x=200, y=160)
        # Attempt Campaign battle
        self.attemptCampaignLabel = customtkinter.CTkLabel(master=self.activityFrame, text='Attempt Campaign', fg_color=("gray86", "gray17"))
        self.attemptCampaignLabel.place(x=10, y=190)
        self.attemptCampaignCheckbox = customtkinter.CTkCheckBox(master=self.activityFrame, text=None, onvalue=True, offvalue=False, command=self.activityUpdate)
        self.attemptCampaignCheckbox.place(x=200, y=190)

        # Spooky Forest
        # Fountain of Time
        self.fountainOfTimeLabel = customtkinter.CTkLabel(master=self.activityFrame, text='Collect Fountain of Time', fg_color=("gray86", "gray17"))
        self.fountainOfTimeLabel.place(x=10, y=220)
        self.fountainOfTimeCheckbox = customtkinter.CTkCheckBox(master=self.activityFrame, text=None, onvalue=True, offvalue=False, command=self.activityUpdate)
        self.fountainOfTimeCheckbox.place(x=200, y=220)
        # Kings Tower
        self.kingsTowerLabel = customtkinter.CTkLabel(master=self.activityFrame, text='Attempt King\'s Tower', fg_color=("gray86", "gray17"))
        self.kingsTowerLabel.place(x=10, y=250)
        self.kingsTowerCheckbox = customtkinter.CTkCheckBox(master=self.activityFrame, text=None, onvalue=True, offvalue=False, command=self.activityUpdate)
        self.kingsTowerCheckbox.place(x=200, y=250)
        # Collect Inn gifts
        self.collectInnLabel = customtkinter.CTkLabel(master=self.activityFrame, text='Collect Inn Gifts', fg_color=("gray86", "gray17"))
        self.collectInnLabel.place(x=10, y=280)
        self.collectInnCheckbox = customtkinter.CTkCheckBox(master=self.activityFrame, text=None, onvalue=True, offvalue=False, command=self.activityUpdate)
        self.collectInnCheckbox.place(x=200, y=280)
        # Battle Guild Hunts
        self.guildHuntLabel = customtkinter.CTkLabel(master=self.activityFrame, text='Battle Guild Hunts', fg_color=("gray86", "gray17"))
        self.guildHuntLabel.place(x=10, y=280)
        self.guildHuntCheckbox = customtkinter.CTkCheckBox(master=self.activityFrame, text=None, onvalue=True, offvalue=False, command=self.activityUpdate)
        self.guildHuntCheckbox.place(x=200, y=280)

        # Ranhorn + Lab
        # Store Purchases
        self.storePurchasesLabel = customtkinter.CTkLabel(master=self.activityFrame, text='Make Store Purchases', fg_color=("gray86", "gray17"))
        self.storePurchasesLabel.place(x=10, y=310)
        self.storePurchasesCheckbox = customtkinter.CTkCheckBox(master=self.activityFrame, text=None, onvalue=True, offvalue=False, command=self.activityUpdate)
        self.storePurchasesCheckbox.place(x=200, y=310)
        # Shop Refresh Amount
        self.shoprefreshLabel = customtkinter.CTkLabel(master=self.activityFrame, text='Store Refreshes', fg_color=("gray86", "gray17"))
        self.shoprefreshLabel.place(x=40, y=340)
        self.shoprefreshEntry = customtkinter.CTkEntry(master=self.activityFrame, height=20, width=25)
        self.shoprefreshEntry.insert('end', config.get('DAILIES', 'shoprefreshes'))
        self.shoprefreshEntry.place(x=200, y=340)
        # Twisted Realm
        self.twistedRealmLabel = customtkinter.CTkLabel(master=self.activityFrame, text='Attempt Twisted Realm', fg_color=("gray86", "gray17"))
        self.twistedRealmLabel.place(x=10, y=370)
        self.twistedRealmCheckbox = customtkinter.CTkCheckBox(master=self.activityFrame, text=None, onvalue=True, offvalue=False, command=self.activityUpdate)
        self.twistedRealmCheckbox.place(x=200, y=370)
        # Handle Lab
        self.runLabLabel = customtkinter.CTkLabel(master=self.activityFrame, text='Run Lab', fg_color=("gray86", "gray17"))
        self.runLabLabel.place(x=10, y=400)
        self.runLabCheckbox = customtkinter.CTkCheckBox(master=self.activityFrame, text=None, onvalue=True, offvalue=False, command=self.activityUpdate)
        self.runLabCheckbox.place(x=200, y=400)
        # Collect Quests
        self.collectQuestsLabel = customtkinter.CTkLabel(master=self.activityFrame, text='Collect Daily/Weekly Quests', fg_color=("gray86", "gray17"))
        self.collectQuestsLabel.place(x=10, y=430)
        self.collectQuestsCheckbox = customtkinter.CTkCheckBox(master=self.activityFrame, text=None, onvalue=True, offvalue=False, command=self.activityUpdate)
        self.collectQuestsCheckbox.place(x=200, y=430)
        # Collect Free Merchant Deals
        self.collectMerchantsLabel = customtkinter.CTkLabel(master=self.activityFrame, text='Collect Merchant Deals/Nobles', fg_color=("gray86", "gray17"))
        self.collectMerchantsLabel.place(x=10, y=460)
        self.collectMerchantsCheckbox = customtkinter.CTkCheckBox(master=self.activityFrame, text=None, onvalue=True, offvalue=False, command=self.activityUpdate)
        self.collectMerchantsCheckbox.place(x=200, y=460)


        # Arena Frame
        self.ArenaFrame = customtkinter.CTkFrame(master=self, width=235, height=280)
        self.ArenaFrame.place(x=255, y=10)
        self.label = customtkinter.CTkLabel(master=self.ArenaFrame, text="Arena:", font=("Arial", 15, 'bold'))
        self.label.place(x=10, y=5)

        # Battle Arena
        self.battleArenaLabel = customtkinter.CTkLabel(master=self.ArenaFrame, text='Battle Arena of Heroes', fg_color=("gray86", "gray17"))
        self.battleArenaLabel.place(x=10, y=40)
        self.battleArenaCheckbox = customtkinter.CTkCheckBox(master=self.ArenaFrame, text=None, onvalue=True, offvalue=False, command=self.activityUpdate)
        self.battleArenaCheckbox.place(x=200, y=40)
        # Arena Battles
        self.arenaBattlesLabel = customtkinter.CTkLabel(master=self.ArenaFrame, text='Number of Battles', fg_color=("gray86", "gray17"))
        self.arenaBattlesLabel.place(x=40, y=70)
        self.arenaBattlesEntry = customtkinter.CTkEntry(master=self.ArenaFrame, height=20, width=30)
        self.arenaBattlesEntry.insert('end', config.get('ARENA', 'arenabattles'))
        self.arenaBattlesEntry.place(x=198, y=70)
        # Arena Opponent
        self.arenaOpponentLabel = customtkinter.CTkLabel(master=self.ArenaFrame, text='Which Opponent', fg_color=("gray86", "gray17"))
        self.arenaOpponentLabel.place(x=40, y=100)
        self.arenaOpponentEntry = customtkinter.CTkEntry(master=self.ArenaFrame, height=20, width=25)
        self.arenaOpponentEntry.insert('end', config.get('ARENA', 'arenaopponent'))
        self.arenaOpponentEntry.place(x=198, y=100)
        # Collect Treasure Scramble Loot
        self.tsCollectLabel = customtkinter.CTkLabel(master=self.ArenaFrame, text='Collect Daily TS loot', fg_color=("gray86", "gray17"))
        self.tsCollectLabel.place(x=10, y=130)
        self.tsCollectCheckbox = customtkinter.CTkCheckBox(master=self.ArenaFrame, text=None, onvalue=True, offvalue=False, command=self.activityUpdate)
        self.tsCollectCheckbox.place(x=200, y=130)
        # Collect Gladiator Coins
        self.gladiatorCollectLabel = customtkinter.CTkLabel(master=self.ArenaFrame, text='Collect Gladiator Coins', fg_color=("gray86", "gray17"))
        self.gladiatorCollectLabel.place(x=10, y=160)
        self.gladiatorCollectCheckbox = customtkinter.CTkCheckBox(master=self.ArenaFrame, text=None, onvalue=True, offvalue=False, command=self.activityUpdate)
        self.gladiatorCollectCheckbox.place(x=200, y=160)

        # Events Frame
        self.eventsFrame = customtkinter.CTkFrame(master=self, width=235, height=210)
        self.eventsFrame.place(x=255, y=300)
        self.label = customtkinter.CTkLabel(master=self.eventsFrame, text="Events:", font=("Arial", 15, 'bold'))
        self.label.place(x=10, y=5)

        # Fight of Fates
        self.fightOfFatesLabel = customtkinter.CTkLabel(master=self.eventsFrame, text='Fight of Fates', fg_color=("gray86", "gray17"))
        self.fightOfFatesLabel.place(x=10, y=40)
        self.fightOfFatesCheckbox = customtkinter.CTkCheckBox(master=self.eventsFrame, text=None, onvalue=True, offvalue=False, command=self.activityUpdate)
        self.fightOfFatesCheckbox.place(x=200, y=40)
        # Battle of Blood
        self.battleOfBloodLabel = customtkinter.CTkLabel(master=self.eventsFrame, text='Battle of Blood', fg_color=("gray86", "gray17"))
        self.battleOfBloodLabel.place(x=10, y=70)
        self.battleOfBloodCheckbox = customtkinter.CTkCheckBox(master=self.eventsFrame, text=None, onvalue=True, offvalue=False, command=self.activityUpdate)
        self.battleOfBloodCheckbox.place(x=200, y=70)
        # Circus Tour
        self.circusTourLabel = customtkinter.CTkLabel(master=self.eventsFrame, text='Circus Tour', fg_color=("gray86", "gray17"))
        self.circusTourLabel.place(x=10, y=100)
        self.circusTourCheckbox = customtkinter.CTkCheckBox(master=self.eventsFrame, text=None, onvalue=True, offvalue=False, command=self.activityUpdate)
        self.circusTourCheckbox.place(x=200, y=100)
        # Heroes of Esperia
        self.heroesOfEsperiaLabel = customtkinter.CTkLabel(master=self.eventsFrame, text='Heoes of Esperia', fg_color=("gray86", "gray17"))
        self.heroesOfEsperiaLabel.place(x=10, y=130)
        self.heroesOfEsperiaCheckbox = customtkinter.CTkCheckBox(master=self.eventsFrame, text=None, onvalue=True, offvalue=False, command=self.activityUpdate)
        self.heroesOfEsperiaCheckbox.place(x=200, y=130)

        # Bounties Frame
        self.BountiesFrame = customtkinter.CTkFrame(master=self, width=235, height=280)
        self.BountiesFrame.place(x=500, y=10)
        self.label = customtkinter.CTkLabel(master=self.BountiesFrame, text="Bounties:", font=("Arial", 15, 'bold'))
        self.label.place(x=10, y=5)

        # Handle Solo Bounties Dust
        self.dispatchDustLabel = customtkinter.CTkLabel(master=self.BountiesFrame, text='Dispatch Dust', fg_color=("gray86", "gray17"))
        self.dispatchDustLabel.place(x=10, y=40)
        self.dispatchDustCheckbox = customtkinter.CTkCheckBox(master=self.BountiesFrame, text=None, onvalue=True, offvalue=False, command=self.activityUpdate)
        self.dispatchDustCheckbox.place(x=200, y=40)
        # Handle Solo Bounties Diamonds
        self.dispatchDiamondsLabel = customtkinter.CTkLabel(master=self.BountiesFrame, text='Dispatch Diamonds', fg_color=("gray86", "gray17"))
        self.dispatchDiamondsLabel.place(x=10, y=70)
        self.dispatchDiamondsCheckbox = customtkinter.CTkCheckBox(master=self.BountiesFrame, text=None, onvalue=True, offvalue=False, command=self.activityUpdate)
        self.dispatchDiamondsCheckbox.place(x=200, y=70)
        # Handle Solo Bounties Shards
        self.dispatchShardsLabel = customtkinter.CTkLabel(master=self.BountiesFrame, text='Dispatch Shards', fg_color=("gray86", "gray17"))
        self.dispatchShardsLabel.place(x=10, y=100)
        self.dispatchShardsCheckbox = customtkinter.CTkCheckBox(master=self.BountiesFrame, text=None, onvalue=True, offvalue=False, command=self.activityUpdate)
        self.dispatchShardsCheckbox.place(x=200, y=100)
        # Handle Solo Bounties Juice
        self.dispatchJuiceLabel = customtkinter.CTkLabel(master=self.BountiesFrame, text='Dispatch Juice', fg_color=("gray86", "gray17"))
        self.dispatchJuiceLabel.place(x=10, y=130)
        self.dispatchJuiceCheckbox = customtkinter.CTkCheckBox(master=self.BountiesFrame, text=None, onvalue=True, offvalue=False, command=self.activityUpdate)
        self.dispatchJuiceCheckbox.place(x=200, y=130)
        # Refreshes
        self.refreshLabel = customtkinter.CTkLabel(master=self.BountiesFrame, text='Number of Refreshes', fg_color=("gray86", "gray17"))
        self.refreshLabel.place(x=10, y=160)
        self.refreshEntry = customtkinter.CTkEntry(master=self.BountiesFrame, height=20, width=25)
        self.refreshEntry.insert('end', config.get('BOUNTIES', 'refreshes'))
        self.refreshEntry.place(x=200, y=160)
        # Remaining
        self.remainingLabel = customtkinter.CTkLabel(master=self.BountiesFrame, text='# Remaining to Dispatch All', fg_color=("gray86", "gray17"))
        self.remainingLabel.place(x=10, y=190)
        self.remainingEntry = customtkinter.CTkEntry(master=self.BountiesFrame, height=20, width=25)
        self.remainingEntry.insert('end', config.get('BOUNTIES', 'remaining'))
        self.remainingEntry.place(x=200, y=190)

        # # Handle Team Bounties
        # self.teamBountiesLabel = customtkinter.CTkLabel(master=self.activityFrame, text='Dispatch Team Bounties', fg_color=("gray86", "gray17"))
        # self.teamBountiesLabel.place(x=10, y=190)
        # self.teamBountiesCheckbox = customtkinter.CTkCheckBox(master=self.activityFrame, text=None, onvalue=True, offvalue=False, command=self.activityUpdate)
        # self.teamBountiesCheckbox.place(x=200, y=190)

        # Misc Frame
        self.MiscFrame = customtkinter.CTkFrame(master=self, width=235, height=210)
        self.MiscFrame.place(x=500, y=300)
        self.label = customtkinter.CTkLabel(master=self.MiscFrame, text="Misc:", font=("Arial", 15, 'bold'))
        self.label.place(x=10, y=5)

        # Use Bag Comsumables
        self.useBagConsumablesLabel = customtkinter.CTkLabel(master=self.MiscFrame, text='Use Bag Consumables', fg_color=("gray86", "gray17"))
        self.useBagConsumablesLabel.place(x=10, y=40)
        self.useBagConsumablesCheckbox = customtkinter.CTkCheckBox(master=self.MiscFrame, text=None, onvalue=True, offvalue=False, command=self.activityUpdate)
        self.useBagConsumablesCheckbox.place(x=200, y=40)

        # Save button
        self.activitySaveButton = customtkinter.CTkButton(master=self, text="Save", fg_color=["#3B8ED0", "#1F6AA5"], width=120, command=self.activitySave)
        self.activitySaveButton.place(x=320, y=520)

        activityBoxes = ['collectRewards', 'collectMail', 'companionPoints', 'lendMercs', 'attemptCampaign', 'gladiatorCollect',
                         'fountainOfTime', 'kingsTower', 'collectInn', 'guildHunt', 'storePurchases', 'twistedRealm',
                         'collectQuests', 'collectMerchants', 'fightOfFates', 'battleOfBlood', 'circusTour', 'dispatchDust',
                         'dispatchDiamonds', 'dispatchShards', 'dispatchJuice', 'runLab', 'battleArena', 'tsCollect',
                         'useBagConsumables', 'heroesOfEsperia']
        for activity in activityBoxes:
            if activity[0:8] == 'dispatch':
                if config.getboolean('BOUNTIES', activity):
                    self.__getattribute__(activity + 'Checkbox').select()
            elif activity == 'battleArena' or activity == 'tsCollect' or activity == 'gladiatorCollect':
                if config.getboolean('ARENA', activity):
                    self.__getattribute__(activity+'Checkbox').select()
            elif activity == 'fightOfFates' or activity == 'battleOfBlood' or activity == 'circusTour' or activity == 'heroesOfEsperia':
                if config.getboolean('EVENTS', activity):
                    self.__getattribute__(activity + 'Checkbox').select()
            else:
                if config.getboolean('DAILIES', activity):
                    self.__getattribute__(activity+'Checkbox').select()

    def activityUpdate(self):
        activityBoxes = ['collectRewards', 'collectMail', 'companionPoints', 'lendMercs', 'attemptCampaign', 'gladiatorCollect',
                         'fountainOfTime', 'kingsTower', 'collectInn', 'guildHunt', 'storePurchases', 'twistedRealm',
                         'collectQuests', 'collectMerchants', 'fightOfFates', 'battleOfBlood', 'circusTour', 'dispatchDust',
                         'dispatchDiamonds', 'dispatchShards', 'dispatchJuice', 'runLab', 'battleArena', 'tsCollect',
                         'useBagConsumables', 'heroesOfEsperia']
        for activity in activityBoxes:
            if activity[0:8] == 'dispatch':
                if self.__getattribute__(activity + 'Checkbox').get() == 1:
                    config.set('BOUNTIES', activity, 'True')
                else:
                    config.set('BOUNTIES', activity, 'False')
            elif activity == 'battleArena' or activity == 'tsCollect' or activity == 'gladiatorCollect':
                if self.__getattribute__(activity + 'Checkbox').get() == 1:
                    config.set('ARENA', activity, 'True')
                else:
                    config.set('ARENA', activity, 'False')
            elif activity == 'fightOfFates' or activity == 'battleOfBlood' or activity == 'circusTour' or activity == 'heroesOfEsperia':
                if self.__getattribute__(activity + 'Checkbox').get() == 1:
                    config.set('EVENTS', activity, 'True')
                else:
                    config.set('EVENTS', activity, 'False')
            else:
                if self.__getattribute__(activity + 'Checkbox').get() == 1:
                    config.set('DAILIES', activity, 'True')
                else:
                    config.set('DAILIES', activity, 'False')
        updateSettings()

    def textFieldUpdates(self):
        if self.refreshEntry.get() != config.get('BOUNTIES', 'refreshes'):
            config.set('BOUNTIES', 'refreshes', self.refreshEntry.get())
        if self.remainingEntry.get() != config.get('BOUNTIES', 'remaining'):
            config.set('BOUNTIES', 'remaining', self.remainingEntry.get())
        if self.arenaBattlesEntry.get() != config.get('ARENA', 'arenabattles'):
            config.set('ARENA', 'arenabattles', self.arenaBattlesEntry.get())
        if self.arenaOpponentEntry.get() != config.get('ARENA', 'arenaopponent'):
            config.set('ARENA', 'arenaopponent', self.arenaOpponentEntry.get())
        if self.fastrewardsEntry.get() != config.get('DAILIES', 'fastrewards'):
            config.set('DAILIES', 'fastrewards', self.fastrewardsEntry.get())
        if self.shoprefreshEntry.get() != config.get('DAILIES', 'shoprefreshes'):
            config.set('DAILIES', 'shoprefreshes', self.shoprefreshEntry.get())

    def activitySave(self):
        self.activityUpdate()
        self.textFieldUpdates()
        updateSettings()
        activityWindow.destroy(self)


# Shop Window
class shopWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x440")
        self.title('Shop Options')
        self.attributes("-topmost", True)

        # Shop Frame
        self.shopGoldFrame = customtkinter.CTkFrame(master=self, width=185, height=380)
        self.shopGoldFrame.place(x=10, y=10)
        self.label = customtkinter.CTkLabel(master=self.shopGoldFrame, text="Gold Purchases:", font=("Arial", 15, 'bold'))
        self.label.place(x=20, y=5)
        # Dim Frame
        self.shopDiamondFrame = customtkinter.CTkFrame(master=self, width=185, height=380)
        self.shopDiamondFrame.place(x=205, y=10)
        self.label = customtkinter.CTkLabel(master=self.shopDiamondFrame, text="Diamond Purchases:", font=("Arial", 15, 'bold'))
        self.label.place(x=20, y=5)

        ## Gold Shop

        # Shards Gold
        self.shards_goldLabel = customtkinter.CTkLabel(master=self.shopGoldFrame, text='Shards', fg_color=("gray86", "gray17"))
        self.shards_goldLabel.place(x=10, y=40)
        self.shards_goldCheckbox = customtkinter.CTkCheckBox(master=self.shopGoldFrame, text=None, onvalue=True, offvalue=False, command=self.shopUpdate)
        self.shards_goldCheckbox.place(x=130, y=40)
        # Dust Gold
        self.dust_goldLabel = customtkinter.CTkLabel(master=self.shopGoldFrame, text='Dust', fg_color=("gray86", "gray17"))
        self.dust_goldLabel.place(x=10, y=70)
        self.dust_goldCheckbox = customtkinter.CTkCheckBox(master=self.shopGoldFrame, text=None, onvalue=True, offvalue=False, command=self.shopUpdate)
        self.dust_goldCheckbox.place(x=130, y=70)
        # Silver Emblems
        self.silver_emblemLabel = customtkinter.CTkLabel(master=self.shopGoldFrame, text='Silver Emblems', fg_color=("gray86", "gray17"))
        self.silver_emblemLabel.place(x=10, y=100)
        self.silver_emblemCheckbox = customtkinter.CTkCheckBox(master=self.shopGoldFrame, text=None, onvalue=True, offvalue=False, command=self.shopUpdate)
        self.silver_emblemCheckbox.place(x=130, y=100)
        # Gold Emblems
        self.gold_emblemLabel = customtkinter.CTkLabel(master=self.shopGoldFrame, text='Gold Emblems', fg_color=("gray86", "gray17"))
        self.gold_emblemLabel.place(x=10, y=130)
        self.gold_emblemCheckbox = customtkinter.CTkCheckBox(master=self.shopGoldFrame, text=None, onvalue=True, offvalue=False, command=self.shopUpdate)
        self.gold_emblemCheckbox.place(x=130, y=130)
        # PoE Gold
        self.poeLabel = customtkinter.CTkLabel(master=self.shopGoldFrame, text='POE', fg_color=("gray86", "gray17"))
        self.poeLabel.place(x=10, y=160)
        self.poeCheckbox = customtkinter.CTkCheckBox(master=self.shopGoldFrame, text=None, onvalue=True, offvalue=False, command=self.shopUpdate)
        self.poeCheckbox.place(x=130, y=160)

        ## Diamond Shop

        # Timegazer
        self.timegazerLabel = customtkinter.CTkLabel(master=self.shopDiamondFrame, text='Timegazer Card', fg_color=("gray86", "gray17"))
        self.timegazerLabel.place(x=10, y=40)
        self.timegazerCheckbox = customtkinter.CTkCheckBox(master=self.shopDiamondFrame, text=None, onvalue=True, offvalue=False, command=self.shopUpdate)
        self.timegazerCheckbox.place(x=130, y=40)
        # Arcane Staffs
        self.arcanestaffsLabel = customtkinter.CTkLabel(master=self.shopDiamondFrame, text='Arcane Staffs', fg_color=("gray86", "gray17"))
        self.arcanestaffsLabel.place(x=10, y=70)
        self.arcanestaffsCheckbox = customtkinter.CTkCheckBox(master=self.shopDiamondFrame, text=None, onvalue=True, offvalue=False, command=self.shopUpdate)
        self.arcanestaffsCheckbox.place(x=130, y=70)
        # Bait
        self.baitsLabel = customtkinter.CTkLabel(master=self.shopDiamondFrame, text='Baits', fg_color=("gray86", "gray17"))
        self.baitsLabel.place(x=10, y=100)
        self.baitsCheckbox = customtkinter.CTkCheckBox(master=self.shopDiamondFrame, text=None, onvalue=True, offvalue=False, command=self.shopUpdate)
        self.baitsCheckbox.place(x=130, y=100)
        # Cores
        self.coresLabel = customtkinter.CTkLabel(master=self.shopDiamondFrame, text='Cores', fg_color=("gray86", "gray17"))
        self.coresLabel.place(x=10, y=130)
        self.coresCheckbox = customtkinter.CTkCheckBox(master=self.shopDiamondFrame, text=None, onvalue=True, offvalue=False, command=self.shopUpdate)
        self.coresCheckbox.place(x=130, y=130)
        # Dust Diamonds
        self.dust_diamondLabel = customtkinter.CTkLabel(master=self.shopDiamondFrame, text='Dust', fg_color=("gray86", "gray17"))
        self.dust_diamondLabel.place(x=10, y=160)
        self.dust_diamondCheckbox = customtkinter.CTkCheckBox(master=self.shopDiamondFrame, text=None, onvalue=True, offvalue=False, command=self.shopUpdate)
        self.dust_diamondCheckbox.place(x=130, y=160)
        # Elite Soulstone
        self.elite_soulstoneLabel = customtkinter.CTkLabel(master=self.shopDiamondFrame, text='Elite Soulstone', fg_color=("gray86", "gray17"))
        self.elite_soulstoneLabel.place(x=10, y=190)
        self.elite_soulstoneCheckbox = customtkinter.CTkCheckBox(master=self.shopDiamondFrame, text=None, onvalue=True, offvalue=False, command=self.shopUpdate)
        self.elite_soulstoneCheckbox.place(x=130, y=190)
        # Superb Soulstone
        self.superb_soulstoneLabel = customtkinter.CTkLabel(master=self.shopDiamondFrame, text='Superb Soulstone', fg_color=("gray86", "gray17"))
        self.superb_soulstoneLabel.place(x=10, y=220)
        self.superb_soulstoneCheckbox = customtkinter.CTkCheckBox(master=self.shopDiamondFrame, text=None, onvalue=True, offvalue=False, command=self.shopUpdate)
        self.superb_soulstoneCheckbox.place(x=130, y=220)

        # Save button
        self.shopSaveButton = customtkinter.CTkButton(master=self, text="Save", fg_color=["#3B8ED0", "#1F6AA5"], width=120, command=self.shopSave)
        self.shopSaveButton.place(x=140, y=400)

        checkboxes = ['arcanestaffs', 'shards_gold', 'cores', 'timegazer', 'baits', 'dust_gold', 'dust_diamond', 'elite_soulstone',
                      'superb_soulstone', 'silver_emblem', 'gold_emblem', 'poe']
        for box in checkboxes:
            if config.getboolean('SHOP', box):
                self.__getattribute__(box+'Checkbox').select()

    def shopUpdate(self):
        checkboxes = ['arcanestaffs', 'shards_gold', 'cores', 'timegazer', 'baits', 'dust_gold', 'dust_diamond', 'elite_soulstone',
                      'superb_soulstone', 'silver_emblem', 'gold_emblem', 'poe']
        for box in checkboxes:
            if self.__getattribute__(box+'Checkbox').get() == 1:
                config.set('SHOP', box, 'True')
            else:
                config.set('SHOP', box, 'False')
        with open(settings, 'w') as configfile:
            config.write(configfile)

    def shopSave(self):
        self.shopUpdate()
        updateSettings()
        shopWindow.destroy(self)

class advancedWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("250x260")
        self.title('Advanced Options')
        self.attributes("-topmost", True)

        # Activity Frame
        self.advancedFrame = customtkinter.CTkFrame(master=self, width=230, height=200)
        self.advancedFrame.place(x=10, y=10)
        self.label = customtkinter.CTkLabel(master=self.advancedFrame, text="Advanced Options:", font=("Arial", 15, 'bold'))
        self.label.place(x=20, y=5)

        # Port Entry
        self.portLabel = customtkinter.CTkLabel(master=self.advancedFrame, text='Port:', fg_color=("gray86", "gray17"))
        self.portLabel.place(x=10, y=40)
        self.portEntry = customtkinter.CTkEntry(master=self.advancedFrame, height=25, width=60)
        self.portEntry.insert('end', config.get('ADVANCED', 'port'))
        self.portEntry.place(x=45, y=40)

        # Loading.. Entry
        self.delayLabel = customtkinter.CTkLabel(master=self.advancedFrame, text='Delay multiplier:', fg_color=("gray86", "gray17"))
        self.delayLabel.place(x=10, y=70)
        self.delayEntry = customtkinter.CTkEntry(master=self.advancedFrame, height=25, width=30)
        self.delayEntry.insert('end', config.get('ADVANCED', 'loadingMuliplier'))
        self.delayEntry.place(x=110, y=70)

        # Victory Check Duration Entry
        self.victoryCheckLabel = customtkinter.CTkLabel(master=self.advancedFrame, text='Victory Check Frequency:', fg_color=("gray86", "gray17"))
        self.victoryCheckLabel.place(x=10, y=100)
        self.victoryCheckEntry = customtkinter.CTkEntry(master=self.advancedFrame, height=25, width=30)
        self.victoryCheckEntry.insert('end', config.get('PUSH', 'victorycheck'))
        self.victoryCheckEntry.place(x=160, y=100)

        # Victory check suppress non-victory
        self.supressLabel = customtkinter.CTkLabel(master=self.advancedFrame, text='Suppress victory check spam?', fg_color=("gray86", "gray17"))
        self.supressLabel.place(x=10, y=130)
        self.supressCheckbox = customtkinter.CTkCheckBox(master=self.advancedFrame, text=None, onvalue=True, offvalue=False)
        self.supressCheckbox.place(x=190, y=130)

        # Debug Mode
        self.debugLabel = customtkinter.CTkLabel(master=self.advancedFrame, text='Debug Mode', fg_color=("gray86", "gray17"))
        self.debugLabel.place(x=10, y=160)
        self.debugCheckbox = customtkinter.CTkCheckBox(master=self.advancedFrame, text=None, onvalue=True, offvalue=False)
        self.debugCheckbox.place(x=190, y=160)

        # Save button
        self.advanceSaveButton = customtkinter.CTkButton(master=self, text="Save", fg_color=["#3B8ED0", "#1F6AA5"], width=120, command=self.advancedSaveButton)
        self.advanceSaveButton.place(x=60, y=220)

        self.advancedLoadSettings()


    def advancedLoadSettings(self):
        if self.portEntry.get() != config.get('ADVANCED', 'port'):
            self.portEntry.insert(config.get('ADVANCED', 'port'))
        if self.delayEntry.get() != config.get('ADVANCED', 'loadingMuliplier'):
            self.delayEntry.insert(config.get('ADVANCED', 'loadingMuliplier'))
        if self.victoryCheckEntry.get() != config.get('PUSH', 'victorycheck'):
            self.victoryCheckEntry.insert(config.get('PUSH', 'victorycheck'))

        if config.getboolean('PUSH', 'suppressSpam'):
            self.supressCheckbox.select()
        else:
            self.supressCheckbox.deselect()

        if config.getboolean('ADVANCED', 'debug') is True:
            self.debugCheckbox.select()
        else:
            self.debugCheckbox.deselect()

    def advancedSave(self):
        if self.portEntry.get() != config.get('ADVANCED', 'port'):
            config.set('ADVANCED', 'port', self.portEntry.get())
        if self.delayEntry.get() != config.get('ADVANCED', 'loadingMuliplier'):
            config.set('ADVANCED', 'loadingMuliplier', self.delayEntry.get())
        if self.victoryCheckEntry.get() != config.get('PUSH', 'victorycheck'):
            config.set('PUSH', 'victorycheck', self.victoryCheckEntry.get())

        if self.supressCheckbox.get() != config.getboolean('PUSH', 'suppressSpam'):
            if self.supressCheckbox.get() == 1:
                config.set('PUSH', 'suppressSpam', 'True')
            else:
                config.set('PUSH', 'suppressSpam', 'False')

        if self.debugCheckbox.get() != config.getboolean('ADVANCED', 'debug'):
            if self.debugCheckbox.get() == 1:
                config.set('ADVANCED', 'debug', 'True')
            else:
                config.set('ADVANCED', 'debug', 'False')

    def advancedSaveButton(self):
        self.advancedSave()
        updateSettings()
        advancedWindow.destroy(self)

class summonsWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("200x260")
        self.title('Unlimited Summons')
        self.attributes("-topmost", True)
        self.wm_iconbitmap(os.path.join(cwd, 'img', 'auto.ico'))

        # Activity Frame
        self.summonsFrame = customtkinter.CTkFrame(master=self, width=180, height=250)
        self.summonsFrame.place(x=10, y=10)
        self.label = customtkinter.CTkLabel(master=self.summonsFrame, text="Unlimited Summons:", font=("Arial", 15, 'bold'))
        self.label.place(x=10, y=5)

        self.wokeLabel = customtkinter.CTkLabel(master=self.summonsFrame, text='Desired Awakened:', fg_color=("gray86", "gray17"))
        self.wokeLabel.place(x=10, y=40)
        # Activities Dropdown
        self.wokeDropdown = customtkinter.CTkComboBox(master=self.summonsFrame, values=['Awakened Talene', 'Awakened Athalia',
        'Gavus', 'Maetria', 'Awakened Ezizh', 'Awakened Thane', 'Awakened Belinda', 'Awakened Brutus', 'Awakened Safiya',
        'Awakened Solise', 'Awakened Lyca', 'Awakened Baden', 'Awakened Shemira'], width=160)
        self.wokeDropdown.configure(state='readonly')
        self.wokeDropdown.place(x=10, y=70)

        self.celehypoLabel = customtkinter.CTkLabel(master=self.summonsFrame, text='Desired CeleHypo:', fg_color=("gray86", "gray17"))
        self.celehypoLabel.place(x=10, y=100)
        # Activities Dropdown
        self.celehypoDropdown = customtkinter.CTkComboBox(master=self.summonsFrame, values=['Audrae', 'Canisa and Ruke',
        'Daemia', 'Ezizh', 'Khazard', 'Lavatune', 'Liberta', 'Lucilla', 'Lucretia', 'Mehira', 'Mortas', 'Olgath', 'Talene',
        'Tarnos', 'Elijah and Lailah', 'Veithal', 'Vyloris', 'Zaphrael', 'Zikis'], width=160)
        self.celehypoDropdown.configure(state='readonly')
        self.celehypoDropdown.place(x=10, y=130)

        self.x6Checkbox = customtkinter.CTkCheckBox(master=self.summonsFrame, text='x6 Speed Mode', onvalue=True, offvalue=False)
        self.x6Checkbox.place(x=10, y=170)

        # Summons button
        self.summonsButton = customtkinter.CTkButton(master=self.summonsFrame, text="Run Summons", command=lambda: threading.Thread(target=unlimitedSummons).start())
        self.summonsButton.place(x=20, y=210)

        def unlimitedSummons():
            connect_device()
            infiniteSummons(self.wokeDropdown.get(), self.celehypoDropdown.get(), self.x6Checkbox.get())
            summonsWindow.destroy(self)

# Will change the dropdown to only include open towers
# May cause issues with timezones..
def setUlockedTowers():
    days = {1:["Campaign", "King's Tower", "Lightbringer Tower"],
    2:["Campaign", "King's Tower", "Mauler Tower"],
    3:["Campaign", "King's Tower", "Wilder Tower", "Celestial Tower"],
    4:["Campaign", "King's Tower", "Graveborn Tower", "Hypogean Tower"],
    5:["Campaign", "King's Tower", "Lightbringer Tower", "Mauler Tower", "Celestial Tower"],
    6:["Campaign", "King's Tower", "Wilder Tower", "Graveborn Tower", "Hypogean Tower"],
    7:["Campaign", "King's Tower", "Lightbringer Tower", "Wilder Tower", "Mauler Tower", "Graveborn Tower", "Hypogean Tower", "Celestial Tower"]}
    for day, towers in days.items():
        if currenttimeutc.isoweekday() == day:
            app.pushLocationDropdown.configure(values=towers)

def headlessArgs():
    if args['dailies']:
        dailies()
        sys.exit(0)
    if args['autotower']:
        connect_device()
        formation = int(str(config.get('PUSH', 'formation'))[0:1])
        duration = int(config.get('PUSH', 'victoryCheck'))
        towerdays = {1: 'Lightbringer Tower', 2: 'Mauler Tower', 3: 'Wilder Tower', 4: 'Graveborn Tower', 5: 'Celestial Tower',
                     6: 'Hypogean Tower', 7: 'King\'s Tower'}
        for day, tower in towerdays.items():
            if currenttimeutc.isoweekday() == day:
                printBlue('Auto-Pushing ' + str(tower) + ' using using the ' + str(config.get('PUSH', 'formation') + ' formation'))
                wait(3)
                while 1:
                    towerPusher.pushTower(tower, formation, duration)
    if args['tower']:
        print('ok')

def updateSettings():
    with open(settings, 'w') as configfile:
        config.write(configfile)
    config.read(settings)  # to load the new value into memory

def buttonState(state):
    app.dailiesButton.configure(state=state)
    app.arenaButton.configure(state=state)
    app.pushButton.configure(state=state)

def activityManager():
    if app.pvpEntry.get() != config.get('ACTIVITY', 'activitybattles'):
        config.set('ACTIVITY', 'activitybattles', app.pvpEntry.get())
    updateSettings()

    if app.activityFormationDropdown.get() == "Fight of Fates":
        buttonState('disabled')
        connect_device()
        handleFightOfFates(config.getint('ACTIVITY', 'activitybattles'))
        buttonState('normal')
        print('')
        return

    if app.activityFormationDropdown.get() == "Battle of Blood":
        buttonState('disabled')
        connect_device()
        handleBattleofBlood(config.getint('ACTIVITY', 'activitybattles'))
        buttonState('normal')
        print('')
        return

    if app.activityFormationDropdown.get() == "Arena of Heroes":
        buttonState('disabled')
        connect_device()
        handleArenaOfHeroes(config.getint('ACTIVITY', 'activitybattles'), config.getint('ARENA', 'arenaopponent'))
        buttonState('normal')
        print('')
        return

    if app.activityFormationDropdown.get() == "Arcane Labyrinth":
        buttonState('disabled')
        connect_device()
        handleLab()
        buttonState('normal')
        print('')
        return

    if app.activityFormationDropdown.get() == "Heroes of Esperia":
        buttonState('disabled')
        connect_device()
        handleHeroesofEsperia(config.getint('ACTIVITY', 'activitybattles'), config.getint('ARENA', 'arenaopponent'))
        buttonState('normal')
        print('')
        return

def open_summonswindow():
    summons_window = None
    if summons_window is None or not summons_window.winfo_exists():
        summons_window = summonsWindow()  # create window if its None or destroyed
        summons_window.focus()
    else:
        summons_window.focus()  # if window exists focus it

def dailiesButton():
    buttonState('disabled')
    dailies()
    print('')
    buttonState('normal')
    return

def serverCheck():
    slotsXY = {1: [700, 575], 2: [700, 750], 3: [700, 920], 4: [700, 1100], 5: [700, 1250], 6: [700, 1450]} # Slot positions
    server = ((config.getint('ADVANCED', 'server'))) # Slot defined in settings
    if (config.getint('ADVANCED', 'server')) != 0:
        clickXY(120, 100, seconds=5) # Navigate to server selection
        clickXY(650, 1675)
        clickXY(300, 500)
        for slot, pos in slotsXY.items(): # Click corresponding server
            if server == slot:
                clickXY(pos[0], pos[1], seconds=10)
                if isVisible('buttons/confirm'):
                    printGreen('Switching to server slot ' + str(server))
                    click('buttons/confirm', confidence=0.8)
                    waitUntilGameActive()
                else:
                    printWarning('No server change confirmation found')
                    clickXY(70, 1810)
                    clickXY(70, 1810)

def dailies():
    connect_device()
    serverCheck() # Change server slot if defined before doing dailies
    if config.getboolean('DAILIES', 'collectrewards') is True:
        collectAFKRewards()
    if config.getboolean('DAILIES', 'collectmail') is True:
        collectMail()
    if config.getboolean('DAILIES', 'companionpoints') is True:
        collectCompanionPoints(config.getboolean('DAILIES', 'lendmercs'))
    if config.getint('DAILIES', 'fastrewards') > 0:
        collectFastRewards(config.getint('DAILIES', 'fastrewards'))
    if config.getboolean('DAILIES', 'attemptcampaign') is True:
        attemptCampaign()
    if config.getboolean('BOUNTIES', 'teambounties') is True:
        handleBounties()
    if config.getboolean('ARENA', 'battlearena') is True:
        handleArenaOfHeroes(config.getint('ARENA', 'arenabattles'), config.getint('ARENA', 'arenaopponent'))
    if config.getboolean('ARENA', 'tscollect') is True:
        collectTSRewards()
    if config.getboolean('ARENA', 'gladiatorcollect') is True:
        collectGladiatorCoins()
    if config.getboolean('DAILIES', 'fountainoftime') is True:
        collectFountainOfTime()
    if config.getboolean('DAILIES', 'kingstower') is True:
        handleKingsTower()
    if config.getboolean('DAILIES', 'collectinn') is True:
        collectInnGifts()
    if config.getboolean('DAILIES', 'guildhunt') is True:
        handleGuildHunts()
    if config.getboolean('DAILIES', 'storepurchases') is True:
        shopPurchases(config.getint('DAILIES', 'shoprefreshes'))
    if config.getboolean('DAILIES', 'twistedrealm') is True:
        handleTwistedRealm()
    if config.getboolean('EVENTS', 'fightoffates') is True:
        handleFightOfFates()
    if config.getboolean('EVENTS', 'battleofblood') is True:
        handleBattleofBlood()
    if config.getboolean('EVENTS', 'circusTour') is True:
        handleCircusTour()
    if config.getboolean('DAILIES', 'runLab') is True:
        handleLab()
    if config.getboolean('EVENTS', 'heroesofesperia') is True:
        handleHeroesofEsperia(3, 4)
    if config.getboolean('DAILIES', 'collectquests') is True:
        collectQuests()
    if config.getboolean('DAILIES', 'collectmerchants') is True:
        clearMerchant()
    if config.getboolean('DAILIES', 'usebagconsumables') is True:
        useBagConsumables()
    printGreen('Dailies done!')
    return

def push():
    connect_device()
    buttonState('disabled')
    formation = int(str(app.pushFormationDropdown.get())[0:1]) # to str first so we can take first character, then int

    if app.pushLocationDropdown.get() == 'Campaign':
        printBlue('Auto-Pushing Campaign using the ' + str(app.pushFormationDropdown.get()) + ' formation')
        confirmLocation('campaign', region=boundaries['campaignSelect'])
        if str(app.pushFormationDropdown.get()) != config.get('PUSH', 'formation'):
            config.set('PUSH', 'formation', app.pushFormationDropdown.get())
        updateSettings()
        while 1:
            pushCampaign(formation=formation, duration=int(config.get('PUSH', 'victoryCheck')))
    else:
        printBlue('Auto-Pushing ' + str(app.pushLocationDropdown.get()) + ' using using the ' + str(app.pushFormationDropdown.get()) + ' formation')
        if str(app.pushFormationDropdown.get()) != config.get('PUSH', 'formation'):
            config.set('PUSH', 'formation', app.pushFormationDropdown.get())
        updateSettings()
        while 1:
            towerPusher.pushTower(tower=app.pushLocationDropdown.get(), formation=formation, duration=int(config.get('PUSH', 'victoryCheck')))

class IORedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

class STDOutRedirector(IORedirector):
    def write(self, string):
        timestamp = '[' + datetime.now().strftime("%H:%M:%S") + '] '
        # Very hacky implementation, we scan first 3 characters for colour tag, if found we apply the textbox tag
        # and print the string minus the first 3 characters
        entry = string[0:3]
        if entry == 'ERR':
            self.text_space.insert('end', timestamp + string[3:], 'error')
        elif entry == 'WAR':
            self.text_space.insert('end', timestamp + string[3:], 'warning')
        elif entry == 'GRE':
            self.text_space.insert('end', timestamp + string[3:], 'green')
        elif entry == 'BLU':
            self.text_space.insert('end', timestamp + string[3:], 'blue')
        elif entry == 'PUR':
            self.text_space.insert('end', timestamp + string[3:], 'purple')
        else:
            self.text_space.insert('end', string)
        self.text_space.see('end')
    def flush(self):
        sys.stdout.flush()

if __name__ == "__main__":
    app = App()
    setUlockedTowers()
    headlessArgs() # Will launch dailies script before we load the UI if its flagged
    app.mainloop()

def writeToLog(text):
    if args['logging'] is True:
        with open((args['config']).split('.')[0] + '.log', 'a') as log:
            line = '[' + datetime.now().strftime("%d/%m/%y %H:%M:%S") + '] ' + text + '\n'
            log.write(line)

# Coloured text for the console
def printError(text):
    if args['dailies']:
        print(text)
    else:
        print('ERR' + text)
    writeToLog(text)

def printGreen(text):
    if args['dailies']:
        print(text)
    else:
        print('GRE' + text)
    writeToLog(text)

def printWarning(text):
    if args['dailies']:
        print(text)
    else:
        print('WAR' + text)
    writeToLog(text)

def printBlue(text):
    if args['dailies']:
        print(text)
    else:
        print('BLU' + text)
    writeToLog(text)

def printPurple(text):
    if args['dailies']:
        print(text)
    else:
        print('PUR' + text)
    writeToLog(text)