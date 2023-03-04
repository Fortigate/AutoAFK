from tools import *

def collectAFKRewards():
    confirmLocation('campaign')
    if (isVisible('buttons/begin')):
        clickXY(550, 1550)
    click('buttons/collect')
    print('AFK Rewards collected')

def collectMail():
    if (pixelCheck(1012, 610, 2) > 240): # We check if the pixel where the notification sits has a red value of higher than 240
        clickXY(960, 630)
        click('buttons/collect_all')
        clickXY(550,1600)
        click('buttons/back')
        print('Mail collected')
    else:
        print('Mail not found')

def collectCompanionPoints():
    if (pixelCheck(1012, 790, 2) > 240):  # We check if the pixel where the notification sits has a red value of higher than 240
        wait()
        clickXY(960, 810)
        wait()
        click('buttons/sendandreceive')
        wait()
        click('buttons/back')
        wait()
        print('Friends Points Sent')
    else:
        print('Friends notification not found')

def collectFastRewards(count):
    counter = 0
    if (pixelCheck(980, 1620, 2) > 240):  # We check if the pixel where the notification sits has a red value of higher than 240
        print('Collecting Fast Rewards ' + str(count) + ' times')
        clickXY(950, 1660)
        while counter < count:
            # click('buttons/use')
            # clickXY(710, 1260)
            wait(2)
            # clickXY(550, 1800)
            print(counter)
            counter = counter+1
        click('buttons/close')
        print('Fast Rewards Done')
    else:
        print('Fast Rewards already done')

def attemptCampaign():
    confirmLocation('campaign')
    click('buttons/begin', seconds=2)
    if (isVisible('buttons/begin', 0.7)): # If we see second Begin it's a multi so we take a different route
        click('buttons/begin', 0.7, seconds=2)
        click('buttons/beginbattle', seconds=2)
        click('buttons/pause')
        click('buttons/exitbattle')
    else: # else it's a single
        click('buttons/battle', seconds=3)
        click('buttons/pause', 0.8)
        click('buttons/exitbattle')
    if (isVisible('buttons/back')):
        click('buttons/back')
        wait()
    if verifyLocation('campaign'):
        print('Campaign attempted')
    else:
        print('Something went wrong, attempted to return to campaign screen')
        returnToCampaign()

def handleBounties():
    confirmLocation('darkforest')
    clickXY(600, 1320)
    clickXY(650, 1700)
    click('buttons/collect_all')
    click('buttons/dispatch')
    click('buttons/confirm')
    clickXY(950,1700)
    click('buttons/collect_all')
    click('buttons/dispatch')
    click('buttons/confirm')
    click('buttons/back')
    print('Bounties attempted')

def handleArenaOfHeroes(count):
    counter = 0
    confirmLocation('darkforest')
    clickXY(740, 1050)
    clickXY(550, 50)
    click('labels/arenaofheroes')
    click('buttons/challenge')
    while counter < count:
        clickXY(820, 1225)
        click('buttons/battle', 0.6) # lower confidence as it's an animated button
        wait(2)
        click('buttons/skip')
        if (isVisible('labels/defeat')):
            print('Defeat!')
        else:
            print('Victory!')
            clickXY(550, 1800) # Clear loot popup
        clickXY(550, 1800)
        counter = counter+1
        print('Battle #' + str(counter) + ' complete!')
    click('buttons/exitmenu')
    click('buttons/back')
    click('buttons/back')
    print('arena done')

def handleKingsTower():
    confirmLocation('darkforest')
    clickXY(500, 870, seconds=3)
    clickXY(555, 585)
    click('buttons/challenge_plain', 0.6) # lower confidence for animated button
    click('buttons/beginbattle', 0.8, seconds=3)
    click('buttons/pause', 0.8)
    click('buttons/exitbattle')
    click('buttons/back')
    click('buttons/back')
    click('buttons/back')
    if verifyLocation('darkforest'):
        print('Tower attempted')
    else:
        print('Something went wrong, attempted to return to campaign screen')
        returnToCampaign()

def collectInnGifts():
    clicks = 0
    x_axis = 250

    confirmLocation('ranhorn')
    wait()
    clickXY(800,290)
    while clicks < 10:
        clickXY(x_axis, 1300, seconds=0.5)
        x_axis = x_axis + 50
        clicks = clicks + 2
        clickXY(550, 1400, seconds=0.5) # Clear loot
    click('buttons/back')
    print('Inn Gifts collected.')

def handleGuildHunts():
    confirmLocation('ranhorn')
    clickXY(380, 360)
    wait(6)
    clickXY(550, 1800) # Clear chests
    clickXY(290, 860)
    # Wrizz check
    if (isVisible('buttons/quickbattle')):
        click('buttons/quickbattle')
        clickXY(725, 1300)
        wait()
        clickXY(550, 1800)
    else:
        print('Wrizz quick battle not found')
    # Soren Check
    clickXY(970, 890)
    if (isVisible('buttons/quickbattle')):
        click('buttons/quickbattle')
        clickXY(725, 1300)
        wait()
        clickXY(550, 1800)
    else:
        print('Soren quick battle not found')
    clickXY(70, 1810)
    clickXY(70, 1810)
    print('guildhunts checked')

def collectQuests():
    clickXY(960, 250)
    clickXY(400, 1650) # Dailies
    if isVisible('labels/questcomplete'):
        clickXY(930, 680)
    while isVisible('buttons/fullquestchest'):
        click('buttons/fullquestchest', seconds=2)
        clickXY(400, 1650)
    clickXY(600, 1650) # Weeklies
    if isVisible('labels/questcomplete'):
        clickXY(930, 680)
    while isVisible('buttons/fullquestchest'):
        click('buttons/fullquestchest', seconds=2)
        clickXY(400, 1650)
    click('buttons/back')
    print('Quests done')
