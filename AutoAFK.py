from activities import *
import customtkinter
import threading
import sys
import configparser
import os

cwd = (os.path.dirname(__file__) + '\\')
config = configparser.ConfigParser()
config.read('settings.ini')
customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x400")
        self.title('Shop Options')
        self.attributes("-topmost", True)

        # Shop Frame
        self.shopFrame = customtkinter.CTkFrame(master=self, width=180, height=380)
        self.shopFrame.place(x=10, y=10)
        self.label = customtkinter.CTkLabel(master=self.shopFrame, text="Shop Purchases:", font=("Arial", 15, 'bold'))
        self.label.place(x=20, y=5)
        # Dim Frame
        self.dimFrame = customtkinter.CTkFrame(master=self, width=180, height=380)
        self.dimFrame.place(x=210, y=10)
        self.label = customtkinter.CTkLabel(master=self.dimFrame, text="Dim Gear:", font=("Arial", 15, 'bold'))
        self.label.place(x=20, y=5)


        # Shards
        self.shardsLabel = customtkinter.CTkLabel(master=self.shopFrame, text='Shards', fg_color=("gray86", "gray17"))
        self.shardsLabel.place(x=10, y=40)
        self.shardsCheckbox = customtkinter.CTkCheckBox(master=self.shopFrame, text=None, onvalue=True, offvalue=False, command=self.shopUpdate)
        self.shardsCheckbox.place(x=130, y=40)
        # Cores
        self.coresLabel = customtkinter.CTkLabel(master=self.shopFrame, text='Cores', fg_color=("gray86", "gray17"))
        self.coresLabel.place(x=10, y=70)
        self.coresCheckbox = customtkinter.CTkCheckBox(master=self.shopFrame, text=None, onvalue=True, offvalue=False, command=self.shopUpdate)
        self.coresCheckbox.place(x=130, y=70)
        # Timegazer
        self.timegazerLabel = customtkinter.CTkLabel(master=self.shopFrame, text='Timegazer Card', fg_color=("gray86", "gray17"))
        self.timegazerLabel.place(x=10, y=100)
        self.timegazerCheckbox = customtkinter.CTkCheckBox(master=self.shopFrame, text=None, onvalue=True, offvalue=False, command=self.shopUpdate)
        self.timegazerCheckbox.place(x=130, y=100)
        # Bait
        self.baitsLabel = customtkinter.CTkLabel(master=self.shopFrame, text='Baits', fg_color=("gray86", "gray17"))
        self.baitsLabel.place(x=10, y=130)
        self.baitsCheckbox = customtkinter.CTkCheckBox(master=self.shopFrame, text=None, onvalue=True, offvalue=False, command=self.shopUpdate)
        self.baitsCheckbox.place(x=130, y=130)
        # Dust Gold
        self.dust_goldLabel = customtkinter.CTkLabel(master=self.shopFrame, text='Dust (gold)', fg_color=("gray86", "gray17"))
        self.dust_goldLabel.place(x=10, y=160)
        self.dust_goldCheckbox = customtkinter.CTkCheckBox(master=self.shopFrame, text=None, onvalue=True, offvalue=False, command=self.shopUpdate)
        self.dust_goldCheckbox.place(x=130, y=160)
        # Dust Diamonds
        self.dust_diamondLabel = customtkinter.CTkLabel(master=self.shopFrame, text='Dust (diamonds)', fg_color=("gray86", "gray17"))
        self.dust_diamondLabel.place(x=10, y=190)
        self.dust_diamondCheckbox = customtkinter.CTkCheckBox(master=self.shopFrame, text=None, onvalue=True, offvalue=False, command=self.shopUpdate)
        self.dust_diamondCheckbox.place(x=130, y=190)
        # Elite Soulstone
        self.elite_soulstoneLabel = customtkinter.CTkLabel(master=self.shopFrame, text='Elite Soulstone', fg_color=("gray86", "gray17"))
        self.elite_soulstoneLabel.place(x=10, y=220)
        self.elite_soulstoneCheckbox = customtkinter.CTkCheckBox(master=self.shopFrame, text=None, onvalue=True, offvalue=False, command=self.shopUpdate)
        self.elite_soulstoneCheckbox.place(x=130, y=220)
        # Elite Soulstone
        self.superb_soulstoneLabel = customtkinter.CTkLabel(master=self.shopFrame, text='Superb Soulstone', fg_color=("gray86", "gray17"))
        self.superb_soulstoneLabel.place(x=10, y=250)
        self.superb_soulstoneCheckbox = customtkinter.CTkCheckBox(master=self.shopFrame, text=None, onvalue=True, offvalue=False, command=self.shopUpdate)
        self.superb_soulstoneCheckbox.place(x=130, y=250)
        # Silver Emblems
        self.silver_emblemLabel = customtkinter.CTkLabel(master=self.shopFrame, text='Silver Emblems', fg_color=("gray86", "gray17"))
        self.silver_emblemLabel.place(x=10, y=280)
        self.silver_emblemCheckbox = customtkinter.CTkCheckBox(master=self.shopFrame, text=None, onvalue=True, offvalue=False, command=self.shopUpdate)
        self.silver_emblemCheckbox.place(x=130, y=280)
        # Gold Emblems
        self.gold_emblemLabel = customtkinter.CTkLabel(master=self.shopFrame, text='Gold Emblems', fg_color=("gray86", "gray17"))
        self.gold_emblemLabel.place(x=10, y=310)
        self.gold_emblemCheckbox = customtkinter.CTkCheckBox(master=self.shopFrame, text=None, onvalue=True, offvalue=False, command=self.shopUpdate)
        self.gold_emblemCheckbox.place(x=130, y=310)
        # PoE
        self.poeLabel = customtkinter.CTkLabel(master=self.shopFrame, text='PoE (gold)', fg_color=("gray86", "gray17"))
        self.poeLabel.place(x=10, y=340)
        self.poeCheckbox = customtkinter.CTkCheckBox(master=self.shopFrame, text=None, onvalue=True, offvalue=False, command=self.shopUpdate)
        self.poeCheckbox.place(x=130, y=340)

        checkboxes = ['shards', 'cores', 'timegazer', 'baits', 'dust_gold', 'dust_diamond', 'elite_soulstone',
                      'superb_soulstone', 'silver_emblem', 'gold_emblem', 'poe']
        for box in checkboxes:
            if config.getboolean('SHOP', box):
                self.__getattribute__(box+'Checkbox').select()

    def shopUpdate(self):
        checkboxes = ['shards', 'cores', 'timegazer', 'baits', 'dust_gold', 'dust_diamond', 'elite_soulstone',
                      'superb_soulstone', 'silver_emblem', 'gold_emblem', 'poe']
        for box in checkboxes:
            if self.__getattribute__(box+'Checkbox').get() == 1:
                config.set('SHOP', box, 'True')
            else:
                config.set('SHOP', box, 'False')
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("AutoAFK")
        self.geometry(f"{800}x{600}")

        # configure grid layout (4x4)
        self.grid_rowconfigure((0, 1, 2), weight=0)
        self.grid_columnconfigure((0, 1, 2), weight=0)

        # Dailies Frame
        self.dailiesFrame = customtkinter.CTkFrame(master=self, height=260, width=180)
        self.dailiesFrame.place(x=10, y=20)
        # Dailies button
        self.dailiesButton = customtkinter.CTkButton(master=self, text="Run Dailies", command=threading.Thread(target=dailiesButton).start)
        self.dailiesButton.place(x=30, y=35)
        # Arena Bttls
        self.arenaLabel = customtkinter.CTkLabel(master=self.dailiesFrame, text='Arena Battles', fg_color=("gray86", "gray17"))
        self.arenaLabel.place(x=10, y=60)
        self.arenaEntry = customtkinter.CTkEntry(master=self.dailiesFrame, height=20, width=30)
        self.arenaEntry.insert('end', config.get('DAILIES', 'arenabattles'))
        self.arenaEntry.place(x=130, y=60)
        # Fast Rewards
        self.fastrewardsLabel = customtkinter.CTkLabel(master=self.dailiesFrame, text='Fast Rewards', fg_color=("gray86", "gray17"))
        self.fastrewardsLabel.place(x=10, y=90)
        self.fastrewardsEntry = customtkinter.CTkEntry(master=self.dailiesFrame, height=20, width=30)
        self.fastrewardsEntry.insert('end', config.get('DAILIES', 'fastrewards'))
        self.fastrewardsEntry.place(x=130, y=90)
        # Shop Refresh
        self.shoprefreshLabel = customtkinter.CTkLabel(master=self.dailiesFrame, text='Shop Refreshes', fg_color=("gray86", "gray17"))
        self.shoprefreshLabel.place(x=10, y=120)
        self.shoprefreshEntry = customtkinter.CTkEntry(master=self.dailiesFrame, height=20, width=30)
        self.shoprefreshEntry.insert('end', config.get('DAILIES', 'shoprefreshes'))
        self.shoprefreshEntry.place(x=130, y=120)
        # Twisted Realm
        self.twistedRealmLabel = customtkinter.CTkLabel(master=self.dailiesFrame, text='Twisted Realm?', fg_color=("gray86", "gray17"))
        self.twistedRealmLabel.place(x=10, y=150)
        self.twistedRealmCheckbox = customtkinter.CTkCheckBox(master=self.dailiesFrame, text=None, onvalue=True, offvalue=False, command=self.Update)
        if bool(config.getboolean('TWISTED REALM', 'twistedrealm')):
            self.twistedRealmCheckbox.select()
        self.twistedRealmCheckbox.place(x=130, y=150)
        # Solo Bounties
        self.soloBountiesLabel = customtkinter.CTkLabel(master=self.dailiesFrame, text='Dispatch Bounties?', fg_color=("gray86", "gray17"))
        self.soloBountiesLabel.place(x=10, y=180)
        self.soloBountiesCheckbox = customtkinter.CTkCheckBox(master=self.dailiesFrame, text=None, onvalue=True, offvalue=False, command=self.Update)
        if bool(config.getboolean('BOUNTIES', 'dispatchsolo')):
            self.soloBountiesCheckbox.select()
        self.soloBountiesCheckbox.place(x=130, y=180)
        # Shop button
        self.dailiesButton = customtkinter.CTkButton(master=self, text="Shop Options", fg_color=["#3B8ED0", "#1F6AA5"], width=120, command=self.open_toplevel)
        self.dailiesButton.place(x=40, y=240)

        # PvP Frame
        self.arenaFrame = customtkinter.CTkFrame(master=self, height=100, width=180)
        self.arenaFrame.place(x=10, y=290)

        # PvP button
        self.arenaButton = customtkinter.CTkButton(master=self.arenaFrame, text="Run PvP Tickets", command=threading.Thread(target=ticketBurn).start)
        self.arenaButton.place(x=20, y=15)
        # PvP Entry
        self.pvpLabel = customtkinter.CTkLabel(master=self.arenaFrame, text='How many battles', fg_color=("gray86", "gray17"))
        self.pvpLabel.place(x=10, y=60)
        self.pvpEntry = customtkinter.CTkEntry(master=self.arenaFrame, height=20, width=40)
        self.pvpEntry.insert('end', config.get('ARENA', 'arenabattles'))
        self.pvpEntry.place(x=130, y=60)

        # Push Frame
        self.pushFrame = customtkinter.CTkFrame(master=self, height=180, width=180)
        self.pushFrame.place(x=10, y=400)

        # Push Button
        self.pushButton = customtkinter.CTkButton(master=self.pushFrame, state='disabled', text="Coming Soon", command=threading.Thread(target=ticketBurn).start)
        self.pushButton.place(x=20, y=15)
        # Push Entry
        self.pushLabel = customtkinter.CTkLabel(master=self.pushFrame, text='Where to push?', fg_color=("gray86", "gray17"))
        self.pushLabel.place(x=10, y=50)
        self.pushDropdown = customtkinter.CTkComboBox(master=self.pushFrame,  values=["Campaign", "King's Tower", "Lightbringer", "Wilder", "Mauler", "Graveborn", "Hypogean", "Celestial"], width=160)
        self.pushDropdown.place(x=10, y=80)
        # Push Formation
        self.pushLabel = customtkinter.CTkLabel(master=self.pushFrame, text='Which formation?', fg_color=("gray86", "gray17"))
        self.pushLabel.place(x=10, y=120)
        self.pushDropdown = customtkinter.CTkComboBox(master=self.pushFrame,  values=["1st", "2nd", "3rd", "4th", "5th"], width=50)
        self.pushDropdown.place(x=120, y=120)
        # Push Duration
        self.pushLabel = customtkinter.CTkLabel(master=self.pushFrame, text='How long for?', fg_color=("gray86", "gray17"))
        self.pushLabel.place(x=10, y=150)
        self.pushDropdown = customtkinter.CTkEntry(master=self.pushFrame, width=50)
        self.pushDropdown.place(x=120, y=150)

        # Textbox Frame
        self.textbox = customtkinter.CTkTextbox(master=self, width=580, height=560)
        self.textbox.place(x=200, y=20)
        self.textbox.configure(text_color='white', font=('Arial', 14))
        self.textbox.tag_config("error", foreground="red")
        self.textbox.tag_config('warning', foreground='yellow')
        self.textbox.tag_config('green', foreground='lawngreen')
        self.textbox.tag_config('blue', foreground='cyan')
        self.textbox.insert('end', 'Welcome to AutoAFK!\n')
        self.textbox.insert('end', 'Some things to note:\n')
        self.textbox.insert('end', '* Running multiple tasks will give a \'thread\' error, so restart for each new task\n')
        self.textbox.insert('end', '* We\'re still in Beta so expect bugs, please report them in Github or Discord\n\n')
        sys.stdout = STDOutRedirector(self.textbox)

        self.toplevel_window = None

    def Update(self):
        if self.twistedRealmCheckbox.get() == 1:
            config.set('TWISTED REALM', 'twistedrealm', 'True')
        else:
            config.set('TWISTED REALM', 'twistedrealm', 'False')

        if self.soloBountiesCheckbox.get() == 1:
            config.set('BOUNTIES', 'dispatchsolo', 'True')
        else:
            config.set('BOUNTIES', 'dispatchsolo', 'False')

        with open('settings.ini', 'w') as configfile:
            config.write(configfile)


    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
            self.toplevel_window.focus()
        else:
            self.toplevel_window.focus()  # if window exists focus it

