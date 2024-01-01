import math

from tools import *
from AutoAFK import printGreen, printError, printWarning, printBlue, printPurple, settings
import datetime
import configparser
import random

config = configparser.ConfigParser()
config.read(settings)
d = datetime.datetime.now()

def collectAFKRewards():
    printBlue('Attempting AFK Reward collection')
    confirmLocation('campaign')
    if (isVisible('buttons/campaign_selected')):
        clickXY(550, 1550)
        click('buttons/collect', 0.8)
        clickXY(550, 1800, seconds=1) # Click campaign in case we level up
        clickXY(550, 1800, seconds=1) # again for the time limited deal popup
        clickXY(550, 1800, seconds=1) # 3rd to be safe
        printGreen('    AFK Rewards collected!')
    else:
        printError('AFK Rewards chests not found!')
        recover()

def collectMail():
    printBlue('Attempting mail collection')
    if isVisible('buttons/mail'):
        if (pixelCheck(1012, 610, 0) > 240): # We check if the pixel where the notification sits has a red value of higher than 240
            clickXY(960, 630)
            click('buttons/collect_all', seconds=3)
            clickXY(550, 1600)
            click('buttons/back')
            printGreen('    Mail collected!')
        else:
            printWarning('    Mail notification not found')
    else:
        printError('Mail icon not found!')

def collectCompanionPoints(mercs=False):
    printBlue('Attempting to send/receive companion points')
    if isVisible('buttons/friends'):
        if (pixelCheck(1012, 790, 0) > 240):  # We check if the pixel where the notification sits has a red value of higher than 240
            clickXY(960, 810)
            click('buttons/sendandreceive')
            if mercs is True:
                clickXY(720, 1760) # Short term
                clickXY(990, 190) # Manage
                clickXY(630, 1590) # Apply
                clickXY(750, 1410) # Auto lend
                click('buttons/exitmenu')
                printGreen('    Mercenaries lent out')
            click('buttons/back')
            printGreen('    Friends Points Sent')
        else:
            printWarning('    Friends notification not found')

def collectFastRewards(count):
    printBlue('Attempting to collecting Fast Rewards ' + str(count) + 'x times')
    counter = 0
    confirmLocation('campaign')
    if isVisible('buttons/fastrewards'):
        if (pixelCheck(980, 1620, 0) > 220):  # We check if the pixel where the notification sits has a red value of higher than 240
            #todo add isVisible 'collect' button verification
            clickXY(950, 1660)
            while counter < count:
                clickXY(710, 1260)
                wait(2)
                clickXY(550, 1800)
                counter = counter+1
            click('buttons/close')
            printGreen('    Fast Rewards Done')
        else:
            printWarning('    Fast Rewards already done')
    else:
        printError('    Fast Rewards icon not found!')

def attemptCampaign():
    printBlue('Attempting Campaign battle')
    confirmLocation('campaign')
    click('buttons/begin', seconds=2)
    if (isVisible('buttons/begin', 0.7)): # If we see second Begin it's a multi so we take different actions
        click('buttons/begin', 0.7, seconds=2)
        click('buttons/beginbattle', seconds=4)
        click('buttons/pause', retry=3) # 3 retries as ulting heroes can cover the button
        click('buttons/exitbattle')
        click('buttons/back')
    else: # else it's a single battle
        click('buttons/battle', 0.8, retry=3, seconds=3)
        click('buttons/battle_large', 0.8, suppress=True) #If you have no autobattle button its larger
        click('buttons/pause', 0.8, retry=3) # 3 retries as ulting heroes can cover the button
        click('buttons/exitbattle')
    if confirmLocation('campaign', bool=True):
        printGreen('    Campaign attempted successfully')
    else:
        printError('    Something went wrong, attempting to recover')
        recover()

