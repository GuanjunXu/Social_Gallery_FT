#!/usr/bin/python
# coding:utf-8

from devicewrapper.android import device as d
import unittest
import commands
import string
import time
import sys
import util

u = util.Util()

PACKAGE_NAME = 'com.intel.android.gallery3d'
ACTIVITY_NAME = PACKAGE_NAME + '/.app.Gallery'

class GalleryTest(unittest.TestCase):
    def setUp(self):
        super(GalleryTest,self).setUp()
        u._clearAllResource()
        u._confirmResourceExists()
        u.launchGallery()
        u.enterXView('fullview')
        u.showPopCard()

    def tearDown(self):
        super(GalleryTest,self).tearDown()
        u.pressBack(4)

    def testRotateLeftInSettingMenu(self):
        '''
            Summary: Rotate left in setting menu
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch Rotate left
                     4.Repeat 2-3 steps 4 times
        '''
        for i in range(4):
            u.setMenuOptions('Rotate left')
            assert d(text = 'Rotate left').wait.gone(timeout = 2000)

    def testRotateRightInSettingMenu(self):
        '''
            Summary: Rotate left in setting menu
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch Rotate right
                     4.Repeat 2-3 steps 4 times
        '''
        for i in range(4):
            u.setMenuOptions('Rotate right')
            assert d(text = 'Rotate right').wait.gone(timeout = 2000)

    def testCropThePhoto(self):
        '''
            Summary: Crop the photo
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Click crop 
                     4.Click crop
        '''
        u.setMenuOptions('Crop')
        assert d(text = 'Crop picture').wait.exists(timeout = 3000)
        d(text = 'Crop').click.wait()
        assert d(text = 'Crop').wait.gone(timeout = 2000)

    def testCropCancel(self):
        '''
            Summary: Crop cancel 
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Click crop 
                     4.Click cancel
        '''
        u.setMenuOptions('Crop')
        assert d(text = 'Crop picture').wait.exists(timeout = 3000)
        d(text = 'Cancel').click.wait()
        assert d(text = 'Crop').wait.gone(timeout = 2000)

    def testCheckDetail(self):
        '''
            Summary: Check Details by setting menu 
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Click Details Item
                     4.Click close
        '''
        u.setMenuOptions('Details')
        assert d(resourceId = 'com.intel.android.gallery3d:id/facebook_icon').wait.exists(timeout = 2000)

    def testAddKeyWords(self):
        '''
            Summary: Add keywords by setting meny 
            Steps:   1.Enter full view
                     2.Add keywords in settings bar
                     3.Click “+” to add new keywords to this photo
        '''
        u.setMenuOptions('Details')
        d.swipe(500,1050,500,200) #Swipe detail list up
        d(resourceId = 'com.intel.android.gallery3d:id/addKeywordButton').click.wait()
        d(text = 'Enter new keyword').click.wait() #Make sure keyboard has been invoked
        d(text = 'Enter new keyword').set_text('NewKeyword')
        self._tapOnDoneButton()
        assert d(text = 'NewKeyword',className = 'android.widget.TextView').wait.exists(timeout = 2000)
        
    def testAddEvent(self):
        '''
            Summary: Add event by setting meny
            Steps:   1.Enter full view
                     2.Add event in settings bar
        '''
        u.setMenuOptions('Details')
        d(resourceId = 'com.intel.android.gallery3d:id/event_edit').click.wait()
        d(text = 'Enter new event').click.wait() #Make sure keyboard has been invoked
        d(text = 'Enter new event').set_text('NewEvent')
        self._tapOnDoneButton()
        assert d(text = 'NewEvent',resourceId = 'com.intel.android.gallery3d:id/event_text').wait.exists(timeout = 2000)

    def testAddVenue(self):
        '''
            Summary: Add venue by setting meny
            Steps:   1.Enter full view
                     2.Add venue in settings bar
        '''
        u.setMenuOptions('Details')
        d(resourceId = 'com.intel.android.gallery3d:id/venue_edit').click.wait()
        d(text = 'Enter new venue').click.wait() #Make sure keyboard has been invoked
        d(text = 'Enter new venue').set_text('NewVenue')
        self._tapOnDoneButton()
        assert d(text = 'NewVenue',resourceId = 'com.intel.android.gallery3d:id/venue_text').wait.exists(timeout = 2000)

    def testSetPicAsContact(self):
        '''
            Summary: Set picture as contact photo
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Click Set picture as 
                     4.Click Contact photo
        '''
        self._setPicAs('contact')
        assert d(text = '   Find contacts').wait.exists(timeout = 2000)

    def testSetPicAsWallpaper(self):
        '''
            Summary: Set picture as wallpaper
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Click Set picture as 
                     4.Click wallpaper
        '''
        self._setPicAs('wallpaper')
        #Set default action for croping picture
        if d(text = 'Complete action using').wait.exists(timeout = 2000):
            try:
                assert d(text = 'Always', enabled = 'true').wait.exists(timeout = 2000)
            except:
                d(text = 'com.intel.android.gallery3d').click.wait()
            finally:
                d(text = 'Always').click.wait()
        assert d(text = 'Set wallpaper').wait.exists(timeout = 2000)
        d(text = 'Crop').click.wait()
        assert d(text = 'Set wallpaper').wait.gone(timeout = 2000)

    def testSetPicAsWallpaperCancel(self):
        '''
            Summary: Cancel Set picture as wallpaper
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Click Set picture as 
                     4.Click Wallpaper
                     5.Click cancel
        '''
        self._setPicAs('wallpaper')
        #Set default action for croping picture
        if d(text = 'Complete action using').wait.exists(timeout = 2000):
            try:
                assert d(text = 'Always', enabled = 'true').wait.exists(timeout = 2000)
            except:
                d(text = 'com.intel.android.gallery3d').click.wait()
            finally:
                d(text = 'Always').click.wait()
        assert d(text = 'Set wallpaper').wait.exists(timeout = 2000)
        d(text = 'Cancel').click.wait()
        assert d(text = 'Set wallpaper').wait.gone(timeout = 2000)

















    def _setPicAs(self,setact):
        d.press('menu')
        d(text = 'Set picture as').click.wait()
        setmode = {'contact':'Contact photo', 'wallpaper':'com.intel.android.gallery3d'}
        d(text = setmode[setact]).click.wait()

    def _tapOnDoneButton(self):
        #Touch on Done button on the soft keyboard
        d.click(650,1130)





    