def buttonState(state):
    app.dailiesButton.configure(state=state)
    app.arenaButton.configure(state=state)

def ticketBurn():
    if app.pvpEntry.get() != config.get('ARENA', 'arenabattles'):
        config.set('ARENA', 'arenabattles', app.pvpEntry.get())

    with open('settings.ini', 'w') as configfile:
        config.write(configfile)

    buttonState('disabled')
    connect_device()
    handleArenaOfHeroes(int(config.get('ARENA', 'arenabattles')))
    buttonState('enabled')

def dailiesButton():
    if app.arenaEntry.get() != config.get('DAILIES', 'arenabattles'):
        config.set('DAILIES', 'arenabattles', app.arenaEntry.get())
    if app.fastrewardsEntry.get() != config.get('DAILIES', 'fastrewards'):
        config.set('DAILIES', 'fastrewards', app.fastrewardsEntry.get())
    if app.shoprefreshEntry.get() != config.get('DAILIES', 'shoprefreshes'):
        config.set('DAILIES', 'shoprefreshes', app.shoprefreshEntry.get())

    with open(cwd + 'settings.ini', 'w') as configfile:
        config.write(configfile)

    dailies()

def dailies():
    connect_device()
    # collectAFKRewards()
    # collectMail()
    # collectCompanionPoints()
    # collectFastRewards(int(app.fastrewardsEntry.get()))
    # attemptCampaign()
    # handleBounties()
    # handleArenaOfHeroes(int(app.arenaEntry.get()))
    # collectGladiatorCoins()
    # collectFountainOfTime()
    # handleKingsTower()
    collectInnGifts()
    handleGuildHunts()
    shopPurchases(int(app.shoprefreshEntry.get()))
    handleTwistedRealm()
    collectQuests()
    clearMerchant()
    printGreen('\nDailies done!')


class IORedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

class STDOutRedirector(IORedirector):
    def write(self, string):
        # Very hacky implementation, we scan first 3 characters for colour tag, if found we apply the textbox tag
        # and print the string minus the first 3 characters
        entry = string[0:3]
        if entry == 'ERR':
            self.text_space.insert('end', string[3:], 'error')
        elif entry == 'WAR':
            self.text_space.insert('end', string[3:], 'warning')
        elif entry == 'GRE':
            self.text_space.insert('end', string[3:], 'green')
        elif entry == 'BLU':
            self.text_space.insert('end', string[3:], 'blue')
        else:
            self.text_space.insert('end', string)
        self.text_space.see('end')
    def flush(self):
        sys.stdout.flush()

if __name__ == "__main__":
    app = App()
    app.mainloop()

## Automation Functions
# Uncomment as needed, screenshot is for debugging/collecting buttons

# take_screenshot(tools.device)

# todolist
# Clear Merchant gifts & !'s
# switchCharacter
# openMenu left and right
# checkDailyQuestStatus
# collectFountainOfTime
# storePurchases
# attemptCardGame / events

# Coloured text for the console
def printError(text):
    print('ERR' + text)

def printGreen(text):
    print('GRE' + text)

def printWarning(text):
    print('WAR' + text)

def printBlue(text):
    print('BLU' + text)
