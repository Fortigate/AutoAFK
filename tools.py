from ppadb.client import Client
from AutoAFK import printGreen, printError, printWarning, printBlue, settings
from pyscreeze import locate, locateAll
from subprocess import check_output, Popen, PIPE
import cv2
import time
import socket
import os
import configparser
import sys
import numbers

config = configparser.ConfigParser()
config.read(settings)
cwd = (os.path.dirname(__file__) + '\\')
os.system('color')  # So colourful text works
connected = False

# Expands the left and right button menus
def expandMenus():
    while isVisible('buttons/downarrow', 0.8):
        click('buttons/downarrow', 0.8, retry=3)

# Checks if AFK Arena process is running, if not we launch it
def afkRunningCheck():
    livegame = str(device.shell('ps | grep -E com.lilithgame.hgame.gp | awk \'{print$9}\'')).splitlines()
    testgame = str(device.shell('ps | grep -E com.lilithgames.hgame.gp.id | awk \'{print$9}\'')).splitlines()
    if not livegame and not testgame:
        printError('AFK Arena is not running, launching..')
        device.shell('monkey -p com.lilithgame.hgame.gp 1')

# Confirms that the game has loaded by checking for the campaign_selected button. Also presses exitmenu.png to clear any new hero popups
# May also require a ClickXY over Campaign to clear Time Limited Deals that appear
def waitUntilGameActive():
    printWarning('Searching for Campaign screen..')
    loadingcounter = 0
    timeoutcounter = 0
    while loadingcounter < 1:
        clickXY(550, 1850)
        click('buttons/campaign_unselected', seconds=0.5, suppress=True)
        click('buttons/exitmenu', seconds=0.5, suppress=True)
        click('buttons/exitmenu_trial', seconds=0.5, suppress=True)
        click('buttons/back', seconds=0.5, suppress=True)
        timeoutcounter += 1
        if isVisible('buttons/campaign_selected', 0.5):
            loadingcounter += 1
        if timeoutcounter > 10:
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
# This returns a UnicodeDecodeError on some systems despite using 'sys.getdefaultencoding()'
def processExists(process_name):
    sysEncoding = sys.getdefaultencoding()
    printWarning('System encoding is: ' + sysEncoding)
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    output = check_output(call).decode(sysEncoding)
    last_line = output.strip().split('\r\n')[-1]
    return last_line.lower().startswith(process_name.lower())

# This function manages the ADB connection. It does not do it in a refined manner.
# First it restarts ADB then checks for `emulator-xxxx` devices, if empty we check for `localhost:xxxx` devices
# If neither are found we use portScan() to find the active port and connect using that
def configureADB():
    global adb_device
    global adb_devices
    adbpath = (os.path.dirname(__file__) + '\\adb.exe') # Locate adb.exe in working directory
    Popen([adbpath, "kill-server"], stdout=PIPE).communicate()[0] # Restart the server
    wait(2)
    adb_devices = Popen([adbpath, "devices"], stdout=PIPE).communicate()[0] # Run 'adb.exe devices' and pipe output to string
    adb_device_str = str(adb_devices[26:40]) # trim the string to extract the first device
    adb_device = adb_device_str[2:15] # trim again because it's a byte object and has extra characters
    # print(adb_device)
    # processID = Popen('powershell.exe Write-Output (Get-Process -Name "HD-Player").Id', stdout=PIPE).communicate()[0]
    # print(processID.strip())
    # ports = Popen('powershell.exe Write-Output(netstat -nao | Select-String ' + str(processID) + ' | Select-String \'127.0.0.1\' | Select-String \'Listening\'\)', stdout=PIPE).communicate()[0]
    # print(ports)
    if adb_device_str[2:11] == 'localhost':
        adb_device = adb_device_str[2:16] # Extra letter needed if we manually connect
        # print(adb_device)
    if adb_device_str[2:10] != 'emulator' and adb_device_str[2:11] != 'localhost':
        Popen([adbpath, 'connect', '127.0.0.1:' + str(portScan())], stdout=PIPE).communicate()[0]
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
    if ':' in str(port):
        printError('Port entered includes the : symbol, it should only be the last 4 or 5 digits not the full IP:Port address. Exiting..')
        exit()
    if int(port) == 5037:
        printError('Port 5037 has been entered, this is the port of the ADB connection service not the emulator, check BlueStacks Settings - Preferences to get the ADB port number')
        exit()
    if int(port) != 0:
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
        exit(1)

    return adbport

# Connects to the found ADB device using PPADB, allowing us to send commands via Python
# On success we go through our startup checks to make sure we are starting from the same point each time, and can recognise the template images
def connect_device():
    config.read(settings) # To update any new values before we run activities
    global connected  # So we don't reconnect with every new activity
    if connected is True:
        return
    printGreen('Attempting to connect, make sure that BlueStacks is running!')
    # if processExists('HD-Player.exe'):
    #     printGreen('Bluestacks found! Trying to connect via ADB..')
    # else:
    #     printError('Bluestacks not found (no running process: HD-Player.exe), please make sure it\'s running before launching!')
    #     printWarning('Trying to continue in case we are wrong..')
    global device
    configureADB()
    adb = Client(host='127.0.0.1', port=5037)
    device = adb.device(adb_device) # connect to the device we extracted above
    if device == None:
        printError('No ADB device found, often due to ADB errors. Please try manually connecting your client.')
        print('Debug lines:')
        print(adb_devices)
        exit(1)
    else:
        printGreen('Device: ' + adb_device + ' successfully connected!')
        resolutionCheck(device)
        afkRunningCheck()
        waitUntilGameActive()
        expandMenus()
        connected = True
        print('')

