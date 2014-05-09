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
        self._turnFDFR('On')
        self._removeIdentity()

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
        d(text = 'Done').click.wait() #Try to save the contact
        #Below is to go to the editing screen
        if d(text = 'Cancel').wait.exists(timeout = 2000):
            d(text = 'Cancel').click.wait()
            d(text = 'Done').click.wait()
        time.sleep(2) #Hold a few seconds util it jump to the croping screen
        assert d(text = 'Crop').wait.exists(timeout = 2000)
        d(text = 'Crop').click.wait()
        assert d(text = 'Crop').wait.gone(timeout = 3000)

    def testTurnFDFROnOff(self):
        '''
            Summary: Test turn on/off FD/FR icon
            Steps:   1. Launch gallery and open a picture
                     2. Press menu key
                     3. Turn on/off FD/FR icon
        '''
        self._turnFDFR('Off')
        u.tapOnCenter() #Tap on the face
        #If FDFR has been turned off, tap on the face will make pop card disappear
        assert d(resourceId = 'com.intel.android.gallery3d:id/handle').wait.gone(timeout = 2000)
        self._turnFDFR('On')
        u.tapOnCenter() #Tap on the face
        assert d(text = 'Create new contact').wait.exists(timeout = 2000)

    def testChangeAndRemoveIdentity(self):
        '''
            Summary: Test change identity and remove identity
            Steps:   1. Launch gallery and open a picture has recognized face
                     2. Tap on the face menu icon and select change identity
                     3. Select an exist contact
                     4.Touch face again and tap on the face menu icon ,
                     5.select remove identity.
        '''
        self._recognizeAFace()
        #Change identity
        self._editFDFR('Change identity')
        assert d(text = 'Create new contact').wait.exists(timeout = 2000)
        u.tapOnCenter() #Tap on the contact on the screen center
        assert d(description = 'Delete').wait.exists(timeout = 2000)
        self._removeIdentity()
        u.tapOnCenter()
        assert d(text = 'Create new contact').wait.exists(timeout = 2000)

    def testChangeContactPhoto(self):
        '''
            Summary: Test change contact photo
            Steps:   1. Launch gallery and open a picture has recognized face
                     2. Tap on the face menu icon and select change contact photo
                     3. Click crop
        '''
        self._recognizeAFace()
        #Change contact photo
        self._editFDFR('Change contact photo')
        d(text = 'Crop').click.wait()
        assert d(description = 'Delete').wait.exists(timeout = 2000)

    def testEditContactInfo(self):
        '''
            Summary: Test edit contact info
            Steps:   1. Launch gallery and open a picture has recognized face
                     2. Tap on the face menu icon and select edit contact info
                     3. Change contact name and click done
        '''
        self._recognizeAFace()
        #Edit contact info
        self._editFDFR('Edit contact info')
        d(resourceId = 'com.android.contacts:id/expansion_view').click.wait()
        d(className = 'android.widget.EditText').click.wait() #Highlight the input box
        d(className = 'android.widget.EditText').set_text('NamePrefix')
        d(text = 'Done').click.wait() #Save the contact
        assert d(description = 'Delete').wait.exists(timeout = 2000)

    def testFindOtherPhotos(self):
        '''
            Summary: Test find other photo
            Steps:   1. Launch gallery and open a picture has recognized face
                     2. Tap on the face menu icon and select find other photo
        '''
        self._recognizeAFace()
        #Edit contact info
        self._editFDFR('Find other photos')
        assert d(resourceId = 'com.intel.android.gallery3d:id/action_camera').wait.exists(timeout = 2000)
























    def _removeIdentity(self):
        u.tapOnCenter() #Tap on the face on image
        #Below is to remove the exists face recognize
        if d(description = 'Edit menu').wait.exists(timeout = 2000):
            self._editFDFR('Remove identity')
        else:
            d.press('back')

    def _editFDFR(self,fdfroption):
        u.tapOnCenter() #Tap on the face on image
        d(description = 'Edit menu').click.wait()
        d(text = fdfroption).click.wait()
        try:
            d(text = fdfroption).click.wait() #If the function used as remove identity, it need confirm
        except:
            pass

    def _recognizeAFace(self):
        #Face recognize
        u.tapOnCenter() #Tap on the face
        u.tapOnCenter() #Tap on the contact on the screen center

    def _turnFDFR(self,fdfroption):
        '''
            The function is to turn on/off face identity, usage as below:

            -> _turnFDFR('On')

            *You may need inputing 'On' but not 'on'
        '''
        u.showPopCard()
        d.press('menu')
        if d(text = 'Face recognition %s' %fdfroption).wait.exists(timeout = 2000):
            d(text = 'Face recognition %s' %fdfroption).click.wait()
        else:
            d.press('menu')