def pushCampaign(formation=3, duration=1):
    click('labels/taptocontinue', confidence=0.8, suppress=True, grayscale=True)
    click('buttons/cancel', seconds=2, suppress=True)
    if (isVisible('buttons/begin_plain', 0.7)): # If we see second Begin it's a multi so we take different actions
        click('buttons/begin_plain', 0.7, seconds=2, retry=2, suppress=True)
        if isVisible('buttons/formations', click=True, seconds=3):
            clickXY(800, 1650, seconds=2) # Change to 'Popular' tab
            clickXY(850, 425 + (formation * 175))
            click('buttons/use', suppress=True)
            click('buttons/confirm_small', suppress=True)
            click('buttons/autobattle', suppress=True) # So we don't hit it in the background while autobattle is active
            click('buttons/activate', suppress=True)
    else:
        if isVisible('buttons/formations', click=True, seconds=3):
            clickXY(850, 425 + (formation * 175))
            click('buttons/use', suppress=True)
            click('buttons/confirm_small', suppress=True)
            click('buttons/autobattle', suppress=True) # So we don't hit it in the background while autobattle is active
            click('buttons/activate', suppress=True)
    wait((duration * 60) - 45)
    clickXY(550, 1750)
    if isVisible('labels/autobattle'):
        if isVisible('labels/autobattle_0'):
            wait(2)
            if config.get('PUSH', 'suppressSpam') is False:
                printWarning('No victory found, checking again in ' + str(config.get('PUSH', 'victoryCheck') + ' minutes.'))
            click('buttons/cancel', retry=3, suppress=True)
        else:
            printGreen('Victory found! Loading the ' + str(config.get('PUSH', 'formation') + ' formation for the current stage..'))
            click('buttons/exit', suppress=True)
            click('buttons/pause', 0.8, retry=3, suppress=True)  # 3 retries as ulting heroes can cover the button
            click('buttons/exitbattle', suppress=True)
            click('labels/taptocontinue', confidence=0.8, suppress=True, grayscale=True)
    else:
        printError('AutoBattle screen not found, exiting..')
        sys.exit(1)
        buttonState('enabled')

def handleBounties():
    printBlue('Handling Bounty Board')
    confirmLocation('darkforest')
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
        click('buttons/back')
        printGreen('    Bounties attempted successfully')
    else:
        printError('    Bounty Board not found, attempting to recover')
        recover()

def dispatchSoloBounties(remaining=2, maxRefreshes=3):
    refreshes = 0
    while refreshes <= maxRefreshes:
        if refreshes > 0:
            printWarning('   Board refreshed (#' + str(refreshes) + ')')
        dispatches = returnMultiple('buttons/dispatch_bounties', confidence=0.97)
        dispatcher(dispatches) # Send the list to the function to dispatch
        swipe(550, 800, 550, 500, duration=200, seconds=2) # scroll down
        dispatches = returnMultiple('buttons/dispatch_bounties', confidence=0.97)
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

def dispatcher(dispatches):
    # print(str(len(dispatches)) + ' Dispatches found.') # Debugging
    for button in dispatches:
        y_center = round(
            button[1] + button[3] / 2)  # Return left + half the height to get the center Y coord of the image
        blue_value = pixelCheck(120, y_center, 2, seconds=0) # Take a reading from the middle of the icon
        red_value = pixelCheck(120, y_center, 0, seconds=0) # Take a reading from the middle of the icon
        # printWarning('Red: ' + str(red_value) + '. Blue: ' + str(blue_value) + '.') # Debugging
        if blue_value < 100 and red_value > 200:
            # Gold
            continue
        elif blue_value > 220 and red_value > 155 and red_value < 200:
            # Soulstone
            continue
        elif blue_value > 190 and red_value < 155:
            if config.getboolean('BOUNTIES', 'dispatchDust'):
                printGreen('    Dispatching Dust')
                clickXY(900, y_center)
                clickXY(350, 1150)
                clickXY(750, 1150)
        elif blue_value > 230 and red_value > 230:
            if config.getboolean('BOUNTIES', 'dispatchDiamonds'):
                printGreen('    Dispatching Diamonds')
                clickXY(900, y_center)
                clickXY(350, 1150)
                clickXY(750, 1150)


