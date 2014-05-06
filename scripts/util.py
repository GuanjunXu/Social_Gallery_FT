#!/usr/bin/env python
from devicewrapper.android import device as d
from uiautomator import device as dd
import unittest
import time
import sys
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

#Commands for refreshing media
REFRESH_MEDIA = 'adb shell am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///sdcard'

#All view could be entry
ViewModeList = ['albumview', 'gridview', 'fullview']

COLUMN_MAX    = 3
ROW_MAX       = 4

# #Get bounds info for the action bar
# ACTBAR_BOUNDS = d(resourceid = ACTBAR_RESID).info.get('bounds')
# #Get bounds info for the main body in gallery
# BODY_BOUNDS   = d(resourceId = GALLEYBODY_RESID).info.get('bounds')
#Get unit width/height for each item
# UNIT_WIDTH    = int((BODY_BOUNDS['right'] - BODY_BOUNDS['left'])/COLUMN_MAX)
# UNIT_HEIGHT   = int((BODY_BOUNDS['bottom'] - ACTBAR_BOUNDS['bottom'])/ROW_MAX)
# #Get the pos for the first item(left-top corner)
# FIRSTITEM_X   = BODY_BOUNDS['left'] + UNIT_WIDTH/2
# FIRSTITEM_Y   = ACTBAR_BOUNDS['bottom'] + UNIT_HEIGHT/2
# #Get pos for the center
# CENTER_X      = (BODY_BOUNDS['left'] + BODY_BOUNDS['right'])/2
# CENTER_Y      = (BODY_BOUNDS['top'] + BODY_BOUNDS['bottom'])/2

class Util():
    def __init__(self):
        pass

    def holdFirstImage(self):
        d.swipe(FIRSTITEM_X,FIRSTITEM_Y,FIRSTITEM_X + 1,FIRSTITEM_Y + 1)    

    #Before using selectImages, the first image at the left-top corner shall be selected
    def selectImages(self,selectCount):
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

    def launchGallery(self):
        d.start_activity(component = ACTIVITY_NAME)
        #Confirm gallery launch successfully by the icon on left-top corner
        assert d(text = 'Albums').wait.exists(timeout = 3000), 'Gallery launch failed'      

    def selectFilter(self,galleryfilter):
        d(resourceId = 'android:id/text1').click.wait() #Tap on the left top corner
        assert d(text = 'Albums').wait.exists(timeout = 2000)
        #Click the selected viewmode
        d(text = galleryfilter).click.wait()    

    def selectPictueWhenEditBurst(self,imagesSelect):
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

    def showPopCard(self):
        d.click(350,100).wait(1000) #The center of the top action bar
        d.click(350,100).wait(1000) #Sometimes there is no response if tap here only once. Although it has poped up, tap here would do no thing for the case
        assert d(description = 'Share').wait.exists(timeout = 2000), 'Pop card does not display after tapping on the top bar twice'       

