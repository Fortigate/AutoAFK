# Imports
from ppadb.client import Client
from AutoAFK import printGreen, printError, printWarning, printBlue, settings, args
from pyscreeze import locate, locateAll
from subprocess import check_output, Popen, PIPE
import time, socket, os, configparser, sys, tools
from PIL import Image
from numpy import asarray
from shutil import which
from platform import system

# Configs/settings
config = configparser.ConfigParser()
config.read(settings) # load settings
cwd = os.path.dirname(__file__) # variable for current directory of AutoAFK.exe
os.system('color')  # So colourful text works
connected = False
connect_counter = 1

# Expands the left and right button menus
def expandMenus():
    while isVisible('buttons/downarrow', 0.8):
        click('buttons/downarrow', 0.8, retry=3)

# Checks if AFK Arena process is running, if not we launch it
def afkRunningCheck():
    if args['test']:
        # printError('AFK Arena Test Server is not running, launching..')
        device.shell('monkey -p  com.lilithgames.hgame.gp.id 1')
    elif not args['test']:
        # printError('AFK Arena is not running, launching..')
        device.shell('monkey -p com.lilithgame.hgame.gp 1')

# Confirms that the game has loaded by checking for the campaign_selected button. Also presses exitmenu.png to clear any new hero popups
# May also require a ClickXY over Campaign to clear Time Limited Deals that appear
def waitUntilGameActive():
    printWarning('Searching for Campaign screen..')
    loadingcounter = 0
    timeoutcounter = 0
    if args['dailies']:
        loaded = 3 # If we're running unattended we want to make real sure there's no delayed popups
    else:
        loaded = 1

    while loadingcounter < loaded:
        clickXY(550, 1850)
        buttons = [os.path.join('buttons', 'campaign_unselected'), os.path.join('buttons', 'exitmenu_trial')]
        for button in buttons:
            click(button, seconds=0, suppress=True)
        timeoutcounter += 1
        if isVisible('buttons/campaign_selected'):
            loadingcounter += 1
        if timeoutcounter > 30: # Long so patching etc doesn't lead to timeout
            printError('Timed out while loading!')
            sys.exit(1)
    printGreen('Game Loaded!')

# Checks we are running 1920x1080 (or 1080x1920 if we're in landscape mode) and 240 DPI, exits if not.
def resolutionCheck(device):
    resolution = device.shell('wm size').split(' ')
    dpi = device.shell('wm density').split(' ')
    if not str(resolution[2]).strip() == '1920x1080' and not str(resolution[2]).strip() == '1080x1920':
        printError('Unsupported Resolution! (' + str(resolution[2]).strip() + '). Please change your Bluestacks resolution to 1080x1920')
        exit(1)
    if str(dpi[2]).strip() != '240':
        printError('Unsupported DPI! (' + str(dpi[2]).strip() + '). Please change your Bluestacks DPI to 240')
        exit(1)

# Checks Windows running processes for Bluestacks.exe
# Depreciated as this returns a UnicodeDecodeError on some systems despite using 'sys.getdefaultencoding()'
def processExists(process_name):
    sysEncoding = sys.getdefaultencoding()
    printWarning('System encoding is: ' + sysEncoding)
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    output = check_output(call).decode(sysEncoding)
    last_line = output.strip().split('\r\n')[-1]
    return last_line.lower().startswith(process_name.lower())

