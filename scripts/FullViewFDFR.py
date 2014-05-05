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
        self._enableFDFR()

    def tearDown(self):
        super(GalleryTest,self).tearDown()
        u.pressBack(4)

    def testFaceRecognized(self):
        '''
            Summary: Test face recognized
            Steps:   1. Launch gallery and open a picture has unrecognized face
                     2. Tap on the face into contact list
                     3. Create a new contact and input name, click done
                     4. When into crop picture interface, tap on crop
        '''
        u.tapOnCenter()
        assert d(text = 'Create new contact').wait.exists(timeout = 2000)
        d(text = 'Create new contact').click.wait()
        if d(text = 'OK').wait.exists(timeout = 2000):
            d(text = 'OK').click.wait()
        d(text = 'Name').click.wait() #Make sure keyboard has been invoked
        d(text = 'Name').set_text('NewContact')
        d(text = 'Done').click.wait() #Save the contact
        assert d(text = 'Crop').wait.exists(timeout = 2000)
        d(text = 'Crop').click.wait()
        assert d(text = 'Crop').wait.gone(timeout = 2000)

    def testTurnFDFROnOff(self):
        '''
            Summary: Test turn on/off FD/FR icon
            Steps:   1. Launch gallery and open a picture
                     2. Press menu key
                     3. Turn on/off FD/FR icon
        '''
        #










    def _enableFDFR(self):
        u.showPopCard()
        d.press('menu')
        if d(text = 'Face recognition on').wait.exists(timeout = 2000):
            d(text = 'Face recognition on').click.wait()
        else:
            d.press('menu')