def handleArenaOfHeroes(count):
    counter = 0
    printBlue('Battling Arena of Heroes ' + str(count) + ' times')
    confirmLocation('darkforest')
    clickXY(740, 1050)
    clickXY(550, 50)
    if isVisible('labels/arenaofheroes_new'): # The label font changes for reasons
        click('labels/arenaofheroes_new', suppress=True)
        click('buttons/challenge', retry=3) # retries for animated button
        while counter < count:
            wait(1) # To avoid error when clickMultipleChoice returns no results
            clickMultipleChoice('buttons/arenafight', 4, confidence=0.98) # Select 4th opponent
            click('buttons/battle', 0.6, retry=3, suppress=True) # lower confidence as it's an animated button
            wait(2)
            click('buttons/skip', retry=5, suppress=True) # Retries as ulting heros can cover the button
            if (isVisible('labels/defeat')):
                printError('    Battle #' + str(counter+1) + ' Defeat!')
            else:
                printGreen('    Battle #' + str(counter+1) + ' Victory!')
                clickXY(600, 550) # Clear loot popup
            clickXY(600, 550)
            counter = counter+1
        click('buttons/exitmenu')
        click('buttons/back')
        click('buttons/back')
        printGreen('    Arena battles complete')
    else:
        printError('Arena of Heroes not found, attempting to recover')
        recover()

def collectGladiatorCoins():
    printBlue('Collecting Gladiator Coins')
    confirmLocation('darkforest')
    clickXY(740, 1050)
    clickXY(550, 50)
    if isVisible('labels/legendstournament_new'): # The label font changes for reasons
        click('labels/legendstournament_new', suppress=True)
        clickXY(550, 300, seconds=2)
        clickXY(50, 1850)
        click('buttons/back')
        click('buttons/back')
        printGreen('    Gladiator Coins collected')
    else:
        printError('    Legends Tournament not found, attempting to recover')
        recover()

def collectFountainOfTime():
    printBlue('Collecting Fountain of Time')
    confirmLocation('darkforest')
    clickXY(800, 700, seconds=6)
    clickXY(800, 700, seconds=1)
    if isVisible('labels/temporalrift'):
        clickXY(550, 1800)
        clickXY(250, 1300)
        clickXY(700, 1350) # Collect
        clickXY(550, 1800, seconds=3) # Clear level up
        clickXY(550, 1800, seconds=3) # Clear limited deal
        clickXY(550, 1800, seconds=3) # Clear newly unlocked
        click('buttons/back')
        printGreen('    Fountain of Time collected')
    else:
        printError('    Temporal Rift not found, attempting to recover')
        recover()

def openTower(name):
    printBlue('Opening ' + name + '.')
    confirmLocation('darkforest')
    wait(3) # Medium wait to make sure tower button is active when we click
    clickXY(500, 870, seconds=3) # Long pause for animation opening towers
    if isVisible('labels/kingstower'):
        towers = {"King's Tower": [500, 870], "Lightbringer Tower": [300, 1000], "Wilder Tower": [800, 600], "Mauler Tower": [400, 1200],
                  "Graveborn Tower": [800, 1200], "Hypogean Tower": [600, 1500], "Celestial Tower": [300, 500]}
        for tower, location in towers.items():
            if tower == name:
                clickXY(location[0], location[1], seconds=3)

def pushTower(formation=3, duration=1):
    click('buttons/challenge_plain', 0.7, retry=3, suppress=True, seconds=3)  # lower confidence and retries for animated button
    click('labels/taptocontinue', confidence=0.8, suppress=True, grayscale=True)
    click('buttons/cancel', seconds=2, suppress=True)
    if (isVisible('buttons/autobattle') and not isVisible('buttons/exit')): # So we don't catch the button in the background
        if isVisible('buttons/formations'):
            click('buttons/formations', seconds=3)
            clickXY(800, 1650, seconds=2) # Change to 'Popular' tab
            clickXY(850, 425 + (formation * 175))
            click('buttons/use', retry=3)
            click('buttons/confirm_small')
            click('buttons/autobattle')
            click('buttons/activate')
    wait((duration * 60)-45)
    clickXY(550, 1750)
    if isVisible('labels/autobattle', retry=2):
        if isVisible('labels/autobattle_0'):
            wait(2)
            if config.get('PUSH', 'suppressSpam') is False:
                printWarning('No victory found, checking again in ' + str(config.get('PUSH', 'victoryCheck') + ' minutes.'))
            click('buttons/cancel', retry=3, suppress=True)
        else:
            printGreen('Victory found! Loading the ' + str(config.get('PUSH', 'formation') + ' formation for the current stage..'))
            click('buttons/exit', suppress=True)
            click('buttons/pause', 0.8, retry=3, suppress=True)  # 3 retries as ulting heroes can cover the button
            click('buttons/exitbattle', suppress=True)
            click('labels/taptocontinue', confidence=0.8, suppress=True, grayscale=True)
    else:
        printError('AutoBattle screen not found, exiting..')
        sys.exit(1)