# This function manages the ADB connection to Bluestacks. It does not do it in a refined manner.
# First it restarts ADB then checks for `emulator-xxxx` devices, if none found we check for `localhost:xxxx` devices
# If neither are found we run portScan() to find the active port and connect using that, or load one from settings
def configureADB():
    global adb_device
    global adb_devices
    config.read(settings)  # to load any new values (ie port changed and saved) into memory
    adbpath = os.path.join(cwd, 'adb.exe') # Locate adb.exe in working directory
    if system() != 'Windows' or not os.path.exists(adbpath):
        adbpath = which('adb') # If we're not on Windows or can't find adb.exe in the working directory we try and find it in the PATH
    Popen([adbpath, "kill-server"], stdout=PIPE).communicate()[0] # Restart the ADB server
    wait(2)
    adb_devices = Popen([adbpath, "devices"], stdout=PIPE).communicate()[0] # Run 'adb.exe devices' and pipe output to string
    adb_device_str = str(adb_devices[26:40]) # trim the string to extract the first device
    adb_device = adb_device_str[2:15] # trim again because it's a byte object and has extra characters
    if config.get('ADVANCED', 'port') == '':
        config.set('ADVANCED', 'port', '0') # So we don't throw a NaN error on the next if statement if the fields blank
    if config.getint('ADVANCED', 'port') != 0:
        printWarning('Port ' + str(config.get('ADVANCED', 'port')) + ' found in settings.ini, using that')
        adb_device = '127.0.0.1:'+str(config.get('ADVANCED', 'port'))
        Popen([adbpath, 'connect', adb_device], stdout=PIPE).communicate()[0]
        return
    if adb_device_str[2:11] == 'localhost':
        adb_device = adb_device_str[2:16] # Extra letter needed if we manually connect
    if adb_device_str[2:10] != 'emulator' and adb_device_str[2:11] != 'localhost': # If the ADB device output doesn't use these two prefixes then:
        Popen([adbpath, 'connect', '127.0.0.1:' + str(portScan())], stdout=PIPE).communicate()[0] # Here we run portScan()
        adb_devices = Popen([adbpath, "devices"], stdout=PIPE).communicate()[0]  # Run 'adb.exe devices' and pipe output to string
        adb_device_str = str(adb_devices[26:40])  # trim the string to extract the first device
        if len(str(config.get('ADVANCED', 'port'))) > 4:
            adb_device = '127.0.0.1:' + (str(config.get('ADVANCED', 'port')))
        else:
            adb_device = adb_device_str[2:16]

# If we don't find a device we use first check settings to see if a port has been manually defined and use that
# if not then we scan the odd ports between 5555 and 5599 to find the ADB port that bluestacks is using (note Hyper-V BS will use a port in the 10000+ range for reasons)
# This is a very slow implementation (1 second per port, up to 45 seconds for port 5599). We can multithread it to speed it up
# If no port is found we have exhausted all options to find the ADB device so will exit
def portScan():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    start = time.time()
    adbport = ''

    config.read(settings)  # to load any new values (ie port changed and saved) into memory
    port = config.get('ADVANCED', 'port')
    if port == '':
        port == 0
    elif ':' in str(port):
        printError('Port entered includes the : symbol, it should only be the last 4 or 5 digits not the full IP:Port address. Exiting..')
        sys.exit(1)
    elif int(port) == 5037:
        printError('Port 5037 has been entered, this is the port of the ADB connection service not the emulator, check BlueStacks Settings - Preferences to get the ADB port number')
        sys.exit(1)
    elif int(port) != 0:
        printGreen('Port: ' + str(config.get('ADVANCED', 'port')) + ' found in the settings.ini file, connecting using that..')
        adbport = int(config.get('ADVANCED', 'port'))
        return adbport

    printWarning('No ADB devices found, and no configured port in settings.ini. Scanning ADB ports to find it automatically, this can take up to 45 seconds..')

    # Port scanner function
    def port_scan(port):
        try:
            s.connect(('127.0.0.1', port))
            return True
        except:
            pass

    # Scan ports
    for port in range(5555,5599):
        if port % 2 != 0: # ADB will only use odd port numbers in this range
            if port_scan(port):
                printWarning('ADB Device Found at port ' + str(port) + ' in ' + str(round((time.time() - start))) + ' seconds!')
                adbport = port
                break

    if adbport == '':
        printError('No device found! Exiting..')
        sys.exit(1)

    return adbport

