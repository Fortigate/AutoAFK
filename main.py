from activities import *
import customtkinter
import threading
import sys

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
        self.dailiesFrame = customtkinter.CTkFrame(master=self, height=200, width=180)
        self.dailiesFrame.place(x=10, y=20)
        # Dailies button
        self.dailiesButton = customtkinter.CTkButton(master=self, text="Run Dailies", command=threading.Thread(target=dailiesButton).start)
        self.dailiesButton.place(x=20, y=40)
        # Arena
        self.arenaLabel = customtkinter.CTkLabel(master=self, text='Arena Battles', fg_color=("gray86", "gray17"))
        self.arenaLabel.place(x=20, y=80)
        self.arenaEntry = customtkinter.CTkEntry(master=self, placeholder_text="5", height=20, width=30)
        self.arenaEntry.place(x=120, y=80)
        # FR
        self.fastrewardsLabel = customtkinter.CTkLabel(master=self, text='Fast Rewards', fg_color=("gray86", "gray17"))
        self.fastrewardsLabel.place(x=20, y=118)
        self.fastrewardsEntry = customtkinter.CTkEntry(master=self, placeholder_text="5", height=20, width=30)
        self.fastrewardsEntry.place(x=120, y=118)
        # Shop Refresh
        self.shoprefreshLabel = customtkinter.CTkLabel(master=self, text='Shop Refreshes', fg_color=("gray86", "gray17"))
        self.shoprefreshLabel.place(x=20, y=154)
        self.shoprefreshEntry = customtkinter.CTkEntry(master=self, placeholder_text="2", height=20, width=30)
        self.shoprefreshEntry.place(x=120, y=154)

        # PvP Frame
        self.arenaFrame = customtkinter.CTkFrame(master=self, height=200, width=180)
        self.arenaFrame.place(x=10, y=240)

        # PvP button
        self.arenaButton = customtkinter.CTkButton(master=self, text="Run PvP Tickets", command=threading.Thread(target=ticketBurn).start)
        self.arenaButton.place(x=20, y=260)

        # PvP Entry
        self.pvpLabel = customtkinter.CTkLabel(master=self, text='How many battles', fg_color=("gray86", "gray17"))
        self.pvpLabel.place(x=20, y=300)
        self.pvpEntry = customtkinter.CTkEntry(master=self, placeholder_text="10", height=20, width=40)
        self.pvpEntry.place(x=130, y=300)

        # self.dailiesButton = customtkinter.CTkButton(master=self, text="Stop", fg_color='red', hover_color='maroon')
        # self.dailiesButton.place(x=20, y=500)

        # Textbox Frame
        self.textbox = customtkinter.CTkTextbox(master=self, width=580, height=560)
        self.textbox.place(x=200, y=20)
        self.textbox.configure(text_color='white', font=('Arial', 14))
        sys.stdout = STDOutRedirector(self.textbox)
        # sys.stderr = STDOutRedirector(self.textbox)

def ticketBurn():
    if app.pvpEntry.get() == '':
        arenaBattles = 5
    else:
        arenaBattles = int(app.pvpEntry.get())
    connect_device()
    handleArenaOfHeroes(arenaBattles)

def dailiesButton():
    if app.arenaEntry.get() == '':
        intArena = 5
    else:
        intArena = int(app.arenaEntry.get())

    if app.fastrewardsEntry.get() == '':
        intFR = 5
    else:
        intFR = int(app.fastrewardsEntry.get())

    if app.shoprefreshEntry.get() == '':
        intSR = 2
    else:
        intSR = int(app.shoprefreshEntry.get())

    dailies(fastRewards=intFR, arenaBattles=intArena, shoprefreshes=intSR)

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
    collectQuests()
    clearMerchant()
    shopPurchases(shoprefreshes)


class IORedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

class STDOutRedirector(IORedirector):
    def write(self, string):
        self.text_space.insert('end', string)
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
    print(text)

def printGreen(text):
    print(text)

def printWarning(text):
    print(text)

def printBlue(text):
    print(text)