#@#@#@##@#@#@##@#@#@##@#@#@##@#@#@##@#@#@##@#@#@##@#@#@##@#@#@##@#@#@##@#@#@##@#@#@##@#@#@##@#@#@##@#@#@##@#@#@##@#@#@#

    def _deleteFoldersInDCIM(self):
        picNo = commands.getoutput('adb shell ls -l /mnt/sdcard/DCIM/100ANDRO/ | wc -l')
        if string.atoi(picNo) != 0:
            commands.getoutput('adb shell rm -r /mnt/sdcard/DCIM/100ANDRO/*')
        commands.getoutput('adb shell am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///sdcard')
    
    def _deleteConvertFile(self):
        """
        Delete Convert File in /sdcard/Sharing/
        """
        resultNO1 = commands.getoutput('adb shell ls -l /sdcard/ | grep Sharing | wc -l')
        if string.atoi(resultNO1) !=0:
            resultNO2 = commands.getoutput('adb shell ls -l /sdcard/Sharing/ | wc -l')
            if string.atoi(resultNO2) != 0 :
                commands.getoutput('adb shell rm -r /sdcard/Sharing/*')
        commands.getoutput('adb shell am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///sdcard')
        
    def _clearAllResource(self):
        self._deleteFoldersInDCIM()
        self._deleteTestResource()
        #delete /sdcard/Sharing/ Convert files
        self._deleteConvertFile()
    
    def _deleteTestResource(self):
        resultNO = commands.getoutput('adb shell ls -l /sdcard/ | grep test | wc -l')
        if string.atoi(resultNO) != 0 :
            commands.getoutput('adb shell rm -r /mnt/sdcard/test*')
        commands.getoutput('adb shell am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///sdcard')
    
    
    def _confirmResourceExists(self):
        """
        If not exists resource ,push the resource to sdcard
        """
        result = commands.getoutput('adb shell ls -l /sdcard/ | grep testalbum | wc -l')
        if string.atoi(result) == 0:
            self._clearAllResource()
            commands.getoutput('adb push ' + sys.path[0] + 'resource/testalbum/ ' + '/sdcard/testalbum')
            time.sleep(2)
        else:
            result1 = commands.getoutput('adb shell ls -l /sdcard/testalbum/test* | grep jpg | wc -l')
            if string.atoi(result1) != 40 :
                self._clearAllResource()
                commands.getoutput('adb push ' + sys.path[0] + 'resource/testalbum/ ' + '/sdcard/testalbum')
        commands.getoutput('adb shell am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///sdcard/')
        
    def _pushResourcesVideo(self):
        result2 = commands.getoutput('adb shell ls -l /sdcard/testvideo/ | grep 3gp | wc -l')
        if string.atoi(result2) == 0:
            commands.getoutput('adb push ' + sys.path[0] + 'resource/testvideo/ '+'/sdcard/testvideo')
            time.sleep(2)
        commands.getoutput('adb shell am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///sdcard')
    
    def _push1Picture(self):
        result = commands.getoutput('adb shell ls -l /sdcard/ | grep test | wc -l')
        resultNO = commands.getoutput('adb shell ls -l /sdcard/testpic1/ | grep jpg | wc -l')
        if string.atoi(result) != 1 :
            self._clearAllResource()
            commands.getoutput('adb push ' + sys.path[0] + 'resource/testpic1/ ' + '/sdcard/testpic1')
        elif string.atoi(resultNO) != 1:
            self._clearAllResource()
            commands.getoutput('adb push ' + sys.path[0] + 'resource/testpic1/ ' + '/sdcard/testpic1')
            
        commands.getoutput('adb shell am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///sdcard')
        
    def _pushConvertPicture(self):
        resultNO = commands.getoutput('adb shell ls -l /sdcard/testConvertPics/ | grep jpg | wc -l')
        if string.atoi(resultNO) == 0 :
            commands.getoutput('adb push ' + sys.path[0] + 'resource/testConvertPics/ ' + '/sdcard/testConvertPics')
        commands.getoutput('adb shell am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///sdcard')
    
    def _enterSingleView(self):
        commands.getoutput('adb shell input tap 355 706')
        time.sleep(2)
        commands.getoutput('adb shell input tap 355 706')
        time.sleep(3)
        
    def _enterGridView(self):
        commands.getoutput('adb shell input tap 355 706')
        time.sleep(2)
    
    def _discardGmailDraft(self):
        self.press('menu')
        self.touch('gmail_discard.png')
        self.touch('gmail_discard_OK.png')
    
    def _prepareVideo(self):
        resultNO = commands.getoutput('adb shell ls -l /sdcard/ | grep test | wc -l')
        if string.atoi(resultNO) != 1:
            self._clearAllResource()
            commands.getoutput('adb push ' + sys.path[0] + 'resource/testvideo/ ' + '/sdcard/testvideo')
            commands.getoutput('adb shell am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///sdcard')
        else:
            resultNo1 = commands.getoutput('adb shell ls -l /sdcard/ | grep testvideo | wc -l')
            if string.atoi(resultNo1) != 1:
                self._clearAllResource()
                commands.getoutput('adb push ' + sys.path[0] + 'resource/testvideo/ ' + '/sdcard/testvideo')
                commands.getoutput('adb shell am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///sdcard')
    
    def _checkBurstResource(self):
        self._deleteConvertFile()
        self._deleteTestResource()
        resultNO = commands.getoutput('adb shell ls -l /sdcard/DCIM/100ANDRO/ | wc -l')
        resultNO1 = commands.getoutput('adb shell ls -l /sdcard/DCIM/100ANDRO/ | grep BST | wc -l')
        if string.atoi(resultNO) != string.atoi(resultNO1):
            self._clearAllResource()
            commands.getoutput('adb push ' + sys.path[0] + 'resource/testburstpics/ ' + '/sdcard/DCIM/100ANDRO/')
            commands.getoutput('adb shell am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///sdcard')
        elif string.atoi(resultNO1) != 10 :
            self._clearAllResource()
            commands.getoutput('adb push ' + sys.path[0] + 'resource/testburstpics/ ' + '/sdcard/DCIM/100ANDRO/')
            commands.getoutput('adb shell am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///sdcard')
        time.sleep(5)
    
    def _getBurstPicturesNum(self):
        result = commands.getoutput('adb  shell ls -l /sdcard/DCIM/100ANDRO/ | grep BST | wc -l')
        return result
    
    def _getPictureNumber(self):
        result = commands.getoutput('adb shell ls -l /sdcard/test*/* | grep IM | wc -l')
        return result
        
    def _getConvertFileNum(self):
        """
        Get convert file number
        """
        result = commands.getoutput('adb shell ls /sdcard/Sharing/| wc -l')
        return result 
    
    def _getPictureNoInAndro(self):
        no = commands.getoutput('adb shell ls -l /mnt/sdcard/DCIM/100ANDRO/ | wc -l')
        return no

