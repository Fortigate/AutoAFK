from tools import *
from AutoAFK import printGreen, printError, printWarning, printBlue, settings
import datetime
import configparser

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
        # if (isVisible('buttons/begin')):
        #     clickXY(550, 1550)
        # click('buttons/collect')
        # clickXY(550, 1800) # Click campaign in case we level up
        printGreen('    AFK Rewards collected!')
    else:
        printError('AFK Rewards chests not found!')
        recover()

def collectMail():
    printBlue('Attempting mail collection')
    if isVisible('buttons/mail'):
        if (pixelCheck(1012, 610, 2) > 240): # We check if the pixel where the notification sits has a red value of higher than 240
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
        if (pixelCheck(1012, 790, 2) > 240):  # We check if the pixel where the notification sits has a red value of higher than 240
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
        if (pixelCheck(980, 1620, 2) > 220):  # We check if the pixel where the notification sits has a red value of higher than 240
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
        click('buttons/beginbattle', seconds=2)
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
    firstrun = True
    if firstrun is True:
        confirmLocation('campaign')
        click('buttons/begin', 0.7, retry=3, suppress=True, seconds=3)  # lower confidence and retries for animated button
        config.read(settings)  # to load any new values (ie formation dropdown changed and saved) into memory
        wait(3)
        firstrun = False
    click('labels/taptocontinue', confidence=0.8, suppress=True, grayscale=True)
    click('buttons/cancel', seconds=2, suppress=True)
    if (isVisible('buttons/begin_plain', 0.7)): # If we see second Begin it's a multi so we take different actions
        click('buttons/begin_plain', 0.7, seconds=2, retry=2, suppress=True)
        if isVisible('buttons/formations'):
            click('buttons/formations', seconds=3)
            clickXY(850, 425 + (formation * 175))
            click('buttons/use', suppress=True)
            click('buttons/confirm_small', suppress=True)
            click('buttons/autobattle', suppress=True) # So we don't hit it in the background while autobattle is active
            click('buttons/activate', suppress=True)
    else:
        if isVisible('buttons/formations'):
            click('buttons/formations', seconds=3, suppress=True)
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

def handleBounties():
    printBlue('Handling Bounty Board')
    confirmLocation('darkforest')
    clickXY(600, 1320)
    if (isVisible('labels/bountyboard')):
        clickXY(650, 1700) # Solo tab
        click('buttons/collect_all', seconds=2, suppress=True)
        if config.getboolean('DAILIES', 'solobounties') is True:
            wait()
            click('buttons/dispatch', suppress=True)
            click('buttons/confirm', suppress=True)
        clickXY(950,1700) # Team tab
        click('buttons/collect_all', seconds=2, suppress=True)
        click('buttons/dispatch', suppress=True)
        click('buttons/confirm', suppress=True)
        click('buttons/back')
        printGreen('    Bounties attempted successfully')
    else:
        printError('    Bounty Board not found, attempting to recover')
        recover()

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
    clickXY(500, 870, seconds=3) # Long pause for animation
    if isVisible('labels/kingstower'):
        towers = {"King's Tower": [500, 870], "Lightbringer Tower": [300, 1000], "Wilder Tower": [800, 600], "Mauler Tower": [400, 1200],
                  "Graveborn Tower": [800, 1200], "Hypogean Tower": [600, 1500], "Celestial Tower": [300, 500]}
        for tower, location in towers.items():
            if tower == name:
                clickXY(location[0], location[1], seconds=3)

def pushTower(formation=3, duration=1):
    firstrun = True
    if firstrun is True:
        click('buttons/challenge_plain', 0.7, retry=3, suppress=True, seconds=3)  # lower confidence and retries for animated button
        config.read(settings)  # to load any new values (ie formation downdown changed and saved) into memory
        wait(3)
        firstrun = False
    click('labels/taptocontinue', confidence=0.8, suppress=True, grayscale=True)
    click('buttons/cancel', seconds=2, suppress=True)
    if (isVisible('buttons/autobattle') and not isVisible('buttons/exit')): # So we don't catch the button in the background
        if isVisible('buttons/formations'):
            click('buttons/formations', seconds=3)
            clickXY(850, 425 + (formation * 175))
            click('buttons/use', suppress=True)
            click('buttons/confirm_small', suppress=True)
            click('buttons/autobattle', suppress=True) # So we don't hit it in the background while autobattle is active
            click('buttons/activate', suppress=True)
    wait((duration * 60)-45)
    clickXY(550, 1750)
    if isVisible('labels/autobattle', retry=3):
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
        click('buttons/challenge_plain', 0.7, retry=5, suppress=True, seconds=3) # lower confidence and retries for animated button
        # For reasons sometimes this button is 'beginbattle' and sometimes it is 'begin', so we use clickXY
        clickXY(700, 1850)
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