# Connects to the found ADB device using PPADB, allowing us to send commands via Python
# On success we go through our startup checks to make sure we are starting from the same point each time, and can recognise the template images
def connect_device():
    if tools.connect_counter == 1:
        printGreen('Attempting to connect, make sure that BlueStacks is running!')
    config.read(settings) # To update any new values before we run activities
    global connected  # So we don't reconnect with every new activity
    global device # Contains our located device
    if connected is True:
        return
    configureADB()
    adb = Client(host='127.0.0.1', port=5037)
    device = adb.device(adb_device) # connect to the device we extracted in configureADB()
    # PPADB can throw errors occasionally for no good reason, here we try and catch them and retry for stability
    while tools.connect_counter < 4:
        try:
            device.shell('echo Hello World!') # Arbitrary test command
        except Exception as e:
            if str(e) != 'ERROR: \'FAIL\' 000edevice offline': # Skip common device offline error as it still runs after that
                printError('PPADB Error: ' + str(e) + ', retrying ' + str(tools.connect_counter) + '/3')
                wait(3)
                tools.connect_counter+=1
                connect_device()
        else:
            break
    if device == None:
        printError('No ADB device found, often due to ADB errors. Please try manually connecting your client.')
        printWarning('Debug:')
        print(adb_devices.decode())
        sys.exit(1)
    else:
        printGreen('Device: ' + adb_device + ' successfully connected!')
        tools.connect_counter = 1 # reset counter just in case
        resolutionCheck(device) # Four start up checks, so we have an exact position/screen configuration to start with
        afkRunningCheck()
        waitUntilGameActive()
        expandMenus()
        connected = True
        print('')

# Takes a screenshot and saves it locally
def take_screenshot(device):
    image = device.screencap()
    with open(os.path.join(cwd, 'screen.bin'), 'wb') as f:
        f.write(image)

def save_screenshot(name):
    image = device.screencap()
    with open(name + '.png', 'wb') as f:
        f.write(image)

# Wait command, default 1 second
# Loading multiplier is defined in settings, it is a decimally notated % multiplier. E.G:
# 0.9 will run with 90% of the default wait times
# 2.0 will run with 200% of the default wait times
# This is handy for slower machines where we need to wait for sections/images to load
def wait(seconds=1):
    time.sleep(seconds * float(config.get('ADVANCED', 'loadingMuliplier')))

# Performs a swipe from X1/Y1 to X2/Y2 at the speed defined in duration
def swipe(x1, y1, x2, y2, duration=100, seconds=1):
    device.input_swipe(x1, y1, x2, y2, duration)
    wait(seconds)

# Returns True if the image is found, False if not
# Confidence value can be reduced for images with animations
# Retry for retrying image search
def isVisible(image, confidence=0.9, seconds=1, retry=1, click=False):
    counter = 0
    take_screenshot(device)
    screenshot = Image.open(os.path.join(cwd, 'screen.bin'))
    search = Image.open(os.path.join(cwd, 'img', image + '.png'))
    res = locate(search, screenshot, grayscale=False, confidence=confidence)

    if res == None and retry != 1:
        while counter < retry:
            res = locate(search, screenshot, grayscale=False, confidence=confidence)
            if res != None:
                if click is True:
                    x, y, w, h = res
                    x_center = round(x + w / 2)
                    y_center = round(y + h / 2)
                    device.input_tap(x_center, y_center)
                wait(seconds)
                return True
            counter = counter + 1
    elif res != None:
        if click is True:
            x, y, w, h = res
            x_center = round(x + w / 2)
            y_center = round(y + h / 2)
            device.input_tap(x_center, y_center)
        wait(seconds)
        return True
    else:
        wait(seconds)
        return False

# Clicks on the given XY coordinates
def clickXY(x,y, seconds=1):
    device.input_tap(x, y)
    wait(seconds)

