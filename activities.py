from math import ceil
from tools import *
from AutoAFK import printGreen, printError, printWarning, printBlue, printPurple, settings
import datetime
import configparser

config = configparser.ConfigParser()
config.read(settings)
d = datetime.datetime.now()

# Counters for summonsCrashDetector()
rarecounter = int()
epiccounter = int()
awakenedcounter = int()

boundries = {
    #locate
    'campaignSelect': (424, 1750, 232, 170),
    'darkforestSelect': (208, 1750, 226, 170),
    'ranhornSelect': (0, 1750, 210, 160),
    #campaign/auto battle
    'begin': (322, 1590, 442, 144),
    'multiBegin': (309, 1408, 467, 129),
    'autobattle': (214, 1774, 256, 112),
    'battle': (574, 1779, 300, 110),
    'battleLarge': (310, 1758, 464, 144),
    'formations': (914, 1762, 102, 134),
    'useAB': (604, 1754, 242, 84),
    'confirmAB': (566, 1188, 252, 90),
    'activateAB': (580, 1208, 272, 86),
    'autobattle0': (562,994,144,122),
    'autobattleLabel': (200, 578, 684, 178),
    'exitAB': (578, 1250, 290, 88),
    'cancelAB': (218, 1248, 298, 90),
    'pauseBattle': (24, 1419, 119, 104),
    'exitBattle': (168, 886, 130, 116),
    'tryagain': (478, 892, 128, 120),
    'continueBattle': (766, 888, 172, 128),
    'taptocontinue': (374, 1772, 330, 62),
    'kingstowerLabel': (253, 0, 602, 100),
    'challengeTower': (356, 726, 364, 1024),
    'heroclassselect': (5, 1620, 110, 120),


    'collectAfk': (590, 1322, 270, 82),
    
    'mailLocate': (874, 575, 190, 157),
    'collectMail': (626, 1518, 305, 102),
    'backMenu': (0, 1720, 150, 200),

    'friends': (880, 754, 178, 168),
    'sendrecieve': (750, 1560, 306, 100),
    
    'exitMerc': (912, 420, 129, 108),

    'fastrewards': (872, 1612, 130, 106),
    'closeFR': (266, 1218, 236, 92),
    

    'challengeAoH': (294, 1738, 486, 140),
    'attackAoH': (714, 654, 180, 606),
    'battleAoH': (294, 1760, 494, 148),
    'skipAoH': (650, 1350, 200, 200),
    'defeat': (116, 720, 832, 212),

    'exitAoH': (930, 318, 126, 132),

}

def collectAFKRewards():
    printBlue('Attempting AFK Reward collection')
    confirmLocation('campaign', region=boundries['campaignSelect'])
    if (isVisible('buttons/campaign_selected', region=boundries['campaignSelect'])):
        clickXY(550, 1550)
        click('buttons/collect', 0.8, region=boundries['collectAfk'])
        clickXY(550, 1800, seconds=1) # Click campaign in case we level up
        clickXY(550, 1800, seconds=1) # again for the time limited deal popup
        clickXY(550, 1800, seconds=1) # 3rd to be safe
        printGreen('    AFK Rewards collected!')
    else:
        printError('AFK Rewards chests not found!')
        recover()

def collectMail():
    printBlue('Attempting mail collection')
    if isVisible('buttons/mail',  region=boundries['mailLocate']):
        if (pixelCheck(1012, 610, 0) > 240): # We check if the pixel where the notification sits has a red value of higher than 240
            clickXY(960, 630, seconds=2) # Click Mail
            click('buttons/collect_all', seconds=3, region=boundries['collectMail'])
            clickXY(550, 1600) # Clear any popups
            click('buttons/back', region=boundries['backMenu'])
            printGreen('    Mail collected!')
        else:
            printWarning('    Mail notification not found')
    else:
        printError('Mail icon not found!')

def collectCompanionPoints(mercs=False):
    printBlue('Attempting to send/receive companion points')
    if isVisible('buttons/friends', region=boundries['friends']):
        if (pixelCheck(1012, 790, 0) > 240):  # We check if the pixel where the notification sits has a red value of higher than 240
            clickXY(960, 810)
            click('buttons/sendandreceive', region=boundries['sendrecieve'])
            if mercs is True:
                clickXY(720, 1760) # Short term
                clickXY(990, 190) # Manage
                clickXY(630, 1590) # Apply
                clickXY(750, 1410) # Auto lend
                click('buttons/exitmenu', region=boundries['exitMerc'])
                printGreen('    Mercenaries lent out')
            click('buttons/back', region=boundries['backMenu'])
            printGreen('    Friends Points Sent')
        else:
            printWarning('    Friends notification not found')

def collectFastRewards(count):
    printBlue('Attempting to collecting Fast Rewards ' + str(count) + 'x times')
    counter = 0
    confirmLocation('campaign', region=boundries['campaignSelect'])
    if isVisible('buttons/fastrewards', region=boundries['fastrewards']):
        if (pixelCheck(980, 1620, 0) > 220):  # We check if the pixel where the notification sits has a red value of higher than 240
            clickXY(950, 1660)
            while counter < count:
                clickXY(710, 1260)
                wait(1)
                clickXY(550, 1800)
                counter = counter + 1
            click('buttons/close', region=boundries['closeFR'])
            printGreen('    Fast Rewards Done')
        else:
            printWarning('    Fast Rewards already done')
    else:
        printError('    Fast Rewards icon not found!')

# Loads and exits a campaign abttle for dailies quest
def attemptCampaign():
    printBlue('Attempting Campaign battle')
    confirmLocation('campaign', region=boundries['campaignSelect'])
    click('buttons/begin', seconds=2, retry=3, region=boundries['begin'])

    # Multi Battle
    if isVisible('buttons/begin', 0.7, retry=3, seconds=2, click=True, region=boundries['multiBegin']): # If we see second Begin it's a multi so we take different actions
        click('buttons/beginbattle', retry=3, seconds=3, region=boundries['battle'])
        click('buttons/pause', retry=3, region=boundries['pauseBattle']) # 3 retries as ulting heroes can cover the button
        click('buttons/exitbattle', retry=3, region=boundries['exitBattle'])
        click('buttons/back', retry=3, seconds=4, suppress=True, region=boundries['backMenu'])
    else: # Single Battle
        click('buttons/battle', 0.8, retry=3, seconds=3, region=boundries['battle'])
        click('buttons/pause', 0.8, retry=3, region=boundries['pauseBattle']) # 3 retries as ulting heroes can cover the button
        click('buttons/exitbattle', seconds=4, region=boundries['exitBattle'])

    if confirmLocation('campaign', bool=True, region=boundries['campaignSelect']):
        printGreen('    Campaign attempted successfully')
    else:
        printError('    Something went wrong, attempting to recover')
        recover()

