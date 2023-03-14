from tools import *
from AutoAFK import printGreen, printError, printWarning, printBlue
import datetime

d = datetime.datetime.now()

def collectAFKRewards():
    printBlue('Attempting AFK Reward collection 2x')
    confirmLocation('campaign')
    if (isVisible('buttons/campaign_selected')):
        clickXY(550, 1550)
        click('buttons/collect', 0.8)
        clickXY(550, 1800, seconds=5) # Click campaign in case we level up, long pause so we can collect twice
        if (isVisible('buttons/begin')):
            clickXY(550, 1550)
        click('buttons/collect')
        clickXY(550, 1800) # Click campaign in case we level up
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
        click('buttons/battle', seconds=3)
        click('buttons/pause', 0.8, retry=3) # 3 retries as ulting heroes can cover the button
        click('buttons/exitbattle')
    if verifyLocation('campaign'):
        printGreen('    Campaign attempted successfully')
    else:
        printError('    Something went wrong, attempting to recover')
        recover()

def handleBounties(dispatch=False):
    printBlue('Handling Bounty Board')
    confirmLocation('darkforest')
    clickXY(600, 1320)
    if (isVisible('labels/bountyboard')):
        clickXY(650, 1700) # Solo tab
        click('buttons/collect_all', seconds=2, suppress=True)
        if dispatch is True:
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
    printBlue('Battling Arena of Heroes ' + str(count) + 'x times')
    confirmLocation('darkforest')
    clickXY(740, 1050)
    clickXY(550, 50)
    if isVisible('labels/arenaofheroes'):
        click('labels/arenaofheroes')
        click('buttons/challenge', retry=3) # retries for animated button
        while counter < count:
            clickXY(820, 1225)
            click('buttons/battle', 0.6, retry=3) # lower confidence as it's an animated button
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
        while clicks < 6: # WE spam clicks in the right area and pray
            clickXY(x_axis, 1300, seconds=0.5)
            x_axis = x_axis + 75
            clicks = clicks + 1
            clickXY(550, 1400, seconds=0.5) # Clear loot
        click('buttons/back')
        printGreen('    Inn Gifts collected.')
    else:
        printError('    Inn not found, attempting to recover')
        recover()

def shopPurchases(shoprefreshes):
    printBlue('Attempting store purchases (Refreshes: ' + str(shoprefreshes) + ')')
    counter = 0
    confirmLocation('ranhorn')
    clickXY(300, 1725, seconds=5)
    if isVisible('labels/store'):
        # First purchases
        swipe(550, 1500, 550, 1200, 500, seconds=2)
        # Buy TG
        clickXY(650, 800)
        click('buttons/shop/purchase', suppress=True)
        clickXY(550, 1220)
        # Buy Shards
        clickXY(200, 800)
        click('buttons/shop/purchase', suppress=True)
        clickXY(550, 1220)
        # Buy dust
        click('buttons/shop/dust', suppress=True)
        click('buttons/shop/purchase', suppress=True)
        clickXY(550, 1220)
        # Buy POE
        click('buttons/shop/poe', suppress=True)
        click('buttons/shop/purchase', suppress=True)
        clickXY(550, 1220)
        # Check for superstones
        click('buttons/shop/superstone', 0.95, suppress=True)
        click('buttons/shop/purchase', suppress=True)
        # refresh purchases
        while counter < shoprefreshes:
            clickXY(1000, 300)
            click('buttons/confirm', suppress=True, seconds=4)
            print('    Refreshed store ' + str(counter+1) + ' times.')
            swipe(550, 1500, 550, 1200, 500, seconds=2)
            # Buy Shards
            clickXY(200, 800)
            click('buttons/shop/purchase', suppress=True)
            clickXY(550, 1220)
            # Buy dust
            click('buttons/shop/dust', suppress=True)
            click('buttons/shop/purchase', suppress=True)
            clickXY(550, 1220)
            # Buy POE
            click('buttons/shop/poe', suppress=True)
            click('buttons/shop/purchase', suppress=True)
            clickXY(550, 1220)
            # Check for superstones
            click('buttons/shop/superstone', 0.95, suppress=True)
            click('buttons/shop/purchase', suppress=True)
            clickXY(550, 1220)
            counter += 1
            wait(5)
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
            wait()
            clickXY(550, 500)
            clickXY(550, 500,seconds=2)
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
            clickXY(400, 1650)
        click('buttons/back')
        printGreen('    Quests collected')
    else:
        printError('    Quests screen not found, attempting to recover')
        recover()

def clearMerchant():
    printBlue('Attempting to collect merchant deals')
    clickXY(120, 300, seconds=5)
    swipe(1000, 1825, 100, 1825, 500)
    swipe(1000, 1825, 100, 1825, 500)
    print('    Collecting Nobles')
    # Nobles
    clickXY(675, 1825)
    # Regal
    clickXY(450, 1600)
    clickXY(860, 520, seconds=2)
    clickXY(860, 520)
    # Twisted
    clickXY(600, 1600)
    clickXY(860, 520, seconds=2)
    clickXY(860, 520)
    # Champion
    clickXY(750, 1600)
    clickXY(860, 520, seconds=2)
    clickXY(860, 520)
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
    print('    Collecting Daily Deals')
    swipe(200, 1825, 450, 1825, 500, seconds=2)
    clickXY(400, 1825)
    # Special Deal
    clickXY(150, 1675)
    click('buttons/dailydeals')
    clickXY(150, 1625)
    # Daily Deal
    clickXY(400, 1675)
    swipe(550, 1400, 550, 1200, 500, seconds=3)
    click('buttons/dailydeals')
    clickXY(400, 1675)
    # Biweeklies
    if d.isoweekday() == 7:
        print('    Collecting Biweekly Deals')
        clickXY(550, 1625)
        swipe(300, 1400, 200, 1200, 500, seconds=3)
        clickXY(200, 1200)
        clickXY(550, 1625)
    # Yuexi
    if d.isoweekday() == 1:
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
    printBlue('Merchant deals collected')