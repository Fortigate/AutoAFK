from ppadb.client import Client
import cv2 as cv2
import pyscreeze
import time

def connect_device():
    adb = Client(host='127.0.0.1',port=5037)
    global device
    device = adb.device("localhost:5575")
    if device == None:
        print('No device found!')
        exit(1)
    else:
        print('Device connected!')

def take_screenshot(device):
    image = device.screencap()
    with open('screen.png', 'wb') as f:
        f.write(image)

def wait(seconds=1):
    time.sleep(seconds)

def isVisible(image, confidence=0.9):
    take_screenshot(device)
    screenshot = cv2.imread('screen.png')
    search = cv2.imread('img/' + image + '.png')
    res = pyscreeze.locate(search, screenshot, grayscale=False, confidence=confidence)

    if res != None:
        return True
    else:
        return False

def clickXY(x,y, seconds=2):
    device.shell('input tap ' + str(x) + ' ' + str(y))
    wait(seconds)

def click(image, confidence=0.9, seconds=2):
    take_screenshot(device)
    screenshot = cv2.imread('screen.png', 0)
    search = cv2.imread('img/' + image + '.png', 0)
    res = pyscreeze.locate(search, screenshot, grayscale=False, confidence=confidence)

    if res != None:
        x, y, w, h = res
        x_center = round(x + w/2)
        y_center = round(y + h/2)
        print(x_center, y_center)
        device.shell('input tap ' + str(x_center) + ' ' + str(y_center))
        wait(seconds)
    else:
        print('Image not found!')

def pixelCheck(x,y,c):
    take_screenshot(device)
    screenshot = cv2.imread('screen.png')
    print(screenshot[y, x , c])
    return screenshot[y, x , c]

def confirmLocation(location, change=True):
    detected = ''

    if (isVisible('buttons/' + location  + '_selected')): # if we're in the right place break early
        return
    else:
        if (isVisible('buttons/campaign_selected')):
            detected = 'campaign'
        if (isVisible('buttons/darkforest_selected')):
            detected = 'darkforest'
        if (isVisible('buttons/ranhorn_selected')):
            detected = 'ranhorn'

    if detected != location and change is True:
        click('buttons/' + location + '_unselected')