def pushCampaign(formation=3, duration=1):
    # Below we open campaign, load the selected formation and start autobattle
    if (isVisible('buttons/begin', 0.7, retry=3, click=True)):
        # Check for a second Begin in the case of a multibattle
        click('buttons/begin_plain', 0.7, seconds=2, retry=3, suppress=True, region=boundries['multiBegin'])
        configureBattleFormation(formation)
    else:
        printError('Can\t find the begin button!')
        sys.exit(1)
    wait((duration * 60) - 30) # Sleep for the wait duration
    clickXY(550, 1750) # Click to prompt the AutoBattle popup
    if isVisible('labels/autobattle', region=boundries['autobattleLabel']): # Make sure the popup is visible (else we've crashed and quit)
        if isVisible('labels/autobattle_0', region=boundries['autobattle0']): # If it's 0 continue
            if config.get('PUSH', 'suppressSpam') is False:
                printWarning('No victory found, checking again in ' + str(config.get('PUSH', 'victoryCheck') + ' minutes.'))
            click('buttons/cancel', retry=3, suppress=True, region=boundries['cancelAB'])
        else: # If it's not 0 we have passed a stage
            printGreen('Victory found! Loading the ' + str(config.get('PUSH', 'formation') + ' formation for the current stage..'))
            click('buttons/exit', suppress=True, retry=3, region=boundries['exitAB'])
            click('buttons/pause', confidence=0.8, retry=3, suppress=True, region=boundries['pauseBattle'])  # 3 retries as ulting heroes can cover the button
            click('buttons/exitbattle', suppress=True, retry=3, region=boundries['exitBattle'])
            click('labels/taptocontinue', confidence=0.8, suppress=True, grayscale=True, region=boundries['taptocontinue'])
            if (isVisible('buttons/begin', 0.7, retry=3, click=True, seconds=2)):
                # Check for a second Begin in the case of a multibattle
                click('buttons/begin_plain', 0.7, seconds=2, retry=3, suppress=True, region=boundries['multiBegin'])
            configureBattleFormation(formation)
    else:
        # If we click and the AutoBattle Label isn't visible we're lost somewhere so we exit
        printError('AutoBattle screen not found, exiting..')
        sys.exit(1)

def configureBattleFormation(formation):
    if isVisible('buttons/formations', click=True, seconds=3, region=boundries['formations']):
        clickXY(800, 1650, seconds=2)  # Change to 'Popular' tab
        clickXY(850, 425 + (formation * 175))
        click('buttons/use', suppress=True, retry=3, region=boundries['useAB'])
        click('buttons/confirm_small', suppress=True, retry=3, region=boundries['confirmAB'])
        click('buttons/autobattle', suppress=True, retry=3, region=boundries['autobattle'])  # So we don't hit it in the background while autobattle is active
        # Sometimes Activate is reported as clicked, but it isn't so this failsafe improves stability
        while isVisible('labels/autobattle', region=boundries['autobattleLabel']):
            click('buttons/activate', suppress=True, retry=3, region=boundries['activateAB'])
    else:
        printWarning('Could not find Formations button')

# Handles the Bounty Board, calls dispatchSoloBounties() to handle solo dust/diamond recognition and dispatching
def handleBounties():
    printBlue('Handling Bounty Board')
    confirmLocation('darkforest', region=boundries['darkforestSelect'])
    clickXY(600, 1320)
    if (isVisible('labels/bountyboard')):
        clickXY(650, 1700) # Solo tab
        click('buttons/collect_all', seconds=2, suppress=True)
        wait(2)
        if config.getboolean('BOUNTIES', 'dispatchDust') is True or config.getboolean('BOUNTIES', 'dispatchDiamonds') is True:
            dispatchSoloBounties(remaining=config.getint('BOUNTIES', 'remaining'), maxRefreshes=config.getint('BOUNTIES', 'refreshes'))
        clickXY(950, 1700) # Team tab
        click('buttons/collect_all', seconds=2, suppress=True)
        click('buttons/dispatch', confidence=0.8, suppress=True, grayscale=True)
        click('buttons/confirm', suppress=True)
        click('buttons/back', region=boundries['backMenu'])
        printGreen('    Bounties attempted successfully')
    else:
        printError('    Bounty Board not found, attempting to recover')
        recover()

# Returns all found instances of the `Dispatch` button then checks pixel colour at an offset to see which resource it is
def dispatchSoloBounties(remaining=2, maxRefreshes=3):
    refreshes = 0
    while refreshes <= maxRefreshes:
        if refreshes > 0:
            printWarning('   Board refreshed (#' + str(refreshes) + ')')
        dispatches = returnDispatchButtons()
        dispatcher(dispatches) # Send the list to the function to dispatch
        swipe(550, 800, 550, 500, duration=200, seconds=2) # scroll down
        dispatches = returnDispatchButtons(scrolled=True)
        if len(dispatches) <= remaining: # if <=remaining bounties left we just dispatch all and continue
            printWarning('  ' + str(remaining) + ' or less bounties remaining, dispatching..')
            click('buttons/dispatch', confidence=0.8, suppress=True, grayscale=True)
            click('buttons/confirm', suppress=True)
            return
        dispatcher(dispatches) # Send the list to the function to dispatch
        if refreshes < maxRefreshes:
            clickXY(90, 250)
            clickXY(700, 1250)
        refreshes += 1
    print(str(maxRefreshes) + ' refreshes done, dispatching remaining..')
    click('buttons/dispatch', confidence=0.8, suppress=True, grayscale=True)
    click('buttons/confirm', suppress=True)

# Recieves a list of Dispatch buttons and checks/dispatches the resource
def dispatcher(dispatches):
    # print(str(len(dispatches)) + ' Dispatches found.') # Debugging
    for button in dispatches:
        blue_value = pixelCheck(190, button, 2, seconds=0) # Take a reading from the border of the icon
        # green_value = pixelCheck(190, y_center, 1, seconds=0) # Take a reading from the middle of the icon
        red_value = pixelCheck(190, button, 0, seconds=0) # Take a reading from the border of the icon
        # printWarning('Blue: ' + str(blue_value) + '. Red: ' + str(red_value) + '.') # Debugging
        if blue_value < 100 and red_value > 100:
            # printGreen('    Skipping Gold')
            # Gold
            continue
        elif blue_value > 215 and red_value > 100 and red_value < 120:
            # printGreen('    Skipping Soulstone')
            # Soulstone
            continue
        elif blue_value >= 205 and red_value >= 150 and red_value <= 165:
            # Dust
            if config.getboolean('BOUNTIES', 'dispatchDust'):
                printGreen('    Dispatching Dust')
                clickXY(900, button)
                clickXY(350, 1150)
                clickXY(750, 1150)
        elif blue_value >= 200 and red_value >= 200:
            # Diamonds
            if config.getboolean('BOUNTIES', 'dispatchDiamonds'):
                printGreen('    Dispatching Diamonds')
                clickXY(900, button)
                clickXY(350, 1150)
                clickXY(750, 1150)

def handleArenaOfHeroes(count):
    counter = 0
    printBlue('Battling Arena of Heroes ' + str(count) + ' times')
    confirmLocation('darkforest', region=boundries['darkforestSelect'])
    clickXY(740, 1050)
    clickXY(550, 50)
    if isVisible('labels/arenaofheroes_new'): # The label font changes for reasons
        click('labels/arenaofheroes_new', suppress=True)
        click('buttons/challenge', retry=3, region=boundries['challengeAoH']) # retries for animated button
        while counter < count:
            wait(1) # To avoid error when clickMultipleChoice returns no results
            selectArenaOpponent(choice=4)
            # clickMultipleChoice('buttons/arenafight', count=4, confidence=0.98, region=boundries['attackAoH'], seconds=3) # Select 4th opponent
            if isVisible('buttons/heroclassselect', retry=3, region=boundries['heroclassselect']): # This is rather than Battle button as that is animated and hard to read
                clickXY(550, 1800, seconds=3)
            click('buttons/skip', retry=5, confidence=0.8, suppress=True, region=boundries['skipAoH']) # Retries as ulting heros can cover the button
            if returnBattleResults(type='arena'):
                printGreen('    Battle #' + str(counter+1) + ' Victory!')
                clickXY(600, 550) # Clear loot popup
            else:
                printError('    Battle #' + str(counter + 1) + ' Defeat!')
            clickXY(600, 550)  # Back to opponent selection
            counter = counter+1
        click('buttons/exitmenu', region=boundries['exitAoH'])
        click('buttons/back', retry=3, region=boundries['backMenu'])
        click('buttons/back', retry=3, region=boundries['backMenu'])
        printGreen('    Arena battles complete')
    else:
        printError('Arena of Heroes not found, attempting to recover')
        recover()

