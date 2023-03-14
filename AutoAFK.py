from activities import *
import customtkinter
import threading
import sys
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')
customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

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
        self.twistedRealmCheckbox = customtkinter.CTkCheckBox(master=self.dailiesFrame, text=None)
        self.twistedRealmCheckbox.place(x=130, y=150)
        # Solo Bounties
        self.soloBountiesLabel = customtkinter.CTkLabel(master=self.dailiesFrame, text='Dispatch Bounties?', fg_color=("gray86", "gray17"))
        self.soloBountiesLabel.place(x=10, y=180)
        self.soloBountiesCheckbox = customtkinter.CTkCheckBox(master=self.dailiesFrame, text=None)
        self.soloBountiesCheckbox.place(x=130, y=180)


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
        self.pushButton = customtkinter.CTkButton(master=self.pushFrame, state='disabled', text="Push", command=threading.Thread(target=ticketBurn).start)
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
        self.textbox.tag_config('green', foreground='green')
        self.textbox.tag_config('blue', foreground='cyan')
        self.textbox.insert('end', 'Welcome to AutoAFK!\n')
        self.textbox.insert('end', 'Some things to note:\n')
        self.textbox.insert('end', '* Running multiple tasks will give a \'thread\' error, so restart for each new task\n')
        self.textbox.insert('end', '* We\'re still in Beta so expect bugs, please report them in Github or Discord\n\n')
        sys.stdout = STDOutRedirector(self.textbox)

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

    if app.fastrewardsEntry.get() == '':
        intFR = 5
    else:
        intFR = int(app.fastrewardsEntry.get())

    if app.shoprefreshEntry.get() == '':
        intSR = 2
    else:
        intSR = int(app.shoprefreshEntry.get())

    with open('settings.ini', 'w') as configfile:
        config.write(configfile)

    dailies(fastRewards=intFR, arenaBattles=int(app.arenaEntry.get()), shoprefreshes=intSR)

def dailies(fastRewards, arenaBattles, shoprefreshes):
    connect_device()
    collectAFKRewards()
    collectMail()
    collectCompanionPoints()
    collectFastRewards(fastRewards)
    attemptCampaign()
    handleBounties()
    handleArenaOfHeroes(arenaBattles)
    handleKingsTower()
    collectInnGifts()
    handleGuildHunts()
    clearMerchant()
    shopPurchases(shoprefreshes)
    collectQuests()


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
