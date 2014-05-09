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

#Max X position
XMAX      = 720
#Y postion for suboption when edit picture
YSUB      = 980
#Per line items' count
ITEMCOUNT = 5
#Width for each item
XUNIT     = XMAX / ITEMCOUNT
#X postion for the center of the first item
XITEM     = XUNIT / 2

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
        #There will be a dialog ask user if save the edited photo when pressing back after case failed
        if d(text = 'Cancel').wait.exists(timeout = 2000):
            d(text = 'Cancel').click.wait()
        u.pressBack(4)

    def testEnterEditScreen(self):
        '''
            Summary: Enter in edit interface
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
        '''
        u.setMenuOptions('Edit')
        assert d(text = 'SAVE').wait.exists(timeout = 2000)

    def testEditWithToneNone(self):
        '''
            Summary: Enter toning interface with selected none mode 
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch toning icon
                     5.Touch none mode
                     6.Touch save
        '''
        self._editImage('fx',1)
        assert d(text = 'SAVE').wait.gone(timeout = 2000)

    def testEditWithTonePunch(self):
        '''
            Summary: Enter toning interface with selected punch mode 
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch toning icon
                     5.Touch punch mode
                     6.Touch save
        '''
        self._editAndCheckIamgesCount('fx',2)

    def testEditWithToneVintage(self):
        '''
            Summary: Enter toning interface with selected vintage mode 
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch toning icon
                     5.Touch vintage mode
                     6.Touch save
        '''
        self._editAndCheckIamgesCount('fx',3)

    def testEditWithToneBW(self):
        '''
            Summary: Enter toning interface with selected B/W mode 
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch toning icon
                     5.Touch B/W mode
                     6.Touch save
        '''
        self._editAndCheckIamgesCount('fx',4)

    def testEditWithToneBleach(self):
        '''
            Summary: Enter toning interface with selected bleach mode 
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch toning icon
                     5.Touch bleach mode
                     6.Touch save
        '''
        self._editAndCheckIamgesCount('fx',5)

    def testEditWithToneInstant(self):
        '''
            Summary: Enter toning interface with selected instant mode 
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch toning icon
                     5.Touch instant mode
                     6.Touch save
        '''
        self._editAndCheckIamgesCount('fx',6)

    def testEditWithToneLatte(self):
        '''
            Summary: Enter toning interface with selected latte mode 
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch toning icon
                     5.Touch latte mode
                     6.Touch save
        '''
        self._editAndCheckIamgesCount('fx',7)

    def testEditWithToneBlue(self):
        '''
            Summary: Enter toning interface with selected blue mode 
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch toning icon
                     5.Touch blue mode
                     6.Touch save
        '''
        self._editAndCheckIamgesCount('fx',8)

    def testEditWithToneLitho(self):
        '''
            Summary: Enter toning interface with selected litho mode 
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch toning icon
                     5.Touch litho mode
                     6.Touch save
        '''
        self._editAndCheckIamgesCount('fx',9)

    def testEditWithToneXProcess(self):
        '''
            Summary: Enter toning interface with selected X-Process mode 
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch toning icon
                     5.Touch X-Process mode
                     6.Touch save
        '''
        self._editAndCheckIamgesCount('fx',10)

    def testEditWithFrame1(self):
        '''
            Summary: Enter photo frame interface with selected the first style  
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch photo frame icon
                     5.Touch the first style
                     6.Touch save
        '''
        self._editImage('border',1)
        assert d(text = 'SAVE').wait.gone(timeout = 2000)

    def testEditWithFrame2(self):
        '''
            Summary: Enter photo frame interface with selected the second style  
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch photo frame icon
                     5.Touch the second style
                     6.Touch save
        '''
        self._editAndCheckIamgesCount('border',2)

    def testEditWithFrame3(self):
        '''
            Summary: Enter photo frame interface with selected the third style  
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch photo frame icon
                     5.Touch the third style
                     6.Touch save
        '''
        self._editAndCheckIamgesCount('border',3)

    def testEditWithFrame4(self):
        '''
            Summary: Enter photo frame interface with selected the forth style  
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch photo frame icon
                     5.Touch the forth style
                     6.Touch save
        '''
        self._editAndCheckIamgesCount('border',4)

    def testEditWithFrame5(self):
        '''
            Summary: Enter photo frame interface with selected the fifth style  
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch photo frame icon
                     5.Touch the fifth style
                     6.Touch save
        '''
        self._editAndCheckIamgesCount('border',5)

    def testEditWithFrame6(self):
        '''
            Summary: Enter photo frame interface with selected the sixth style  
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch photo frame icon
                     5.Touch the sixth style
                     6.Touch save
        '''
        self._editAndCheckIamgesCount('border',6)

    def testEditWithFrame7(self):
        '''
            Summary: Enter photo frame interface with selected the seventh style  
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch photo frame icon
                     5.Touch the seventh style
                     6.Touch save
        '''
        self._editAndCheckIamgesCount('border',6)

    def testEnterCropScreen(self):
        '''
            Summary: Enter Crop interface 
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch Crop icon
        '''
        u.setMenuOptions('Edit')
        d(resourceId = 'com.intel.android.gallery3d:id/geometryButton').click.wait()
        assert d(resourceId = 'com.intel.android.gallery3d:id/straightenButton').wait.exists(timeout = 2000)

    def testEditWithCropStraighten(self):
        '''
            Summary: Enter Crop interface with selected straighten mode 
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch Crop icon
                     5.Touch straighten mode
                     6.Apply one positive straightening adjustment
                     7.Touch save
        '''
        self._editImage('geometry','straighten')

    def testEditWithCropWith1ratio1(self):
        '''
            Summary: Enter Crop interface with selected Crop mode
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch Crop icon
                     5.Touch Crop mode and select 1:1 option
                     6.Touch save
        '''
        self._editAndCheckIamgesCount('geometry','crop','1:1')

    def testEditWithCropWith1ratio2(self):
        '''
            Summary: Enter Crop interface with selected Crop mode
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch Crop icon
                     5.Touch Crop mode and select 4:3 option
                     6.Touch save
        '''
        self._editAndCheckIamgesCount('geometry','crop','4:3')

    def testEditWithCropWith1ratio3(self):
        '''
            Summary: Enter Crop interface with selected Crop mode
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch Crop icon
                     5.Touch Crop mode and select 3:4 option
                     6.Touch save
        '''
        self._editAndCheckIamgesCount('geometry','crop','3:4')

    def testEditWithCropWith1ratio4(self):
        '''
            Summary: Enter Crop interface with selected Crop mode
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch Crop icon
                     5.Touch Crop mode and select 5:7 option
                     6.Touch save
        '''
        self._editAndCheckIamgesCount('geometry','crop','5:7')

    def testEditWithCropWith1ratio5(self):
        '''
            Summary: Enter Crop interface with selected Crop mode
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch Crop icon
                     5.Touch Crop mode and select 7:5 option
                     6.Touch save
        '''
        self._editAndCheckIamgesCount('geometry','crop','7:5')

    def testEditWithCropWith1ratio6(self):
        '''
            Summary: Enter Crop interface with selected Crop mode
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch Crop icon
                     5.Touch Crop mode and select None option
                     6.Touch save
        '''
        self._editImage('geometry','crop','None')
        assert d(description = 'Share').wait.exists(timeout = 2000)

    def testEditWithCropWith1ratio7(self):
        '''
            Summary: Enter Crop interface with selected Crop mode
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch Crop icon
                     5.Touch Crop mode and select Original option
                     6.Touch save
        '''
        self._editImage('geometry','crop','Original')
        assert d(description = 'Share').wait.exists(timeout = 2000)

    def testEditWithCropWithRotate(self):
        '''
            Summary: Enter Crop interface with selected Rotate mode
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch Crop icon
                     5.Touch Rotate mode
                     6.Drag screen from right to left  one time and Apply rotate 
                     7.Touch Save Icon
        '''
        self._editImage('geometry','rotate')
        assert d(description = 'Share').wait.exists(timeout = 2000)

    def testEditWithCropWithMirror(self):
        '''
            Summary: Enter Crop interface with selected Mirror mode
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch Crop icon
                     5.Touch Mirror mode
                     6.Drag screen from right to left  one time and Apply rotate 
                     7.Touch Save Icon
        '''
        self._editImage('geometry','flip')
        assert d(description = 'Share').wait.exists(timeout = 2000)

    def testEditWithBrightnessWithAutocolor(self):
        '''
            Summary: Enter Brightness interface with selected Autocolor mode
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch Brightness icon
                     5.Touch Autocolor mode
                     6.Apply and save it
        '''
        self._editImage('colors',1)
        assert d(description = 'Share').wait.exists(timeout = 2000)

    def testEditWithBrightnessWithExposure(self):
        '''
            Summary: Enter Brightness interface with selected Exposure mode
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch Brightness icon
                     5.Touch Exposure mode
                     6.Apply and save it
        '''
        self._editImage('colors',2)
        assert d(description = 'Share').wait.exists(timeout = 2000)

    def testEditWithBrightnessWithVignette(self):
        '''
            Summary: Enter Brightness interface with selected Vignette mode
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch Brightness icon
                     5.Touch Vignette mode
                     6.Apply and save it
        '''
        self._editImage('colors',3)
        assert d(description = 'Share').wait.exists(timeout = 2000)

    def testEditWithBrightnessWithContrast(self):
        '''
            Summary: Enter Brightness interface with selected Contrast mode
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch Brightness icon
                     5.Touch Contrast mode
                     6.Apply and save it
        '''
        self._editImage('colors',4)
        assert d(description = 'Share').wait.exists(timeout = 2000)

    def testEditWithBrightnessWithShadows(self):
        '''
            Summary: Enter Brightness interface with selected Shadows mode
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch Brightness icon
                     5.Touch Shadows mode
                     6.Apply and save it
        '''
        self._editImage('colors',5)
        assert d(description = 'Share').wait.exists(timeout = 2000)

    def testEditWithBrightnessWithVibrance(self):
        '''
            Summary: Enter Brightness interface with selected Vibrance mode
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch Brightness icon
                     5.Touch Vibrance mode
                     6.Apply and save it
        '''
        self._editImage('colors',6)
        assert d(description = 'Share').wait.exists(timeout = 2000)

    def testEditWithBrightnessWithSharpness(self):
        '''
            Summary: Enter Brightness interface with selected Sharpness mode
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch Brightness icon
                     5.Touch Sharpness mode
                     6.Apply and save it
        '''
        self._editImage('colors',7)
        assert d(description = 'Share').wait.exists(timeout = 2000)

    def testEditWithBrightnessWithCurves(self):
        '''
            Summary: Enter Brightness interface with selected Curves mode
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch Brightness icon
                     5.Touch Curves mode
                     6.Apply and save it
        '''
        self._editImage('colors',8)
        assert d(description = 'Share').wait.exists(timeout = 2000)

    def testEditWithBrightnessWithHue(self):
        '''
            Summary: Enter Brightness interface with selected Hue mode
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch Brightness icon
                     5.Touch Hue mode
                     6.Apply and save it
        '''
        self._editImage('colors',9)
        assert d(description = 'Share').wait.exists(timeout = 2000)

    def testEditWithBrightnessWithSaturation(self):
        '''
            Summary: Enter Brightness interface with selected Saturation mode
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch Brightness icon
                     5.Touch Saturation mode
                     6.Apply and save it
        '''
        self._editImage('colors',10)
        assert d(description = 'Share').wait.exists(timeout = 2000)

    def testEditWithBrightnessWithBWFilter(self):
        '''
            Summary: Enter Brightness interface with selected B/WFilter mode
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch Brightness icon
                     5.Touch B/WFilter mode
                     6.Apply and save it
        '''
        self._editImage('colors',11)
        assert d(description = 'Share').wait.exists(timeout = 2000)

    def testEditWithTonePunchRedoAndUndo(self):
        '''
            Summary: Enter enter interface select a mode and click undo then click redo
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch toning icon
                     5.Touch punch
                     6.Touch setting menu
                     7.Touch undo
                     8.Touch setting menu
                     9.Touch redo
                     10.Touch Save
        '''
        u.setMenuOptions('Edit')
        #Tap on punch option
        d(index = 1, className = 'android.view.View').click.wait()
        u.setMenuOptions('Undo')
        u.setMenuOptions('Redo')
        #Save the changed image
        d(text = 'SAVE').click.wait()
        assert d(description = 'Share').wait.exists(timeout = 2000)

    def testEditWithTonePunchReset(self):
        '''
            Summary: Enter enter interface select a mode and click reset
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch toning icon
                     5.Touch punch
                     6.Touch setting menu
                     7.Touch Reset
                     8.Touch Save
        '''
        u.setMenuOptions('Edit')
        #Tap on punch option
        d(index = 1, className = 'android.view.View').click.wait()
        u.setMenuOptions('Reset')
        #Save the changed image
        d(text = 'SAVE').click.wait()
        assert d(description = 'Share').wait.exists(timeout = 2000)

    def testEditWithTonePunchShowHistory(self):
        '''
            Summary: Enter enter interface select a mode and click Show history 
            Steps:   1.Enter full view
                     2.Click setting menu
                     3.Touch edit
                     4.Touch toning icon
                     5.Touch punch
                     6.Touch setting menu
                     7.Touch Show History
                     8.Touch Save
        '''
        u.setMenuOptions('Edit')
        #Tap on punch option
        d(index = 1, className = 'android.view.View').click.wait()
        u.setMenuOptions('Show history')
        assert d(text = 'History').wait.exists(timeout = 2000)
        #Save the changed image
        d(text = 'SAVE').click.wait()
        assert d(description = 'Share').wait.exists(timeout = 2000)























    def _editImage(self,bottombutton,suboption,cropscale=None):
        '''
            You need just know the NO. of the wanted option, e.g.:
                you want to set an image as 'Hue' in 'Colors',

                -> _editImage('colors',9)

                *Hue is NO.9 in the option list
                *An exception, if you set something in geometry(3rd button on the bottom), you may use func like:

                -> _editImage('geometry','crop')

                *You could just use the string shows on screen

            Comparison Table:

                NO.| bottombutton | suboption            | cropscale
            -------+--------------+----------------------+---------------------
                1. | fx           | int 1 ~ 10           |
                2. | border       | int 1 ~ 7            |
                3. | geometry     | str straighten       |
                   |              |     crop             | str 1:1
                   |              |                      |     4:3
                   |              |                      |     3:4
                   |              |                      |     5:7
                   |              |                      |     7:5
                   |              |                      |     None
                   |              |                      |     Original
                   |              |     rotate           |
                   |              |     flip (*'Mirror') |
                4. | colors       | int 1 ~ 11           |
            -------+--------------+----------------------+---------------------

        '''
        u.setMenuOptions('Edit')
        #Click bottom button
        d(resourceId = 'com.intel.android.gallery3d:id/%sButton'%bottombutton).click.wait()
        if bottombutton == 'geometry':
            d(resourceId = 'com.intel.android.gallery3d:id/%sButton'%suboption).click.wait()
        else:
            if suboption < 6:
                d(index = suboption-1,focusable = 'false',clickable = 'true').click.wait()
                #d.click(XITEM + XUNIT * (suboption - 1), YSUB)
            elif suboption == 11:
                d.swipe(XMAX-1, YSUB, 0, YSUB, 5) #Swipe to the end
                #d.click(XITEM + XUNIT * 4, YSUB)
                d(index = suboption-1,focusable = 'false',clickable = 'true').click.wait()
            else:
                d.swipe(XMAX-1, YSUB, 0, YSUB, 60) #Swipe the 5th item to the 0 position(out of screen)
                #d.click(XITEM + XUNIT * (suboption - ITEMCOUNT - 1), YSUB)
                d(index = suboption-1,focusable = 'false',clickable = 'true').click.wait()
        #When croping image, there are some expend options
        if cropscale != None:
            d(resourceId = 'com.intel.android.gallery3d:id/aspect').click.wait()
            d(text = cropscale).click.wait()
        #Some effect may need user's applying
        if d(text = 'Apply').wait.exists(timeout = 2000):
            d(text = 'Apply').click.wait()
        #Save the changed image
        d(text = 'SAVE').click.wait()
        
    def _editAndCheckIamgesCount(self,bottombutton,suboption,cropscale=None):
        beforeNo = commands.getoutput('adb shell ls -l /sdcard/testalbum/testpictures2 | grep JPG | wc -l')
        #print beforeNo
        self._editImage(bottombutton,suboption,cropscale)
        time.sleep(5) #Saving action may take a few seconds
        afterNo  = commands.getoutput('adb shell ls -l /sdcard/testalbum/testpictures2 | grep JPG | wc -l')
        #print afterNo
        if string.atoi(afterNo) - string.atoi(beforeNo) == 0:
            self.fail('New image has not been created after editing')