def collectGladiatorCoins():
    printBlue('Collecting Gladiator Coins')
    confirmLocation('darkforest', region=boundries['darkforestSelect'])
    clickXY(740, 1050)
    clickXY(550, 50)
    if isVisible('labels/legendstournament_new'): # The label font changes for reasons
        click('labels/legendstournament_new', suppress=True)
        clickXY(550, 300, seconds=2)
        clickXY(50, 1850)
        click('buttons/back', region=boundries['backMenu'])
        click('buttons/back', region=boundries['backMenu'])
        printGreen('    Gladiator Coins collected')
    else:
        printError('    Legends Tournament not found, attempting to recover')
        recover()

def collectFountainOfTime():
    printBlue('Collecting Fountain of Time')
    confirmLocation('darkforest', region=boundries['darkforestSelect'])
    clickXY(800, 700, seconds=6)
    clickXY(800, 700, seconds=1)
    if isVisible('labels/temporalrift'):
        clickXY(550, 1800)
        clickXY(250, 1300)
        clickXY(700, 1350) # Collect
        clickXY(550, 1800, seconds=3) # Clear level up
        clickXY(550, 1800, seconds=3) # Clear limited deal
        clickXY(550, 1800, seconds=3) # Clear newly unlocked
        click('buttons/back', region=boundries['backMenu'])
        printGreen('    Fountain of Time collected')
    else:
        printError('    Temporal Rift not found, attempting to recover')
        recover()

def openTower(name):
    printBlue('Opening ' + name + '.')
    confirmLocation('darkforest', region=boundries['darkforestSelect'])
    wait(3) # Medium wait to make sure tower button is active when we click
    clickXY(500, 870, seconds=3) # Long pause for animation opening towers
    if isVisible('labels/kingstower', region=boundries['kingstowerLabel']):
        towers = {"King's Tower": [500, 870], "Lightbringer Tower": [300, 1000], "Wilder Tower": [800, 600], "Mauler Tower": [400, 1200],
                  "Graveborn Tower": [800, 1200], "Hypogean Tower": [600, 1500], "Celestial Tower": [300, 500]}
        for tower, location in towers.items():
            if tower == name:
                clickXY(location[0], location[1], seconds=3)

def pushTower(formation=3, duration=1):
    # TODO Add another icon here
    if isVisible('buttons/challenge_plain', 0.8, retry=3, seconds=3, click=True, region=boundries['challengeTower']):  # lower confidence and retries for animated button
        configureBattleFormation(formation)
    if isVisible('buttons/autobattle', 0.95, retry=3, seconds=2, click=True, region=boundries['autobattle']):  # higher confidence so we don't find it in the background
        configureBattleFormation(formation)
    wait((duration * 60)-30)
    clickXY(550, 1750)
    if isVisible('labels/autobattle', retry=2, region=boundries['autobattleLabel']): # Make sure the popup is visible
        if isVisible('labels/autobattle_0', retry=3, region=boundries['autobattle0']): # If it's 0 continue
            if bool(config.get('PUSH', 'suppressspam')) is False:
                printWarning('No victory found, checking again in ' + str(config.get('PUSH', 'victoryCheck') + ' minutes.'))
            click('buttons/cancel', retry=3, suppress=True, region=boundries['cancelAB'])
        else: # If it's not 0 we have passed a stage
            printGreen('Victory found! Loading the ' + str(config.get('PUSH', 'formation') + ' formation for the current stage..'))
            click('buttons/exit', retry=3, suppress=True, region=boundries['exitAB'])
            click('buttons/pause', 0.8, retry=3, suppress=True, region=boundries['pauseBattle'])  # 3 retries as ulting heroes can cover the button
            click('buttons/exitbattle', retry=2, suppress=True, region=boundries['exitBattle'])
            click('labels/taptocontinue', retry=2, confidence=0.8, suppress=True, grayscale=True, region=boundries['taptocontinue'])
    else:
        printError('AutoBattle screen not found, exiting..')
        sys.exit(1)
        buttonState('enabled')


def handleKingsTower():
    printBlue('Attempting Kings Tower battle')
    confirmLocation('darkforest', region=boundries['darkforestSelect'])
    clickXY(500, 870, seconds=3) # Long pause for animation
    if isVisible('labels/kingstower'):
        clickXY(555, 585)
        click('buttons/challenge_plain', 0.7, retry=5, suppress=True, seconds=5) # lower confidence and retries for animated button
        # For reasons sometimes this button is 'beginbattle' and sometimes it is 'begin', so we use clickXY
        clickXY(700, 1850, seconds=2)
        # click('buttons/beginbattle', 0.8, seconds=3, retry=5)
        click('buttons/pause', 0.8, retry=5, suppress=True)
        click('buttons/exitbattle')
        click('buttons/back', retry=3, region=boundries['backMenu'])
        click('buttons/back', retry=3, region=boundries['backMenu'])
        if isVisible('buttons/back', retry=3, region=boundries['backMenu']):
            click('buttons/back', region=boundries['backMenu']) # Last one only needed for multifights
        printGreen('    Tower attempted successfully')
    else:
        printError('Tower screen not found, attempting to recover')
        recover()

def collectInnGifts():
    clicks = 0
    x_axis = 250
    printBlue('Attempting daily Inn gift collection')
    confirmLocation('ranhorn', region=boundries['ranhornSelect'])
    clickXY(800,290, seconds=4)
    if isVisible('buttons/manage'):
        while clicks < 10: # We spam clicks in the right area and pray
            clickXY(x_axis, 1300, seconds=0.5)
            x_axis = x_axis + 50
            clicks = clicks + 1
            clickXY(550, 1400, seconds=0.5) # Clear loot
        click('buttons/back', region=boundries['backMenu'])
        printGreen('    Inn Gifts collected.')
    else:
        printError('    Inn not found, attempting to recover')
        recover()

def handleShopPurchasing(counter):
    config.read(settings)  # re-load for any updated values
    toprow = {'arcanestaffs': [180, 920], 'cores': [425, 920], 'timegazer': [650, 920], 'baits': [875, 920]}
    bottomrow = {'dust_gold': 'buttons/shop/dust', 'shards_gold': 'buttons/shop/shards_gold', 'dust_diamond': 'buttons/shop/dust_diamonds', 'elite_soulstone': 'buttons/shop/soulstone',
                  'superb_soulstone': 'buttons/shop/superstone', 'silver_emblem': 'buttons/shop/silver_emblems', 'gold_emblem': 'buttons/shop/gold_emblems', 'poe': 'buttons/shop/poe'}

    # Purchase top row
    for item, pos in toprow.items():
        if config.getboolean('SHOP', item):
            if item == 'timegazer' and counter > 0: # only one TG card
                continue
            if item == 'baits' and counter > 1: # only two baits
                continue
            if (item == 'cores' or item == 'arcanestaffs') and counter > 2: # only three shards/staffs
                continue
            printPurple('Buying: ' + item)
            clickXY(pos[0], pos[1])
            click('buttons/shop/purchase', suppress=True)
            clickXY(550, 1220, seconds=2)

    # Scroll down so bottom row is visible
    swipe(550, 1500, 550, 1200, 500, seconds=5)

    # Purchase everything else
    for item, button in bottomrow.items():
        if config.getboolean('SHOP', item):
            printPurple('Buying: ' + item)
            click(button, 0.95, suppress=True)
            click('buttons/shop/purchase', suppress=True)
            clickXY(550, 1220)
    wait(3) # Else we can't find TR after