def handleKingsTower():
    printBlue('Attempting Kings Tower battle')
    confirmLocation('darkforest')
    clickXY(500, 870, seconds=3) # Long pause for animation
    if isVisible('labels/kingstower'):
        clickXY(555, 585)
        click('buttons/challenge_plain', 0.7, retry=5, suppress=True, seconds=5) # lower confidence and retries for animated button
        # For reasons sometimes this button is 'beginbattle' and sometimes it is 'begin', so we use clickXY
        clickXY(700, 1850, seconds=2)
        # click('buttons/beginbattle', 0.8, seconds=3, retry=5)
        click('buttons/pause', 0.8, retry=5)
        click('buttons/exitbattle')
        click('buttons/back')
        click('buttons/back')
        if isVisible('buttons/back'):
            click('buttons/back') # Last one only needed for multifights
        printGreen('    Tower attempted successfully')
    else:
        printError('Tower screen not found, attempting to recover')
        recover()

def collectInnGifts():
    clicks = 0
    x_axis = 250
    printBlue('Attempting daily Inn gift collection')
    confirmLocation('ranhorn')
    clickXY(800,290, seconds=4)
    if isVisible('buttons/manage'):
        while clicks < 10: # We spam clicks in the right area and pray
            clickXY(x_axis, 1300, seconds=0.5)
            x_axis = x_axis + 50
            clicks = clicks + 1
            clickXY(550, 1400, seconds=0.5) # Clear loot
        click('buttons/back')
        printGreen('    Inn Gifts collected.')
    else:
        printError('    Inn not found, attempting to recover')
        recover()

def handleShopPurchasing(counter):
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

def shopPurchases(shoprefreshes):
    printBlue('Attempting store purchases (Refreshes: ' + str(shoprefreshes) + ')')
    counter = 0
    confirmLocation('ranhorn')
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
    confirmLocation('ranhorn')
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
        click('buttons/back')
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
            clickXY(400, 1675)
        # Biweeklies
        if d.isoweekday() == 3: # Wednesday
            if isVisible('buttons/merchant_biweekly', confidence=0.8, click=True):
                printPurple('    Collecting Biweekly Deal')
                swipe(300, 1400, 200, 1200, 500, seconds=3)
                clickXY(200, 1200)
                clickXY(550, 1625)
        # Yuexi
        if d.isoweekday() == 1: # Monday
            print('    Collecting Yuexi')
            clickXY(200, 1825)
            clickXY(240, 880)
            clickXY(150, 1625)
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
    confirmLocation('ranhorn')
    clickXY(380, 360, seconds=6)
    clickXY(550, 1800) # Clear chests
    clickXY(775, 875, seconds=2)
    clickXY(550, 600, seconds=3)
    if isVisible('buttons/nextboss'):
        printGreen('    Twisted Realm found, battling')
        if isVisible('buttons/challenge_tr'):
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

# Whole things needs alot of refinement, the event is too dynamic for static wait times
def handleBattleofBlood(battles=3):
    printBlue('Attempting to run Battle of Blood ' + str(battles) + ' times')
    counter = 0
    click('buttons/events', confidence=0.8, retry=3, seconds=3)
    if isVisible('labels/battleofblood_event_banner', click=True):
        while counter < battles:
            click('buttons/challenge_tr', confidence=0.8, suppress=True, retry=3, seconds=20)
            # Cards 1-2, ready
            clickXY(550, 1250, seconds=1)
            clickXY(350, 1250, seconds=1)
            clickXY(550, 1850, seconds=10)
            # Cards 3-4, ready
            clickXY(550, 1250, seconds=1)
            clickXY(350, 1250, seconds=1)
            clickXY(550, 1850, seconds=10)
            # Card 5, ready
            clickXY(550, 1250, seconds=1)
            clickXY(550, 1850, seconds=30)
            # Clear Battle Report
            clickXY(550, 1850, seconds=3)
            counter = counter + 1
            printGreen('    Battle of Blood Battle #' + str(counter) + ' complete')
        # Click quests
        clickXY(150, 230, seconds=2)
        # select dailies tab
        clickXY(650, 1720, seconds=1)
        # Collect Dailies
        clickXY(850, 720, seconds=2)
        clickXY(920, 525, seconds=2)
        clickXY(920, 525, seconds=2)
        # clear loot
        clickXY(550, 250, seconds=2)
        # Back twice to exit
        clickXY(70, 1650, seconds=1)
        clickXY(70, 1810, seconds=1)
        printGreen('    Battle of Blood attempted successfully')
    else:
        printWarning('Battle of Blood not found, recovering..')
        recover()