def handleShopPurchasing():
    # Buy Shards
    if config.getboolean('SHOP', 'shards'):
        clickXY(200, 800)
        click('buttons/shop/purchase', suppress=True)
        clickXY(550, 1220)
    # Buy Shards
    if config.getboolean('SHOP', 'cores'):
        clickXY(425, 800)
        click('buttons/shop/purchase', suppress=True)
        clickXY(550, 1220)
    # Buy TG
    if config.getboolean('SHOP', 'timegazer'):
        clickXY(650, 800)
        click('buttons/shop/purchase', suppress=True)
        clickXY(550, 1220)
    # Buy Bait
    if config.getboolean('SHOP', 'baits'):
        clickXY(875, 800)
        click('buttons/shop/purchase', suppress=True)
        clickXY(550, 1220)
    # Buy Dust Gold
    if config.getboolean('SHOP', 'dust_gold'):
        click('buttons/shop/dust', 0.95, suppress=True)
        click('buttons/shop/purchase', suppress=True)
        clickXY(550, 1220)
    # Buy Dust Diamonds
    if config.getboolean('SHOP', 'dust_diamond'):
        click('buttons/shop/dust_diamond', 0.95, suppress=True)
        click('buttons/shop/purchase', suppress=True)
        clickXY(550, 1220)
    # Buy Super Soulstone
    if config.getboolean('SHOP', 'superb_soulstone'):
        click('buttons/shop/superstone', 0.95, suppress=True)
        click('buttons/shop/purchase', suppress=True)
        clickXY(550, 1220)
    # Buy Elite Soulstone
    if config.getboolean('SHOP', 'elite_soulstone'):
        click('buttons/shop/superstone', 0.80, suppress=True)
        click('buttons/shop/purchase', suppress=True)
        clickXY(550, 1220)
    # Buy Gold Emblems
    if config.getboolean('SHOP', 'gold_emblem'):
        click('buttons/shop/gold_emblems', 0.95, suppress=True)
        click('buttons/shop/purchase', suppress=True)
        clickXY(550, 1220)
    # Buy Silver Emblems
    if config.getboolean('SHOP', 'silver_emblem'):
        click('buttons/shop/silver_emblems', 0.95, suppress=True)
        click('buttons/shop/purchase', suppress=True)
        clickXY(550, 1220)
    # Buy PoE Emblems
    if config.getboolean('SHOP', 'poe'):
        click('buttons/shop/poe', suppress=True)
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
        swipe(550, 1500, 550, 1200, 500, seconds=5)
        handleShopPurchasing()
        # refresh purchases
        while counter < shoprefreshes:
            clickXY(1000, 300)
            click('buttons/confirm', suppress=True, seconds=3)
            swipe(550, 1500, 550, 1200, 500, seconds=3)
            print('    Refreshed store ' + str(counter+1) + ' times.')
            handleShopPurchasing()
            counter += 1
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
    if isVisible('buttons/confirm_nobles', 0.8, retry=2):
        printWarning('Noble resource collection screen found, skipping merchant collection')
        clickXY(550, 100)
        clickXY(70, 1810)
        return
    swipe(1000, 1825, 100, 1825, 500)
    swipe(1000, 1825, 100, 1825, 500)
    if isVisible('buttons/noblesociety'):
        print('    Collecting Nobles')
        # Nobles
        clickXY(675, 1825)
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
        print('    Collecting Monthly Cards')
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
        print('    Collecting Special Deal')
        click('buttons/dailydeals')
        clickXY(150, 1625)
        # Daily Deal
        if isVisible('buttons/merchant_daily', confidence=0.8, click=True):
            print('    Collecting Daily Deal')
            swipe(550, 1400, 550, 1200, 500, seconds=3)
            click('buttons/dailydeals')
            clickXY(400, 1675)
        # Biweeklies
        if d.isoweekday() == 3: # Wednesday
            if isVisible('buttons/merchant_biweekly', confidence=0.8, click=True):
                print('    Collecting Biweekly Deal')
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
        print('    Clearing Rhapsody notification')
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
    clickXY(775, 875)
    clickXY(550, 600)
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