def shopPurchases(shoprefreshes):
    printBlue('Attempting store purchases (Refreshes: ' + str(shoprefreshes) + ')')
    counter = 0
    confirmLocation('ranhorn', region=boundries['ranhornSelect'])
    wait(2)
    clickXY(300, 1725, seconds=5)
    if isVisible('labels/store'):
        # First purchases
        handleShopPurchasing(counter)
        # refresh purchases
        while counter < shoprefreshes:
            clickXY(1000, 300)
            click('buttons/confirm', suppress=True, seconds=5)
            counter += 1
            printPurple('    Refreshed store ' + str(counter) + ' times.')
            handleShopPurchasing(counter)
        click('buttons/back')
        printGreen('Store purchases attempted.')
    else:
        printError('Store not found, attempting to recover')
        recover()

def handleGuildHunts():
    printBlue('Attempting to run Guild Hunts')
    confirmLocation('ranhorn', region=boundries['ranhornSelect'])
    clickXY(380, 360)
    wait(6)
    clickXY(550, 1800) # Clear chests
    click('buttons/guild_chests', seconds=2)
    if isVisible('buttons/collect_guildchest'):
        click('buttons/collect_guildchest')
        clickXY(550, 1300)
        clickXY(900, 550)
        clickXY(550, 1800)  # Clear window
        wait(1)
    else:
        clickXY(550, 1800)  # Clear window
    clickXY(290, 860)
    # Wrizz check
    if isVisible('labels/wrizz'):
        if (isVisible('buttons/quickbattle')):
            printGreen('    Wrizz Found, collecting')
            click('buttons/quickbattle')
            clickXY(725, 1300)
            # So we don't get stuck on capped resources screen
            if isVisible('buttons/confirm'):
               click('buttons/confirm')
            clickXY(550, 500)
            clickXY(550, 500,seconds=2)
        else:
            printWarning('    Wrizz quick battle not found')
        # Soren Check
        clickXY(970, 890)
        if (isVisible('buttons/quickbattle')):
            printGreen('    Soren Found, collecting')
            click('buttons/quickbattle')
            clickXY(725, 1300)
            # So we don't get stuck on capped resources screen
            if isVisible('buttons/confirm'):
               click('buttons/confirm')
            clickXY(550, 500)
            clickXY(550, 500, seconds=2)
        else:
            printWarning('    Soren quick battle not found')
        clickXY(70, 1810)
        clickXY(70, 1810)
        printGreen('    Guild Hunts checked successfully')
    else:
        printError('    Error opening Guild Hunts, attempting to recover')
        recover()

def collectQuests():
    printBlue('Attempting to collect quest chests')
    clickXY(960, 250)
    if isVisible('labels/quests'):
        clickXY(400, 1650) # Dailies
        if isVisible('labels/questcomplete'):
            printGreen('    Daily Quest(s) found, collecting..')
            clickXY(930, 680, seconds=4) # Click top quest
            click('buttons/fullquestchest', seconds=3, retry=3, suppress=True)
            clickXY(400, 1650)
        clickXY(600, 1650) # Weeklies
        if isVisible('labels/questcomplete'):
            printGreen('    Weekly Quest(s) found, collecting..')
            clickXY(930, 680, seconds=4) # Click top quest
            click('buttons/fullquestchest', seconds=3, retry=3, suppress=True)
            clickXY(600, 1650, seconds=2)
            clickXY(600, 1650)  # Second in case we get Limited Rewards popup
        click('buttons/back', retry=3)
        printGreen('    Quests collected')
    else:
        printError('    Quests screen not found, attempting to recover')
        recover()

def clearMerchant():
    printBlue('Attempting to collect merchant deals')
    clickXY(120, 300, seconds=5)
    swipe(1000, 1825, 100, 1825, 500)
    swipe(1000, 1825, 100, 1825, 500, seconds=3)
    if isVisible('buttons/noblesociety'):
        printPurple('    Collecting Nobles')
        # Nobles
        clickXY(675, 1825)
        if isVisible('buttons/confirm_nobles', 0.8, retry=2):
            printWarning('Noble resource collection screen found, skipping Noble collection')
            clickXY(70, 1810)
        else:
            # Champion
            clickXY(750, 1600) # Icon
            clickXY(440, 1470, seconds=0.5)
            clickXY(440, 1290, seconds=0.5)
            clickXY(440, 1100, seconds=0.5)
            clickXY(440, 915, seconds=0.5)
            clickXY(440, 725, seconds=0.5)
            clickXY(750, 1600) # Icon
            # Twisted
            clickXY(600, 1600) # Icon
            clickXY(440, 1470, seconds=0.5)
            clickXY(440, 1290, seconds=0.5)
            clickXY(440, 1100, seconds=0.5)
            clickXY(440, 915, seconds=0.5)
            clickXY(440, 725, seconds=0.5)
            clickXY(600, 1600) # Icon
            # Regal
            clickXY(450, 1600) # Icon
            clickXY(440, 1470, seconds=0.5)
            clickXY(440, 1290, seconds=0.5)
            clickXY(440, 1100, seconds=0.5)
            clickXY(440, 915, seconds=0.5)
            clickXY(440, 725, seconds=0.5)
            clickXY(450, 1600) # Icon
        # Monthly Cards
        printPurple('    Collecting Monthly Cards')
        clickXY(400, 1825)
        # Monthly
        clickXY(300, 1000, seconds=3)
        clickXY(560, 430)
        # Deluxe Monthly
        clickXY(850, 1000, seconds=3)
        clickXY(560, 430)
        # Daily Deals
        swipe(200, 1825, 450, 1825, 500, seconds=2)
        clickXY(400, 1825)
        # Special Deal
        # if isVisible('buttons/merchant_special', confidence=0.8, click=True):
        printPurple('    Collecting Special Deal')
        click('buttons/dailydeals')
        clickXY(150, 1625)
        # Daily Deal
        if isVisible('buttons/merchant_daily', confidence=0.8, click=True):
            printPurple('    Collecting Daily Deal')
            swipe(550, 1400, 550, 1200, 500, seconds=3)
            click('buttons/dailydeals')
            clickXY(400, 1675, seconds=2)
        # Biweeklies
        if d.isoweekday() == 3: # Wednesday
            if isVisible('buttons/merchant_biweekly', confidence=0.8, click=True):
                printPurple('    Collecting Biweekly Deal')
                swipe(300, 1400, 200, 1200, 500, seconds=3)
                clickXY(200, 1200)
                clickXY(550, 1625, seconds=2)
        # Yuexi
        if d.isoweekday() == 1: # Monday
            print('    Collecting Yuexi')
            clickXY(200, 1825)
            clickXY(240, 880)
            clickXY(150, 1625, seconds=2)
        # Clear Rhapsody bundles
        printPurple('    Clearing Rhapsody notification')
        clickXY(200, 1825)
        clickXY(620, 1600)
        clickXY(980, 200)
        clickXY(70, 1810)
        clickXY(70, 1810)
        printGreen('    Merchant deals collected')
    else:
        printError('    Noble screen not found, attempting to recover')
        recover()

def handleTwistedRealm():
    printBlue('Attempting to run Twisted Realm')
    confirmLocation('ranhorn', region=boundries['ranhornSelect'])
    clickXY(380, 360, seconds=6)
    clickXY(550, 1800) # Clear chests
    clickXY(775, 875, seconds=2)
    clickXY(550, 600, seconds=3)
    if isVisible('buttons/nextboss'):
        printGreen('    Twisted Realm found, battling')
        if isVisible('buttons/challenge_tr', retry=3, confidence=0.8):
            clickXY(550, 1850, seconds=2)
            click('buttons/autobattle')
            if not (isVisible('labels/skipbattle_Active')):
                clickXY(300, 975)  # Activate Skip Battle Animations
            clickXY(700, 1300, seconds=6)
            clickXY(550, 1300)
            clickXY(550, 1800)
            clickXY(70, 1800)
            clickXY(70, 1800)
            clickXY(70, 1800)
            printGreen('    Twisted Realm attempted successfully')
        else:
            clickXY(70, 1800)
            clickXY(70, 1800)
            printError('    Challenge button not found, attempting to recover')
    else:
        printError('    Error opening Twisted Realm, attempting to recover')
        recover()

