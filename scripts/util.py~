#!/usr/bin/env python
from devicewrapper.android import device as d
from uiautomator import device as dd
import unittest
import time
import sys
import os
import commands
import string
import random
import math

PACKAGE_NAME = 'com.intel.android.gallery3d'
ACTIVITY_NAME = PACKAGE_NAME + '/.app.Gallery'

#Resource-id for gallery main body, it does not change when switch between view
GALLEYBODY_RESID = 'com.intel.android.gallery3d:id/cardpop'

#Resource-id for action bar of gallery
ACTBAR_RESID = 'android:id/action_bar'

#All view could be entry
ViewModeList = {'AlbumeView': 0,
                'GridView': 1,
                'FullView': 2
                }

#All filter could be selected for gallery
FilterList = {'Albums': 'Albums',
              'Places': 'Places',
              'Events': 'Events',
              'Dates': 'Dates',
              'People': 'People'
              }

#Different capture mode shall have its own count changes
CaptureModeAndCountChanges = {'Single': 1,
                              'Video': 1,
                              'Burst': 10,
                              'Perfect': 9,
                              'Panorama': 1
                              }

#Different capture mode shall have its own file saving path
CaptureModeAndGrepFilter = {'Single': 'IMG',
                            'Video': 'VID',
                            'Burst': 'BST',
                            'Perfect': 'BST', #Waiting for confirm...
                            'Panorama': 'PAN'
                            }

COLUMN_MAX = 3
ROW_MAX = 4

#Get bounds info for the action bar
ACTBAR_BOUNDS = d(resourceId = ACTBAR_RESID).info.get('bounds')
#Get bounds info for the main body in gallery
BODY_BOUNDS = d(resourceId = GALLEYBODY_RESID).info.get('bounds')
#Get unit width/height for each item
UNIT_WIDTH = int((BODY_BOUNDS['right'] - BODY_BOUNDS['left'])/COLUMN_MAX)
UNIT_HEIGHT = int((BODY_BOUNDS['bottom'] - ACTBAR_BOUNDS['bottom'])/ROW_MAX)
#Get the pos for the first item(left-top corner)
FIRSTITEM_X = BODY_BOUNDS['left'] + UNIT_WIDTH/2
FIRSTITEM_Y = ACTBAR_BOUNDS['bottom'] + UNIT_HEIGHT/2

def holdFirstImage():
    d.swipe(FIRSTITEM_X,FIRSTITEM_Y,FIRSTITEM_X + 1,FIRSTITEM_Y + 1)

#Before using selectImages, the first image at the left-top corner shall be selected
def selectImages(selectCount):
    d.swipe(FIRSTITEM_X,FIRSTITEM_Y,FIRSTITEM_X + 1,FIRSTITEM_Y + 1)
    selectCount = selectCount - 1
    x = FIRSTITEM_X
    y = FIRSTITEM_Y + FIRSTITEM_Y
    while selectCount > 0:
        d.click(x, y)
        time.sleep(1)
        y = y + FIRSTITEM_Y
        #When y touch the boundry it means that it need swiching y back to the top
        if y > BODY_BOUNDS['bottom']:
            x = x + UNIT_WIDTH
            y = FIRSTITEM_Y
        #When x touch the boundry, it means that the images on the screen have all been highlighted. Need slide screen to a new page(without selected)
        if x > BODY_BOUNDS['right']:
            for i in range(0,COLUMN_MAX):
                d.swipe(UNIT_WIDTH*2, FIRSTITEM_Y, UNIT_WIDTH, FIRSTITEM_Y, steps = 20)
                time.sleep(1)
            #Reset x, y
            x = FIRSTITEM_X
            y = FIRSTITEM_Y
        selectCount = selectCount - 1


def launchGallery():
    d.start_activity(component = ACTIVITY_NAME)
    #Confirm gallery launch successfully by the icon on left-top corner
    assert d(text = 'Albums').wait.exists(timeout = 2000), 'Gallery launch failed'

def getPosForGalleryCenter():
    #Get bounds infomation for the main body, it includes{'left', 'right', 'top', 'bottom'}
    #BODY_BOUNDS = d(resourceId = GALLEYBODY_RESID).info.get('bounds')
    x = (BODY_BOUNDS['left'] + BODY_BOUNDS['right'])/2 #Calculate the abscissa of the main body's center
    y = (BODY_BOUNDS['top'] + BODY_BOUNDS['bottom'])/2 #Calculate the ordinate of the main body's center
    return x, y

def switchViewMode(viewmode):
    centerpos = getPosForGalleryCenter() #The value return from getPosForGalleryCenter is a list
    posx = centerpos[0] #Get abscissa from the list's first item
    posy = centerpos[1] #Get ordinate from the list's second item
    for i in range (0, ViewModeList[viewmode]):
        d.click(posx,posy) #Tap on the center pos




def selectFilter(galleryfilter):
    d(resourceId = 'android:id/text1').click.wait() #Tap on the left top corner
    assert d(text = 'Albums').wait.exists(timeout = 2000)
    #Click the selected viewmode
    d(text = FilterList[galleryfilter]).click.wait()

def selectPictueWhenEditBurst(imagesSelect):
    #Could display 5 pictures on selection bar at most, when the count of image selected bigger than 5, need swipe
    x = 70 #The abscissa of the first picture
    while imagesSelect > 0:
        d.click(x, 250)
        time.sleep(1) #Sometimes case failed if tap action is too fast
        x = x + 150 #The gap between two pictures are 150 pix
        if x > 700: #The left boundry of the fifth image, so if abscissa over than 600, need swipe
            d.swipe(650,250,1,250,steps=5)
            time.sleep(1)
            x = 70 #Reset the first abscissa
        imagesSelect = imagesSelect - 1

def showPopCard():
    time.sleep(2)
    d.click(350,100) #The center of the top action bar
    d.click(350,100) #Sometimes there is no response if tap here only once. Although it has poped up, tap here would do no thing for the case
    assert d(description = 'Share').wait.exists(timeout = 2000), 'Pop card does not display after tapping on the top bar twice'

def pushTestPicture(path,targetpath):
    pathDic = {'testAlbum': '/testalbum/ ',
               'testVideo': '/testvideo/ ',
               'testBurst': '/testburstpics/ '
                }
    targetpathDic = {'tarAlbum': '/testalbum/',
                     'tarBurst': '/DCIM/100ANDRO/',
                     'tarVideo': '/testvideo/'
                    }
    adbpushstr = 'adb push ' + sys.path[0] + '/resource' + pathDic[path] + ' /sdcard' + targetpathDic[targetpath]
    commands.getoutput(adbpushstr)
    #print adbpushstr
    commands.getoutput(REFRESH_MEDIA)




