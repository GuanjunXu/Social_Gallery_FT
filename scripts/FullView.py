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

    def testSlidePictures(self):
        '''
            Summary: Slide the photo left 4 times then right 4 times
            Steps:   1.Enter full view
                     2.Slide the photo to right 4 times
                     3.Slide the photo to left 4 times
        '''
        #Step 2
        for i in range(4):
            self._slideImageRtoL()
            print i
        #Step 3
        for j in range(4):
            self._slideImageLtoR()
            print j

    def testCheckShareListIcons(self):
        '''
            Summary: Click share icon the share list would appear
            Steps:   1.Enter full view
                     2.Click share icon
        '''
        u.shareItem()
        assert d(text = 'See all').wait.exists(timeout = 2000)

    def testSharePictureToBlueTooth(self):
        '''
            Summary: Share 1 picture in bluetooth
            Steps:   1.Enter full view
                     2.Click share icon
                     3.Click bluetooth icon
        '''
        u.shareItem('Bluetooth')
        if d(text = 'Turn on').wait.exists(timeout = 2000):
            d(text = 'Turn on').click.wait()
        assert d(text = 'Scan for devices').wait.exists(timeout = 2000)

    def testSharePictureToPicasa(self):
        '''
            Summary: Share 1 picture in picasa
            Steps:   1.Enter full view
                     2.Click share icon
                     3.Click picasa icon
        '''
        u.shareItem('Picasa')
        assert d(text = 'Upload').wait.exists(timeout = 2000)

    def testSharePictureToMessaging(self):
        '''
            Summary: Share 1 picture in messaging
            Steps:   1.Enter full view
                     2.Click share icon
                     3.Click messaging icon
        '''
        u.shareItem('Messaging')
        assert d(text = 'New message').wait.exists(timeout = 2000)
        #Discard the new message
        d.press('menu')
        d(text = 'Discard').click.wait()

    def testSharePictureToOrkut(self):
        '''
            Summary: Share 1 picture in orkut
            Steps:   1.Enter full view
                     2.Click share icon
                     3.Click orkut icon
        '''
        u.shareItem('Orkut')
        assert d(text = 'Add a new account').wait.exists(timeout = 2000)

    def testSharePictureTowifidirect(self):
        '''
            Summary: Share 1 picture in Wi‑Fi Direct
            Steps:   1.Enter full view
                     2.Click share icon
                     3.Click Wi‑Fi Direct icon
        '''
        u.shareItem('Wi‑Fi Direct')
        assert d(text = 'Peer devices').wait.exists(timeout = 2000)

    def testSharePictureToGooglePlus(self):
        '''
            Summary: Share 1 picture in Google+
            Steps:   1.Enter full view
                     2.Click share icon
                     3.Click Google+ icon
        '''
        u.shareItem('Google+')
        if d(text = 'Choose account').wait.exists(timeout = 2000):
            d(resourceId = 'com.google.android.apps.plus:id/avatar').click.wait()
        assert d(text = 'Share').wait.exists(timeout = 2000)

    def testSharePictureToGmail(self):
        '''
            Summary: Share 1 picture in Gmail
            Steps:   1.Enter full view
                     2.Click share icon
                     3.Click Gmail icon
        '''
        u.shareItem('Gmail')
        assert d(text = 'Subject').wait.exists(timeout = 2000)

    def testSharePictureToDrive(self):
        '''
            Summary: Share 1 picture in Gmail
            Steps:   1.Enter full view
                     2.Click share icon
                     3.Click Gmail icon
        '''
        u.shareItem('Drive')
        assert d(text = 'Upload to Drive').wait.exists(timeout = 2000)

    def testSharePictureToFacebook(self):
        '''
            Summary: Share 1 picture in FaceBook
            Steps:   1.Enter full view
                     2.Click share icon
                     3.Click FaceBook icon
        '''
        u.shareItem('Facebook')
        assert d(text = 'Loading...').wait.exists(timeout = 2000)

    def testDeleteSingle(self):
        '''
            Summary: Delete the photo
            Steps:   1.Enter full view
                     2.Touch trash icon
                     3.Touch delete
        '''
        d(description = 'Delete').click.wait()
        d(text = 'Delete').click.wait()
        assert d(text = 'Delete').wait.gone(timeout = 5000)

    def testDeleteCancel(self):
        '''
            Summary: Delete the photo
            Steps:   1.Enter full view
                     2.Touch trash icon
                     3.Touch cancel
        '''
        d(description = 'Delete').click.wait()
        d(text = 'Cancel').click.wait()
        assert d(text = 'Delete').wait.gone(timeout = 5000)














    def _slideImageRtoL(self):
        #Swipe screen from right to left
        d.swipe(650,300,60,300,2)
        time.sleep(2)

    def _slideImageLtoR(self):
        #Swipe screen from left to right
        d.swipe(60,300,650,300,2)
        time.sleep(2)

    