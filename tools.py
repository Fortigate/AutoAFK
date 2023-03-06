from ppadb.client import Client
import cv2 as cv2
import pyscreeze
import time
from subprocess import *
import socket
import sys
import os

cwd = (os.path.dirname(__file__) + '\\')
os.system('color') # So colourful text works

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
    if adb_device_str[2:11] == 'localhost':
        adb_device = adb_device_str[2:16] # Extra letter needed if we manually connect
        # print(adb_device)
    if adb_device_str[2:10] != 'emulator' and adb_device_str[2:11] != 'localhost':
        printWarning('No devices found, attempting to find it automatically..')
        Popen([adbpath, 'connect', '127.0.0.1:' + str(portScan())], stdout=PIPE).communicate()[0]
        # Popen([adbpath, 'connect', '127.0.0.1:5575'], stdout=PIPE).communicate()[0] #faster testing
        adb_devices = Popen([adbpath, "devices"], stdout=PIPE).communicate()[0]  # Run 'adb.exe devices' and pipe output to string
        adb_device_str = str(adb_devices[26:40])  # trim the string to extract the first device
        adb_device = adb_device_str[2:16]

# If we don't find a device we use this to scan the odd ports between 5555 and 5587 which ADB uses, then try and conenct
# This is a very slow implementation, we can multithread it to speed it up
def portScan():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    start = time.time()
    adbport = ''

    printWarning('Starting port scan (between 5555-5587), this can take up to 30 seconds..')

    # Port scanner function
    def port_scan(port):
        try:
            s.connect(('127.0.0.1', port))
            return True
        except:
            pass

    # Scan ports
    for port in range(5555,5588):
        if port % 2 != 0: # ADB will only use odd port numbers in this range
            if port_scan(port):
                printGreen('ADB Device Found at port ' + str(port) + ' in ' + str(round((time.time() - start))) + ' seconds!')
                adbport = port
                break

    if adbport == '':
        printError('No device found! Exiting..')
        exit(1)

    return adbport

# Connects to the device through ADB using PPADB, the device name is currently staticly set
def connect_device():
    global device
    configureADB()
    adb = Client(host='127.0.0.1',port=5037)
    device = adb.device(adb_device) # connect to the device we extracted above
    if device == None:
        printError('No device found, often due to ADB errors. Please try manually connecting your client.')
        print('Debug lines:')
        print(adb_devices)
        exit(1)
    else:
        printGreen('Device ' + adb_device + ' successfully connected!')

# Takes a screenshot and saves it locally
def take_screenshot(device):
    image = device.screencap()
    with open('screen.png', 'wb') as f:
        f.write(image)

# Wait command, default 1 second
def wait(seconds=1):
    time.sleep(seconds)

# Returns True if the image is found, False if not
# Confidence value can be reduced for images with animations
def isVisible(image, confidence=0.9, seconds=1):
    take_screenshot(device)
    screenshot = cv2.imread(cwd + 'screen.png')
    search = cv2.imread(cwd + 'img\\' + image + '.png')
    res = pyscreeze.locate(search, screenshot, grayscale=False, confidence=confidence)
    wait(seconds)

    if res != None:
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
def click(image, confidence=0.9, seconds=1, retry=1, suppress=False):
    counter = 0
    take_screenshot(device)
    screenshot = cv2.imread(cwd + 'screen.png', 0)
    search = cv2.imread(cwd + 'img\\' + image + '.png', 0)
    res = pyscreeze.locate(search, screenshot, grayscale=False, confidence=confidence)

    if res == None and retry != 1:
        while counter < retry:
            take_screenshot(device)
            screenshot = cv2.imread(cwd + 'screen.png', 0)
            res = pyscreeze.locate(search, screenshot, grayscale=False, confidence=confidence)
            if res != None:
                x, y, w, h = res
                x_center = round(x + w / 2)
                y_center = round(y + h / 2)
                device.shell('input tap ' + str(x_center) + ' ' + str(y_center))
                wait(seconds)
                return
            if suppress is not True:
                printWarning('Retrying ' + image + ' search: ' + str(counter+1) + '/' + str(retry))
            counter = counter + 1
            wait(1)
    elif res != None:
        x, y, w, h = res
        x_center = round(x + w/2)
        y_center = round(y + h/2)
        device.shell('input tap ' + str(x_center) + ' ' + str(y_center))
        wait(seconds)
    else:
        if suppress is not True:
            printWarning('Image:' + image + ' not found!')
        wait(seconds)

# Checks the pixel at the XY coordinates, returns B,G,R value dependent on c variable
def pixelCheck(x,y,c,seconds=1):
    take_screenshot(device)
    screenshot = cv2.imread('screen.png')
    # print(screenshot[y, x , c])
    wait(seconds)
    return screenshot[y, x , c]

# Used to confirm which game screen we're currently sitting in, and change to if we're not.
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

COLOR = {
    "CYAN": "\033[96m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "RED": "\033[91m",
    "RESET": "\033[0m",
}

def printError(text):
    print(COLOR['RED'], text, COLOR['RESET'])

def printGreen(text):
    print(COLOR['GREEN'], text, COLOR['RESET'])

def printWarning(text):
    print(COLOR['YELLOW'], text, COLOR['RESET'])

def printBlue(text):
    print(COLOR['CYAN'], text, COLOR['RESET'])