# If the given image is found, it will click on the center of it, if not returns "No image found"
# Confidence is how sure we are we have the right image, for animated icons we can lower the value
# Seconds is time to wait after clicking the image
# Retry will try and find the image x number of times, useful for animated or covered buttons, or to make sure the button is not skipped
# Suppress will disable warnings, sometimes we don't need to know if a button isn't found
def click(image, confidence=0.9, seconds=1, retry=1, suppress=False, grayscale=False):
    counter = 0
    take_screenshot(device)
    screenshot = Image.open(os.path.join(cwd, 'screen.bin'))
    search = Image.open(os.path.join(cwd, 'img', image + '.png'))
    result = locate(search, screenshot, grayscale=grayscale, confidence=confidence)

    if result == None and retry != 1:
        while counter < retry:
            take_screenshot(device)
            screenshot = Image.open(os.path.join(cwd, 'screen.bin'))
            result = locate(search, screenshot, grayscale=grayscale, confidence=confidence)
            if result != None:
                x, y, w, h = result
                x_center = round(x + w / 2)
                y_center = round(y + h / 2)
                device.input_tap(x_center, y_center)
                wait(seconds)
                return
            if suppress is not True:
                printWarning('Retrying ' + image + ' search: ' + str(counter+1) + '/' + str(retry))
            counter = counter + 1
            wait(1)
    elif result != None:
        x, y, w, h = result
        x_center = round(x + w/2)
        y_center = round(y + h/2)
        device.input_tap(x_center, y_center)
        wait(seconds)
    else:
        if suppress is not True:
            printWarning('Image:' + image + ' not found!')
        wait(seconds)

# Searchs for all matchs of the found image and stores them in a list, from there we select which one we want to click with 'choice'
# If choice is higher than the found image we default to last found Image in the list
# Choice is which image we click starting at '1', we search from top left line by line, and they will be ordered as found
# Confidence is confidence in the found image, it needs to be tight here, or we have multiple entries for the same image
# Seconds is how long to pause after finding the image
def clickMultipleChoice(image, choice, confidence=0.9, seconds=1):
    take_screenshot(device)
    screenshot = Image.open(os.path.join(cwd, 'screen.bin'))
    search = Image.open(os.path.join(cwd, 'img', image + '.png'))
    results = list(locateAll(search, screenshot, grayscale=False, confidence=confidence))
    if len(results) == 0:
        printError('clickMultipleChoice error, image:' + str(image) + ' not found')
        return
    if choice > len(results): # If the choice is higher than the amount of results we take the last result
        x, y, w, h = results[len(results)-1]
        x_center = round(x + w / 2)
        y_center = round(y + h / 2)
        device.input_tap(x_center, y_center)
        wait(seconds)
    else:
        x, y, w, h = results[choice-1] # -1 to match the array starting at 0
        x_center = round(x + w / 2)
        y_center = round(y + h / 2)
        device.input_tap(x_center, y_center)
        wait(seconds)

def returnMultiple(image, confidence=0.9, seconds=1):
    take_screenshot(device)
    screenshot = Image.open(os.path.join(cwd, 'screen.bin'))
    search = Image.open(os.path.join(cwd, 'img', image + '.png'))
    results = list(locateAll(search, screenshot, grayscale=False, confidence=confidence))
    return results

# Checks the pixel at the XY coordinates
# C Variable is array from 0 to 2 for RGB value
def pixelCheck(x,y,c,seconds=1):
    take_screenshot(device)
    screenshot = asarray(Image.open(os.path.join(cwd, 'screen.bin'))) # Convert PIL Image to NumPy Array for tuples
    wait(seconds)
    return screenshot[y, x, c]