def handleCircusTour(battles = 3):
    counter = 1
    printBlue('Attempting to run Circus Tour battles')
    confirmLocation('ranhorn') # Trying to fix 'buttons/events not found' error
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
                clickXY(950, 1820, seconds=0.3)
                clickXY(950, 1820, seconds=0.3)
                wait(2)
            # return Awakened, Epic or Rare
            found = str(returnCardPullsRarity())
            counter += 1
            if found == "Awakened":
                printWarning('Awakened Found')
                # Let's check if it's the one we want
                if isVisible(os.path.join('summons', 'awakeneds', wokes[woke]), confidence=0.85, seconds=0.5):
                    printGreen('    ' + woke + ' found! Checking for ' + celehypo)
                    # If it is we then check the celeypo
                    if isVisible(os.path.join('summons', 'celehypos', celehypos[celehypo]), confidence=0.85):
                        printGreen('    ' + celehypo + ' found too! Recording Summon and exiting..')
                        click('buttons/summons/record', confidence=0.85, retry=3, seconds=3)
                        click('buttons/summons/change', confidence=0.85, retry=3, seconds=3, suppress=True) # Suppress as this isn't always present
                        click('buttons/summons/confirm', confidence=0.85, retry=3, seconds=3)
                        search = False
                    else:
                        printError('    ' + celehypo + ' not found, continuing..')
            if found == 'Epic':
                printPurple('Epic Found')
            if found == 'Rare':
                printBlue('Rare found')
        # Funky math for duration calculation, ceiling is used to roundup else it returns with a decimal place
        duration = time.time() - starttime
        hours = str(math.ceil(duration // 3600))
        minutes = str(math.ceil(duration // 60))
        printGreen('Unlimited Summons finished!')
        printGreen('In just ' + str(counter) + ' pulls and ' + hours + ' hours ' + minutes + ' minutes. Hooray!')
    else:
        # If we can't find the Unlimited Summons button we end
        printError('Could not find Unlimited Summons button..')


def TS_Battle_Stastistics():
    region = 10
    position = 80
    battle = 1
    team = 1
    while position < 100:
        # Open User
        clickXY(250, 560) # Click Portrait
        clickXY(450, 1800) # Follow
        wait(2)
        clickXY(550, 110) # Close player window
        clickXY(1000, 560) # Battle History
        # Open result 1
        clickXY(800, 600) # Battle History
        # open battle 1
        clickXY(550, 700) # team 1
        swipe(550, 800, 550, 600, duration=500)
        save_screenshot('ts_region' + str(region) + '_rank' + str(position) + '_battle' + str(battle) + '_team' + str(team))
        click('buttons/exitmenu')
        team += 1
        clickXY(550, 1000) # team 2
        swipe(550, 800, 550, 600, duration=500)
        save_screenshot('ts_region' + str(region) + '_rank' + str(position) + '_battle' + str(battle) + '_team' + str(team))
        click('buttons/exitmenu')
        team += 1
        clickXY(550, 1300) # team 3
        swipe(550, 800, 550, 600, duration=500)
        save_screenshot('ts_region' + str(region) + '_rank' + str(position) + '_battle' + str(battle) + '_team' + str(team))
        click('buttons/exitmenu')
        click('buttons/exitmenu')
        # # open battle 2
        # clickXY(800, 800)
        # clickXY(550, 700) # team 1
        # swipe(550, 800, 550, 600, duration=500)
        # save_screenshot('ts_region' + region + ' + _rank' + str(position) + '_battle' + str(battle) + '_team' + str(team))
        # click('buttons/exitmenu')
        # team += 1
        # clickXY(550, 1000) # team 2
        # swipe(550, 800, 550, 600, duration=500)
        # save_screenshot('ts_region' + region + ' + _rank' + str(position) + '_battle' + str(battle) + '_team' + str(team))
        # click('buttons/exitmenu')
        # click('buttons/exitmenu')
        # team = 1
        # battle += 1
        # # open battle 3
        # clickXY(800, 1000)
        # clickXY(550, 700) # team 1
        # swipe(550, 800, 550, 600, duration=500)
        # save_screenshot('ts_region' + region + ' + _rank' + str(position) + '_battle' + str(battle) + '_team' + str(team))
        # click('buttons/exitmenu')
        # team += 1
        # clickXY(550, 1000) # team 2
        # swipe(550, 800, 550, 600, duration=500)
        # save_screenshot('ts_region' + region + ' + _rank' + str(position) + '_battle' + str(battle) + '_team' + str(team))
        # click('buttons/exitmenu')
        # click('buttons/exitmenu')
        # team = 1
        # battle += 1
        # # open battle 4
        # clickXY(800, 1200)
        # clickXY(550, 700) # team 1
        # swipe(550, 800, 550, 600, duration=500)
        # save_screenshot('ts_region' + region + ' + _rank' + str(position) + '_battle' + str(battle) + '_team' + str(team))
        # click('buttons/exitmenu')
        # team += 1
        # clickXY(550, 1000) # team 2
        # swipe(550, 800, 550, 600, duration=500)
        # save_screenshot('ts_region' + region + ' + _rank' + str(position) + '_battle' + str(battle) + '_team' + str(team))
        # click('buttons/exitmenu')
        # click('buttons/exitmenu')
        # team = 1
        # battle += 1
        # # open battle 5
        # clickXY(800, 1400)
        # clickXY(550, 700) # team 1
        # swipe(550, 800, 550, 600, duration=500)
        # save_screenshot('ts_region' + region + ' + _rank' + str(position) + '_battle' + str(battle) + '_team' + str(team))
        # click('buttons/exitmenu')
        # team += 1
        # clickXY(550, 1000) # team 2
        # swipe(550, 800, 550, 600, duration=500)
        # save_screenshot('ts_region' + region + ' + _rank' + str(position) + '_battle' + str(battle) + '_team' + str(team))
        # click('buttons/exitmenu')
        click('buttons/exitmenu')
        click('buttons/exitmenu')
        clickXY(250, 550) # Click Portrait
        clickXY(450, 1800) # Unfollow
        clickXY(650, 1250) # Confirm Unfollow
        clickXY(550, 110) # Close player window
        team = 1
        battle = 1
        position += 1
        swipe(550, 800, 550, 635, duration=8000)

def TS_Battle_Report():
    region = 22
    position = 80
    battle = 1
    while position < 100:
        # Open User
        clickXY(250, 550, seconds=2) # Click Portrait
        clickXY(450, 1800, seconds=2) # Follow
        wait(2)
        clickXY(550, 110, seconds=2) # Close player window
        clickXY(1000, 550, seconds=2) # Battle History
        # Open battle 1
        clickXY(800, 600, seconds=2)
        save_screenshot('ts_region' + str(region) + '_rank' + str(position) + '_battle' + str(battle))
        click('buttons/exitmenu')
        battle += 1
        # # open battle 2
        # clickXY(800, 800, seconds=2)
        # save_screenshot('ts_region' + str(region) + '_rank' + str(position) + '_battle' + str(battle))
        # click('buttons/exitmenu')
        # battle += 1
        # # open battle 3
        # clickXY(800, 1000, seconds=2)
        # save_screenshot('ts_region' + str(region) + '_rank' + str(position) + '_battle' + str(battle))
        # click('buttons/exitmenu')
        # battle += 1
        # # open battle 4
        # clickXY(800, 1200, seconds=2)
        # save_screenshot('ts_region' + str(region) + '_rank' + str(position) + '_battle' + str(battle))
        # click('buttons/exitmenu')
        # battle += 1
        # # open battle 5
        # clickXY(800, 1400, seconds=2)
        # save_screenshot('ts_region' + str(region) + '_rank' + str(position) + '_battle' + str(battle))
        # click('buttons/exitmenu')
        click('buttons/exitmenu')
        clickXY(250, 550, seconds=2) # Click Portrait
        clickXY(450, 1800, seconds=2) # Unfollow
        clickXY(650, 1250, seconds=2) # Confirm Unfollow
        clickXY(550, 110, seconds=2) # Close player window
        battle = 1
        position += 1
        swipe(550, 800, 550, 635, duration=8000)