#@#@#@##@#@#@##@#@#@##@#@#@##@#@#@##@#@#@##@#@#@##@#@#@##@#@#@##@#@#@##@#@#@##@#@#@##@#@#@##@#@#@##@#@#@##@#@#@##@#@#@#


    def tapOnCenter(self):
        time.sleep(2)
        d.click(350,700)

    def enterXView(self,viewmode):
        for i in range (0, ViewModeList.index(viewmode)):
            self.tapOnCenter()
    
    def pressBack(self,touchtimes):
        for i in range(0,touchtimes):
            d.press('back')

    #Add on May 5th
    def shareItem(self,shareto = None):
        '''
            The function simulate user sharing items in gallery.
            Usage:
                If you want to share item with Facebook(this item at the bottom of the share list as default)
                
                -> shareItem('Facebook')
                
                *Do not write press menu/share icon step before using
        '''
        d(description = 'Share').click.wait() #Its description is 'Share' in each view
        if shareto != None:
            try:
                assert d(text = shareto).wait.exists(timeout = 2000)
            except:
                d(text = 'See all').click.wait() #Display all share path
            finally:
                try:
                    assert d(text = shareto).wait.exists(timeout = 2000)
                except:
                    d.swipe(500,1050,500,200) #Slide share list up
                finally:
                    d(text = shareto).click.wait() #Tap on the path you want to share to

    #Add on May 6th
    def setMenuOptions(self,setoption = None):
        d.press('menu')
        d(text = setoption).click.wait()
        
    #Add on May 6th
    def deleteItem(self,deleteoption):
        '''
           deleteoption has two args: Delete, Cancel(str type, initial capital), usage:

           -> deleteItem('Cancel')

           It means you will cancel deleting image/video file
        '''
        d(description = 'Delete').click.wait()
        d(text = deleteoption).click.wait()
        