def handleFightOfFates(battles=3):
    printBlue('Attempting to run Fight of Fates ' + str(battles) + ' times')
    counter = 0
    click('buttons/fightoffates', confidence=0.8, retry=5, seconds=3)
    if isVisible('labels/fightoffates'):
        while counter < battles:
            click('buttons/challenge_tr', confidence=0.8, suppress=True, retry=3, seconds=15)
            while not isVisible('labels/fightoffates', confidence=0.95):
                # Hero
                swipe(200, 1700, 290, 975, 200)
                # Skill 1
                swipe(450, 1700, 550, 950, 200)
                # Hero
                swipe(200, 1700, 290, 975, 200)
                # Skill 2
                swipe(600, 1700, 550, 950, 200)
                # Hero
                swipe(200, 1700, 290, 975, 200)
                # Skill 3
                swipe(800, 1700, 550, 950, 200)
            counter = counter + 1
            printGreen('    Fight of Fates Battle #' + str(counter) + ' complete')
        # Click quests
        clickXY(975, 125, seconds=2)
        # select dailies tab
        clickXY(650, 1650, seconds=1)
        # Collect Dailies
        clickXY(940, 680, seconds=2)
        clickXY(980, 435, seconds=2)
        # clear loot
        clickXY(550, 250, seconds=2)
        # Back twice to exit
        clickXY(70, 1650, seconds=1)
        clickXY(70, 1810, seconds=1)
        printGreen('    Fight of Fates attempted successfully')
    else:
        printWarning('Fight of Fates not found, recovering..')
        recover()

# Basic support for dailies quests, we simply choose the 5 cards from the top row of our hand
# Ater starting a battle we read the Stage 1/2/3 text at the top to determine when our opponent has placed their cards and to continue with placing ours
# Timeout is probably 10 seconds longer than the stage timer so if we exceed that something has gone wrong
# A round can take between 40 seconds or over 2 minutes depending on if our opponent is afk or not, at the end we collect daily quests
def handleBattleofBlood(battles=3):
    printBlue('Attempting to run Battle of Blood ' + str(battles) + ' times')
    battlecounter = 0 # Number of battles we want to run
    bob_timeout = 0 # Timer for tracking if something has gone wrong with placing cards
    click('buttons/events', confidence=0.8, retry=3, seconds=3)
    if isVisible('labels/battleofblood_event_banner', click=True):
        while battlecounter < battles:
            click('buttons/challenge_tr', confidence=0.8, suppress=True, retry=3, seconds=7)
            # Place cards 1-2, click ready
            while not isVisible('labels/battleofblood_stage1', region=(465, 20, 150, 55)):
                wait(1)
                bob_timeout += 1
                if bob_timeout > 30:
                    printError('Battle of Blood timeout!')
                    return
            else:
                wait(4) # For the card animations
                bob_timeout = 0 # reset timer
                clickXY(550, 1250, seconds=1)
                clickXY(350, 1250, seconds=1)
                clickXY(550, 1850, seconds=1)
            if isVisible('buttons/confirm_small', retry=3, region=(600, 1220, 200, 80)):
                clickXY(325, 1200)
                clickXY(700, 1270)
            # Place cards 3-4, click ready
            while not isVisible('labels/battleofblood_stage2', region=(465, 20, 150, 55)):
                wait(1)
                bob_timeout += 1
                if bob_timeout > 30:
                    printError('Battle of Blood timeout!')
                    return
            else:
                wait(4) # For the card animations
                bob_timeout = 0 # reset timer
                clickXY(550, 1250, seconds=1)
                clickXY(350, 1250, seconds=1)
                clickXY(550, 1850, seconds=1)
            # Place card 5, click ready
            while not isVisible('labels/battleofblood_stage3', region=(465, 20, 150, 55), confidence=0.95): # higher confidence so we don't get confused with battleofblood_stage2.png
                wait(1)
                bob_timeout += 1
                if bob_timeout > 30:
                    printError('Battle of Blood timeout!')
                    return
            else:
                wait(4) # For the card animations
                bob_timeout = 0 # reset timer
                clickXY(550, 1250, seconds=1)
                clickXY(550, 1850, seconds=8)
                # Return Battle Report
                battlecounter += 1
                result = returnBattleResults('BoB')
                if result is True:
                    printGreen('    Victory! Battle of Blood Battle #' + str(battlecounter) + ' complete')
                else:
                    printError('    Defeat! Battle of Blood Battle #' + str(battlecounter) + ' complete')
        # Click quests
        clickXY(150, 230, seconds=2)
        # select dailies tab
        clickXY(650, 1720, seconds=1)
        # Collect Dailies
        clickXY(850, 720, seconds=3)
        clickXY(920, 525, seconds=2)
        clickXY(920, 525, seconds=2)
        # clear loot
        clickXY(550, 250, seconds=2)
        # Back twice to exit
        clickXY(70, 1810, seconds=1) # Exit Quests
        clickXY(70, 1810, seconds=1) # Exit BoB
        clickXY(70, 1810, seconds=1) # Exit Events screen
        printGreen('    Battle of Blood attempted successfully')
    else:
        printWarning('Battle of Blood not found, recovering..')
        recover()

def handleCircusTour(battles = 3):
    counter = 1
    printBlue('Attempting to run Circus Tour battles')
    confirmLocation('ranhorn', region=boundries['ranhornSelect']) # Trying to fix 'buttons/events not found' error
    wait()
    click('buttons/events', confidence=0.8, retry=3, seconds=3)
    if isVisible('labels/circustour', retry=3, click=True):
        while counter < battles:
            printGreen('    Circus Tour battle #' + str(counter))
            click('buttons/challenge_tr', confidence=0.8, retry=3, seconds=3)
            if counter == 1:
                clickXY(550, 900, seconds=1) # Clear dialogue box on new boss rotation
                clickXY(550, 900, seconds=1) # Only need to do this on the first battle
                clickXY(550, 900, seconds=1)
                clickXY(550, 900, seconds=1)
                clickXY(550, 900, seconds=1)
                clickXY(550, 900, seconds=1)
            click('buttons/battle_large', confidence=0.8, retry=3, seconds=5)
            click('buttons/skip', confidence=0.8, retry=5, seconds=5)
            clickXY(550, 1800)
            counter += 1
        wait(3)
        clickXY(500, 1600)
        clickXY(500, 1600) # Twice to clear loot popup
        clickXY(900, 1600)
        clickXY(900, 1600) # Twice to clear loot popup
        # Back twice to exit
        clickXY(70, 1810, seconds=1)
        clickXY(70, 1810, seconds=1)
    else:
        printWarning('Circus Tour not found, recovering..')
        recover()