def returnCardPullsRarity():
    take_screenshot(device)
    screenshot = asarray(Image.open(os.path.join(cwd, 'screen.bin')))  # Convert PIL Image to NumPy Array for tuples
    cards = {'1': [95, 550], '2': [95, 900], '3': [95, 1350], '4': [410, 250], '5': [410, 650], '6': [410, 1100], '7': [410, 1550], '8': [729, 550], '9': [729, 900], '10': [729, 1350]}

    for card, location in cards.items(): # screenshot[] searchs Y first then X for reasons, so the locations[] are reversed
        if screenshot[location[1], location[0], 0] > 200 and screenshot[location[1], location[0], 1] > 200: # Red and Green > 200 = Yellow border
            return 'Awakened'

    for card, location in cards.items():
        if screenshot[location[1], location[0], 0] > 200 and screenshot[location[1], location[0], 2] > 200: # Red and Blue > 200 = Purple border
            return 'Epic'

    return 'Rare'

# def returnAwakened():
#     take_screenshot(device)
#     screenshot = Image.open(cwd + 'screen.bin')
#     wokes = {'Awakened Talene': 'aTalene', 'Gavus': 'Gavus', 'Maetria': 'Maetria', 'Awakened Ezizh': 'aEzizh',
#              'Awakened Thane': 'aThane', 'Awakened Belinda': 'aBelinda', 'Awakened Brutus': 'aBrutus',
#              'Awakened Safiya': 'aSafiya', 'Awakened Lyca': 'aLyca', 'Awakened Solise': 'aSolise',
#              'Awakened Baden': 'aBaden', 'Awakened Shemira': 'aShemira', 'Awakened Athalia': 'aAthalia'}
#
#     for awakened, imageloc in wokes.items():
#         search = Image.open(cwd + 'img\\summons\\awakeneds\\' + imageloc + '.png')
#         res = locate(search, screenshot, grayscale=False, confidence=0.85)
#         if res != None:
#             return awakened
#     return 'Unknown'
#
# def returnCeleHypo():
#     take_screenshot(device)
#     screenshot = Image.open(cwd + 'screen.bin')
#     celehypos = {'Awakened Talene': 'aTalene', 'Gavus': 'Gavus', 'Maetria': 'Maetria', 'Awakened Ezizh': 'aEzizh',
#              'Awakened Thane': 'aThane', 'Awakened Belinda': 'aBelinda', 'Awakened Brutus': 'aBrutus',
#              'Awakened Safiya': 'aSafiya', 'Awakened Lyca': 'aLyca', 'Awakened Solise': 'aSolise',
#              'Awakened Baden': 'aBaden', 'Awakened Shemira': 'aShemira', 'Awakened Athalia': 'aAthalia'}
#
#     for celehypo, imageloc in celehypos.items():
#         search = Image.open(cwd + 'img\\summons\\awakeneds\\' + imageloc + '.png')
#         res = locate(search, screenshot, grayscale=False, confidence=0.85)
#         if res != None:
#             return celehypo
#     return "Unknown or 4F Epic"

# Used to confirm which game screen we're currently sitting in, and change to if we're not.
# Optionally with 'bool' flag we can return boolean for if statements
def confirmLocation(location, change=True, bool=False):
    detected = ''
    locations = {'campaign_selected': 'campaign', 'darkforest_selected': 'darkforest', 'ranhorn_selected': 'ranhorn'}
    take_screenshot(device)
    screenshot = Image.open(os.path.join(cwd, 'screen.bin'))
    for location_button, string in locations.items():
        search = Image.open(os.path.join(cwd, 'img', 'buttons', location_button + '.png'))
        res = locate(search, screenshot, grayscale=False)
        if res != None:
            detected = string
            break

    if detected == location and bool is True:
        return True
    elif detected != location and change is True and bool is False:
        click(os.path.join('buttons', location + '_unselected'))
    elif detected != location and bool is True:
        return False

# Last ditch effort to keep clicking the back button to return to a known location
# TODO update to handle battle screen and screens without a back button
def recover():
    clickXY(70, 1810)
    clickXY(70, 1810)
    clickXY(70, 1810)
    confirmLocation('campaign')
    if confirmLocation('campaign', bool=True):
        printWarning('Recovered succesfully')
    else:
        printError('Recovery failed, exiting')
        exit(0)