# Takes a screenshot and saves it locally
def take_screenshot(device):
    image = device.screencap()
    with open('screen.bin', 'wb') as f:
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

def swipe(x1, y1, x2, y2, duration=100, seconds=1):
    device.shell('input swipe ' + str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2) + ' ' + str(duration))
    wait(seconds)


# Returns True if the image is found, False if not
# Confidence value can be reduced for images with animations
def isVisible(image, confidence=0.9, seconds=1, click=False):
    take_screenshot(device)
    screenshot = cv2.imread(cwd + 'screen.bin')
    search = cv2.imread(cwd + 'img\\' + image + '.png')
    res = locate(search, screenshot, grayscale=False, confidence=confidence)
    wait(seconds)

    if res != None:
        if click is True:
            x, y, w, h = res
            x_center = round(x + w / 2)
            y_center = round(y + h / 2)
            device.shell('input tap ' + str(x_center) + ' ' + str(y_center))
        return True
    else:
        return False

# Clicks on the given XY coordinates
def clickXY(x,y, seconds=1):
    device.shell('input tap ' + str(x) + ' ' + str(y))
    wait(seconds)

# If the given image is found, it will click on the center of it, if not returns "No image found"
# Confidence is how sure we are we have the right image, for animated icons we can lower the value
# Seconds is time to wait after clicking the image
# Retry will try and find the image x number of times, useful for animated or covered buttons, or to make sure the button is not skipped
# Suppress will disable warnings, sometimes we don't need to know if a button isn't found
def click(image, confidence=0.9, seconds=1, retry=1, suppress=False, grayscale=False):
    counter = 0
    take_screenshot(device)
    screenshot = cv2.imread(cwd + 'screen.bin', 0)
    search = cv2.imread(cwd + 'img\\' + image + '.png', 0)
    result = locate(search, screenshot, grayscale=grayscale, confidence=confidence)

    if result == None and retry != 1:
        while counter < retry:
            take_screenshot(device)
            screenshot = cv2.imread(cwd + 'screen.bin', 0)
            result = locate(search, screenshot, grayscale=grayscale, confidence=confidence)
            if result != None:
                x, y, w, h = result
                x_center = round(x + w / 2)
                y_center = round(y + h / 2)
                device.shell('input tap ' + str(x_center) + ' ' + str(y_center))
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
        device.shell('input tap ' + str(x_center) + ' ' + str(y_center))
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
    screenshot = cv2.imread(cwd + 'screen.bin', 0)
    search = cv2.imread(cwd + 'img\\' + image + '.png', 0)
    results = list(locateAll(search, screenshot, grayscale=False, confidence=confidence))
    if len(results) == 0:
        printError('clickMultipleChoice error, image:' + str(image) + ' not found')
        return
    if choice > len(results): # If the choice is higher than the amount of results we take the last result
        x, y, w, h = results[len(results)-1]
        x_center = round(x + w / 2)
        y_center = round(y + h / 2)
        device.shell('input tap ' + str(x_center) + ' ' + str(y_center))
        wait(seconds)
    else:
        x, y, w, h = results[choice-1] # -1 to match the array starting at 0
        x_center = round(x + w / 2)
        y_center = round(y + h / 2)
        device.shell('input tap ' + str(x_center) + ' ' + str(y_center))
        wait(seconds)

# Checks the pixel at the XY coordinates, returns B,G,R value dependent on c variable
def pixelCheck(x,y,c,seconds=1):
    take_screenshot(device)
    screenshot = cv2.imread('screen.bin')
    # print(screenshot[y, x , c])
    wait(seconds)
    return screenshot[y, x , c]

# Used to confirm which game screen we're currently sitting in, and change to if we're not.
# Very slow function, we should handle this more smarterly
def confirmLocation(location, change=True):
    detected = ''

    if (isVisible('buttons/' + location  + '_selected')): # if we're in the right place break early
        return
    else:
        if (isVisible('buttons/campaign_selected', seconds=0)):
            detected = 'campaign'
        if (isVisible('buttons/darkforest_selected', seconds=0)):
            detected = 'darkforest'
        if (isVisible('buttons/ranhorn_selected', seconds=0)):
            detected = 'ranhorn'

    if detected != location and change is True:
        click('buttons/' + location + '_unselected')

# Returns True if `location` is found
def verifyLocation(location):
    detected = ''

    if (isVisible('buttons/' + location  + '_selected')): # if we're in the right place break early
        return True
    else:
        if (isVisible('buttons/campaign_selected')):
            detected = 'campaign'
        if (isVisible('buttons/darkforest_selected')):
            detected = 'darkforest'
        if (isVisible('buttons/ranhorn_selected')):
            detected = 'ranhorn'

    if detected != location:
        return False

# Last ditch effort to keep clicking the back button to return to a known location
# Should be updated to handle battle screen and screens without a back button
def recover():
    clickXY(70, 1810)
    clickXY(70, 1810)
    clickXY(70, 1810)
    confirmLocation('campaign')
    if verifyLocation('campaign'):
        printWarning('Recovered succesfully, continuing script')
    else:
        printError('Recovery failed, exiting')
        exit(0)