def infiniteSummons(woke, celehypo, x6mode=False):
    printBlue('Attempting to run Unlimited Summons')
    counter = 0 # Pull amount counter
    starttime = time.time() # Pull duration counter
    if not isVisible('buttons/summons/summons_sidebar'):
        printWarning('Can\'t see the summons event button, scrolling the side menu down..')
        swipe(50, 800, 50, 500, duration=500, seconds=1)  # scroll down
    if isVisible('buttons/summons/summons_sidebar', retry=3, click=True):
        # List to match the dropdown name to the image file name
        wokes = {'Awakened Talene': 'aTalene', 'Gavus': 'Gavus', 'Maetria': 'Maetria', 'Awakened Ezizh': 'aEzizh',
                 'Awakened Thane': 'aThane', 'Awakened Belinda': 'aBelinda', 'Awakened Brutus': 'aBrutus',
                 'Awakened Safiya': 'aSafiya', 'Awakened Lyca': 'aLyca', 'Awakened Solise': 'aSolise',
                 'Awakened Baden': 'aBaden', 'Awakened Shemira': 'aShemira', 'Awakened Athalia': 'aAthalia'}
        # List to match the dropdown name to the image file name
        celehypos = {'Audrae': 'audrae', 'Canisa and Ruke': 'cruke', 'Daemia': 'daemia', 'Ezizh': 'ezizh', 'Khazard': 'khazard',
                 'Lavatune': 'lavatune', 'Liberta': 'liberta', 'Lucilla': 'lucilla', 'Lucretia': 'lucretia', 'Mehira': 'mehira',
                 'Mezoth': 'mezoth', 'Mortas': 'mortas', 'Olgath': 'olgath', 'Talene': 'talene', 'Tarnos': 'tarnos',
                     'Elijah and Lailah': 'twins', 'Veithael': 'vei', 'Vyloris': 'vyloris', 'Zahprael': 'zaph', 'Zikis': 'zikis'}

        search = True
        printGreen('Searching for: ' + woke + ' and ' + celehypo)
        print('')
        clickXY(700, 1700, seconds=2) # Click 'Summon Again'
        while search is True:
            if x6mode is False: # Self-explanatory, if x6 mode is enabled we click a little faster, else slower
                clickXY(680, 1820, seconds=2)
                clickXY(950, 1820)
                clickXY(950, 1820)
                wait(6)
            else:
                clickXY(680, 1820)
                clickXY(950, 1820, seconds=0.5)
                clickXY(950, 1820, seconds=0.5)
                wait(2)
            # return Awakened, Epic or Rare
            found = str(returnCardPullsRarity())
            counter += 1
            if found == "Awakened":
                printWarning('Awakened Found')
                if summonsCrashDetector('awakened'):
                    return
                # Let's check if it's the one we want
                if isVisible(os.path.join('summons', 'awakeneds', wokes[woke]), confidence=0.85, seconds=0.5):
                    printGreen('    ' + woke + ' found! Checking for ' + celehypo)
                    # If it is we then check the celeypo
                    if isVisible(os.path.join('summons', 'celehypos', celehypos[celehypo]), confidence=0.85):
                        printGreen('    ' + celehypo + ' found too! Recording Summon and exiting..')
                        click('buttons/summons/record', confidence=0.85, retry=3, seconds=3)
                        click('buttons/summons/change', confidence=0.85, retry=3, seconds=3, suppress=True) # Suppress as this isn't always present
                        click('buttons/summons/confirm', confidence=0.85, retry=3, seconds=3, suppress=True)# Suppress as this isn't always present
                        search = False
                    else:
                        printError('    ' + celehypo + ' not found, continuing..')
            if found == 'Epic':
                if summonsCrashDetector('epic'):
                    return
                printPurple('Epic Found')
            if found == 'Rare':
                if summonsCrashDetector('rare'):
                    return
                printBlue('Rare found')
        # Funky math for duration calculation, ceiling is used to roundup else it returns with a decimal place
        duration = time.time() - starttime
        hours = str(ceil(duration // 3600))
        minutes = str((ceil(duration // 60)) - (int(hours) * 60))
        printGreen('Unlimited Summons finished!')
        printGreen('In just ' + str(counter) + ' pulls and ' + hours + ' hours ' + minutes + ' minutes. Hooray!')
    else:
        # If we can't find the Unlimited Summons button we end
        printError('Could not find Unlimited Summons button..')

# Counts if we get 10 of the same type in a row, which indicates the game has crashed or frozen and exits
def summonsCrashDetector(type):
    global rarecounter
    global epiccounter
    global awakenedcounter

    if type == 'rare':
        rarecounter += 1
        epiccounter = 0
        awakenedcounter = 0
    elif type == 'epic':
        rarecounter = 0
        epiccounter += 1
        awakenedcounter = 0
    elif type == 'awakened':
        rarecounter = 0
        epiccounter = 0
        awakenedcounter += 1

    if rarecounter >= 10 or epiccounter >= 10 or awakenedcounter >= 10:
        printError('10 of the same type in a row, this normally means something has gone wrong, exiting..')
        recover()
        rarecounter = 0
        epiccounter = 0
        awakenedcounter = 0
        return True

def handleLab():
    printBlue('Attempting to run Arcane Labyrinth')
    lowerdirection = '' # for whether we go left or right for the first battle
    upperdirection = '' # For whether we go left or right to get the double battle at the end
    confirmLocation('darkforest', region=boundries['darkforestSelect'])
    wait()
    clickXY(400, 1150, seconds=3)
    if isVisible('labels/labfloor3', retry=3, confidence=0.8, seconds=3):
        printGreen('Lab already ran! Continuing..')
        clickXY(50, 1800, seconds=2)  # Exit Lab Menu
        return
    if isVisible('labels/lab', retry=3):
        # Check for Swept
        if isVisible('labels/labswept', retry=3, confidence=0.8, seconds=3):
            printGreen('Lab already ran! Continuing..')
            clickXY(50, 1800, seconds=2)  # Exit Lab Menu
            return
        # Check for Sweep
        if isVisible('buttons/labsweep', retry=3, confidence=0.8, click=True, seconds=3):
            printGreen('    Sweep Available!')
            if isVisible('buttons/labsweepbattle', retry=3, confidence=0.8, click=True, seconds=3):
                clickXY(720, 1450, seconds=3) # Click Confirm
                clickXY(550, 1550, seconds=3) # Clear Rewards
                if isVisible('labels/notice', retry=3, seconds=3):  # And again for safe measure
                    clickXY(550, 1250)
                clickXY(550, 1550, seconds=5) # Clear Roamer Deals, long wait for the Limited Offer to pop up for Lab completion
                clickXY(550, 1650) # Clear Limited Offer
                printGreen('    Lab Swept!')
                return
        else: # Else we run lab manually
            printGreen('    Sweep not found, attempting manual Lab run..')

            # Pre-run set up
            printGreen('    Entering Lab')
            clickXY(750, 1100, seconds=2) # Center of Dismal
            clickXY(550, 1475, seconds=2) # Challenge
            clickXY(550, 1600, seconds=2) # Begin Adventure
            clickXY(700, 1250, seconds=6) # Confirm
            clickXY(550, 1600, seconds=3) # Clear Debuff
            # TODO Check Dismal Floor 1 text
            printGreen('    Sweeping to 2rd Floor')
            clickXY(950, 1600, seconds=2) # Level Sweep
            clickXY(550, 1550, seconds=8) # Confirm, long wait for animations
            clickXY(550, 1600, seconds=2) # Clear Resources Exceeded message
            clickXY(550, 1600, seconds=2) # And again for safe measure
            clickXY(550, 1600, seconds=3) # Clear Loot
            clickXY(550, 1250, seconds=5) # Abandon Roamer
            printGreen('    Choosing relics')
            clickXY(550, 900) # Relic 1
            clickXY(550, 1325, seconds=3) # Choose
            clickXY(550, 900) # Relic 2
            clickXY(550, 1325, seconds=3) # Choose
            clickXY(550, 900) # Relic 3
            clickXY(550, 1325, seconds=3) # Choose
            clickXY(550, 900) # Relic 4
            clickXY(550, 1325, seconds=3) # Choose
            clickXY(550, 900) # Relic 5
            clickXY(550, 1325, seconds=3) # Choose
            clickXY(550, 900) # Relic 6
            clickXY(550, 1325, seconds=3) # Choose
            printGreen('    Entering 3rd Floor')
            clickXY(550, 550, seconds=2) # Portal to 3rd Floor
            clickXY(550, 1200, seconds=5) # Enter
            clickXY(550, 1600, seconds=2) # Clear Debuff
            # TODO Check Dismal Floor 3 text

            # Check which route we are taking, as to avoid the cart
            clickXY(400, 1400, seconds=2) # Open first tile on the left
            if isVisible('labels/labguard', retry=2):
                printWarning('    Loot Route: Left')
                lowerdirection = 'left'
            else:
                printWarning('    Loot Route: Right')
                lowerdirection = 'right'
                clickXY(550, 50, seconds=3)  # Back to Lab screen

            # 1st Row (single)
            handleLabTile('lower', lowerdirection, '1')
            if isVisible('buttons/heroclassselect', retry=3):  # Check we're at the battle screen
                configureLabTeams(1)
                clickXY(550, 1850, seconds=4)  # Battle
            else:
                printError('Battle Screen not found! Exiting')
                recover()
                return
            if returnBattleResults(type='lab') is False:
                return

            # 2nd Row (multi)
            handleLabTile('lower', lowerdirection, '2')
            if isVisible('buttons/heroclassselect', retry=3):  # Check we're at the battle screen
                clickXY(550, 1850, seconds=4) # Battle
            else:
                printError('Battle Screen not found! Exiting')
                recover()
                return
            if returnBattleResults(type='lab', firstOfMulti=True) is False:
                return
            clickXY(750, 1725, seconds=4) # Continue to second battle
            if isVisible('buttons/heroclassselect', retry=3):  # Check we're at the battle screen
                configureLabTeams(2)
                clickXY(550, 1850, seconds=4) # Battle
            else:
                printError('Battle Screen not found! Exiting')
                recover()
                return
            if returnBattleResults(type='lab') is False:
                return

            # 3rd Row (single relic)
            handleLabTile('lower', lowerdirection, '3')
            if isVisible('buttons/heroclassselect', retry=3):  # Check we're at the battle screen
                clickXY(550, 1850, seconds=4) # Battle
            else:
                printError('Battle Screen not found! Exiting')
                recover()
                return
            if returnBattleResults(type='lab') is False:
                return
            clickXY(550, 1350, seconds=2) # Clear Relic reward

            # 4th Row (multi)
            handleLabTile('lower', lowerdirection, '4')
            if isVisible('buttons/heroclassselect', retry=3):  # Check we're at the battle screen
                clickXY(550, 1850, seconds=4) # Battle
            else:
                printError('Battle Screen not found! Exiting')
                recover()
                return
            if returnBattleResults(type='lab', firstOfMulti=True) is False:
                return
            clickXY(750, 1725, seconds=4) # Continue to second battle
            if isVisible('buttons/heroclassselect', retry=3):  # Check we're at the battle screen
                clickXY(550, 1850, seconds=4) # Battle
            else:
                printError('Battle Screen not found! Exiting')
                recover()
                return
            if returnBattleResults(type='lab') is False:
                return

            # 5th Row (single)
            handleLabTile('lower', lowerdirection, '5')
            if isVisible('buttons/heroclassselect', retry=3):  # Check we're at the battle screen
                clickXY(550, 1850, seconds=4) # Battle
            else:
                printError('Battle Screen not found! Exiting')
                recover()
                return
            if returnBattleResults(type='lab') is False:
                return

            # 6th Row (single relic)
            handleLabTile('lower', lowerdirection, '6')
            if isVisible('buttons/heroclassselect', retry=3):  # Check we're at the battle screen
                clickXY(550, 1850, seconds=4) # Battle
            else:
                printError('Battle Screen not found! Exiting')
                recover()
                return
            if returnBattleResults(type='lab') is False:
                return
            clickXY(550, 1350, seconds=2) # Clear Relic reward

            # Check which route we are taking for the upper tiles
            swipe(550, 200, 550, 1800, duration=1000)
            clickXY(400, 1450, seconds=2) # First tile on the left
            if isVisible('labels/labpraeguard', retry=2):
                printWarning('    Loot Route: Left')
                upperdirection = 'left'
            else:
                printWarning('    Loot Route: Right')
                upperdirection = 'right'
                clickXY(550, 50, seconds=2)  # Back to Lab screen

            # 7th Row (multi)
            handleLabTile('upper', upperdirection, '7')
            if isVisible('buttons/heroclassselect', retry=3):  # Check we're at the battle screen
                clickXY(550, 1850, seconds=4) # Battle
            else:
                printError('Battle Screen not found! Exiting')
                recover()
                return
            if returnBattleResults(type='lab', firstOfMulti=True) is False:
                return
            clickXY(750, 1725, seconds=4) # Continue to second battle
            if isVisible('buttons/heroclassselect', retry=3):  # Check we're at the battle screen
                clickXY(550, 1850, seconds=4) # Battle
            else:
                printError('Battle Screen not found! Exiting')
                recover()
                return
            if returnBattleResults(type='lab') is False:
                return

            # 8th Row (multi)
            handleLabTile('upper', upperdirection, '8')
            if isVisible('buttons/heroclassselect', retry=3):  # Check we're at the battle screen
                clickXY(550, 1850, seconds=4) # Battle
            else:
                printError('Battle Screen not found! Exiting')
                recover()
                return
            if returnBattleResults(type='lab', firstOfMulti=True) is False:
                return
            clickXY(750, 1725, seconds=4) # Continue to second battle
            if isVisible('buttons/heroclassselect', retry=3):  # Check we're at the battle screen
                configureLabTeams(2, pet=False)  # We've lost heroes to Thoran etc by now, so lets re-pick 5 strongest heroes
                clickXY(550, 1850, seconds=4) # Battle
            else:
                printError('Battle Screen not found! Exiting')
                recover()
                return
            if returnBattleResults(type='lab') is False:
                return

            # 9th Row (witches den or fountain)
            handleLabTile('upper', upperdirection, '9')
            if isVisible('labels/labwitchsden', retry=3):
                printWarning('    Clearing Witch\'s Den')
                clickXY(550, 1500, seconds=3)  # Go
                clickXY(300, 1600, seconds=4)  # Abandon
            if isVisible('labels/labfountain', retry=3):
                printWarning('    Clearing Divine Fountain')
                clickXY(725, 1250, seconds=3)  # Confirm
                clickXY(725, 1250, seconds=2) # Go

            # 10th row (single boss)
            handleLabTile('upper', upperdirection, '10')
            if isVisible('buttons/heroclassselect', retry=3):  # Check we're at the battle screen
                configureLabTeams(1, pet=False) # We've lost heroes to Thoran etc by now, so lets re-pick 5 strongest heroes
                clickXY(550, 1850, seconds=4) # Battle
            else:
                printError('Battle Screen not found! Exiting')
                recover()
                return
            if returnBattleResults(type='lab') is False:
                return

            wait(6) # Long pause for Value Bundle to pop up
            clickXY(550, 1650, seconds=3) # Clear Value Bundle for completing lab
            clickXY(550, 550, seconds=3) # Loot Chest
            clickXY(550, 1650, seconds=2) # Clear Loot
            clickXY(550, 1650, seconds=2) # Clear Notice
            clickXY(550, 1650, seconds=2) # One more for safe measure
            clickXY(50, 1800, seconds=2) # Click Back to Exit
            printGreen("    Manual Lab run complete!")
    else:
        printError("Can't find Lab screen! Exiting..")

# Clears selected team and replaces it with top5 heroes, and 6th-10th for team2, selects pets in the first and second slots
def configureLabTeams(team, pet=True):
    if team == 1:
        clickXY(1030, 1100, seconds=2)  # Clear Team
        clickXY(550, 1250, seconds=2)  # Confirm
        clickXY(930, 1300)  # Slot 5 (Reverse order as our top heroes tend to be squishy so they get back line)
        clickXY(730, 1300)  # Slot 4
        clickXY(530, 1300)  # Slot 3
        clickXY(330, 1300)  # Slot 2
        clickXY(130, 1300)  # Slot 1
        if pet is True and isVisible('buttons/pet_empty', confidence=0.75, retry=3, click=True):
            clickXY(150, 1250, seconds=2) # First Pet
            clickXY(750, 1800, seconds=4) # Confirm
    if team == 2:
        clickXY(1030, 1100, seconds=2)  # Clear Team
        clickXY(550, 1250, seconds=2)  # Confirm
        clickXY(130, 1550)  # Slot 1
        clickXY(330, 1550)  # Slot 2
        clickXY(530, 1550)  # Slot 3
        clickXY(730, 1550)  # Slot 4
        clickXY(930, 1550)  # Slot 5
        if pet is True and isVisible('buttons/pet_empty', confidence=0.75, retry=3, click=True):
            clickXY(350, 1250, seconds=2) # Second Pet
            clickXY(750, 1800, seconds=4) # Confirm

# Will select the correct Lab tile and take us to the battle screen
# Elevation is either Upper or Lower dependon on whether we have scrolled the screen up or not for the scond half
# Side is left or right, we choose once at the start and once after scrolling up to get both multi fights
# Tile is the row of the tile we're aiming for, from 1 at the bottom to 10 at the final boss
def handleLabTile(elevation, side, tile):
    if tile == '4' or tile == '6' or tile == '10':
        printBlue('    Battling ' + elevation.capitalize() + ' Tile ' + tile)
    else:
        printBlue('    Battling ' + elevation.capitalize() + ' ' + side.capitalize() + ' Tile ' + tile)
    wait(1)
    if elevation == 'lower':
        if side == 'left':
            if tile == '1': # Single
                clickXY(400, 1450, seconds=2) # Tile
                clickXY(550, 1500, seconds=4)  # Go
            if tile == '2': # Multi
                clickXY(250, 1250, seconds=2) # Tile
                clickXY(550, 1500, seconds=4) # Click Go
                if isVisible('labels/notice', confidence=0.8, retry=3): # 'High Difficulty popup at first multi'
                    clickXY(450, 1150, seconds=2)  # Don't show this again
                    clickXY(725, 1250, seconds=4)  # Go
                clickXY(750, 1500, seconds=4) # Click Begin Battle
            if tile == '3': # Single
                clickXY(400, 1050, seconds =2) # Tile
                clickXY(550, 1600, seconds=4)  # Go (lower for relic)
            if tile == '4': # Multi
                clickXY(550, 850, seconds=2) # Tile
                clickXY(550, 1500, seconds=4) # Click Go
                clickXY(750, 1500, seconds=4) # Click Begin Battle
            if tile == '5': # Single
                clickXY(400, 650, seconds=2) # Tile
                clickXY(550, 1500, seconds=4)  # Go
            if tile == '6': # Single
                clickXY(550, 450, seconds=2) # Tile
                clickXY(550, 1600, seconds=4)  # Go (lower for relic)
        if side == 'right':
            if tile == '1': # Single
                clickXY(700, 1450, seconds=2) # Tile
                clickXY(550, 1500, seconds=4)  # Go
            if tile == '2': # Multi
                clickXY(800, 1225, seconds=2) # Tile
                clickXY(550, 1500, seconds=4) # Click Go
                if isVisible('labels/notice', confidence=0.8, retry=3): # 'High Difficulty popup at first multi'
                    clickXY(450, 1150, seconds=2)  # Don't show this again
                    clickXY(725, 1250, seconds=4)  # Go
                clickXY(750, 1500, seconds=4) # Click Begin Battle
            if tile == '3': # Single
                clickXY(700, 1050, seconds=2) # Tile
                clickXY(550, 1600, seconds=4)  # Go (lower for relic)
            if tile == '4': # Multi
                clickXY(550, 850, seconds=2) # Tile
                clickXY(550, 1500, seconds=4) # Click Go
                clickXY(750, 1500, seconds=4) # Click Begin Battle
            if tile == '5': # Single
                clickXY(700, 650, seconds=2) # Tile
                clickXY(550, 1500, seconds=4)  # Go
            if tile == '6':
                clickXY(550, 450, seconds=2) # Tile
                clickXY(550, 1600, seconds=4)  # Go (lower for relic)
    if elevation == 'upper':
        if side == 'left':
            if tile == '7': # Multi
                clickXY(400, 1450, seconds=2) # Tile
                # No Go as we opened the tile to check direction
                clickXY(750, 1500, seconds=4) # Click Begin Battle
            if tile == '8': # Multi
                clickXY(250, 1250, seconds=2) # Tile
                clickXY(550, 1500, seconds=4)  # Go
                clickXY(750, 1500, seconds=4) # Click Begin Battle
            if tile == '9':  # Witches Den or Well
                clickXY(400, 1100, seconds=2)  # Tile
            if tile == '10': # Single
                clickXY(550, 900, seconds=2) # Tile
                clickXY(550, 1500, seconds=4)  # Go
        if side == 'right':
            if tile == '7': # Multi
                clickXY(700, 1450, seconds=2) # Tile
                clickXY(550, 1500, seconds=4) # Go
                clickXY(750, 1500, seconds=4) # Click Begin Battle
            if tile == '8': # Multi
                clickXY(800, 1225, seconds=2) # Tile
                clickXY(550, 1500, seconds=4)  # Go
                clickXY(750, 1500, seconds=4) # Click Begin Battle
            if tile == '9':  # Witches Den or Well
                clickXY(700, 1100, seconds=2)  # Tile
            if tile == '10': # Single
                clickXY(550, 850, seconds=2) # Tile
                clickXY(550, 1500, seconds=4)  # Go

# Returns result of a battle, diferent types for the different types of post-battle screens, count for number of battles in Arena
# firstOfMulti is so we don't click to clear loot after a lab battle, which would exit us from the battle screen for the second fight
def returnBattleResults(type, firstOfMulti=False):
    counter = 0

    if type == 'BoB':
        while counter < 20:
            if isVisible('labels/victory'):
                # printGreen('    Battle of Blood Victory!')
                clickXY(550, 1850, seconds=3)  # Clear window
                return True
            if isVisible('labels/defeat'):
                # printError('    Battle of Blood Defeat!')
                clickXY(550, 1850, seconds=3)  # Clear window
                return False
            counter += 1
        printError('Battletimer expired')
        recover()
        return False

    if type == 'lab':
        while counter < 15:
            # For 'resources exceeded' message
            if isVisible('labels/notice'):
                clickXY(550, 1250)
            if isVisible('labels/victory'):
                printGreen('    Lab Battle Victory!')
                if firstOfMulti is False:  # Else we exit before second battle while trying to collect loot
                    clickXY(550, 1850, seconds=5)  # Clear loot popup and wait for Lab to load again
                return
            if isVisible('labels/defeat'):
                # TODO Use Duras Tears so we can continue
                printError('    Lab Battle  Defeat! Exiting..')
                recover()
                return False
            counter += 1
        printError('Battletimer expired')
        recover()
        return False

    if type == 'arena':
        while counter < 10:
            if isVisible('labels/rewards'):
                return True
            if isVisible('labels/defeat'):
                return False
            wait(1)
            counter += 1
        printError('Arena battle timed out!')
        return False